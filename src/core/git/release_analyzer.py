"""
Git release analyzer for Codex-AI.

Analyzes changes between Git tags/releases with detailed or simple output.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from constants.git import EXCLUDE_PATTERNS
from .log_analyzer import GitLogAnalyzer, CommitInfo


@dataclass
class ReleaseInfo:
    """Represents information about a Git release/tag."""
    tag: str
    date: str
    commit_hash: str
    is_first_release: bool = False


@dataclass
class ReleaseComparison:
    """Represents a comparison between two releases."""
    current_release: ReleaseInfo
    previous_release: Optional[ReleaseInfo]
    commits: List[CommitInfo]
    diff_stats: str = ""
    full_diff: str = ""


class GitReleaseAnalyzer:
    """
    Analyzes Git releases and changes between tags.
    
    Provides detailed and simple analysis of changes between Git releases
    with improved error handling and structured data output.
    """
    
    def __init__(self, repo_path: str = ".", output_dir: Optional[str] = None):
        """
        Initialize Git release analyzer.
        
        Args:
            repo_path: Path to Git repository (default: current directory)
            output_dir: Output directory for generated files (default: .tmp)
        """
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir) if output_dir else self.repo_path / ".tmp"
        self.log_analyzer = GitLogAnalyzer(repo_path, output_dir)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _run_git_command(self, command: List[str]) -> str:
        """
        Run a Git command and return output.
        
        Args:
            command: Git command as list of strings
            
        Returns:
            Command output as string
            
        Raises:
            RuntimeError: If Git command fails
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")
    
    def is_git_repository(self) -> bool:
        """Check if current directory is a Git repository."""
        try:
            self._run_git_command(["git", "rev-parse", "--is-inside-work-tree"])
            return True
        except RuntimeError:
            return False
    
    def get_current_tag(self) -> Optional[str]:
        """
        Get the current/latest tag.
        
        Returns:
            Current tag name or None if no tags exist
        """
        try:
            return self._run_git_command(["git", "describe", "--tags", "--abbrev=0"])
        except RuntimeError:
            return None
    
    def get_all_tags(self) -> List[str]:
        """
        Get all tags sorted by creation date (newest first).
        
        Returns:
            List of tag names sorted by creation date
        """
        try:
            tags_output = self._run_git_command(["git", "tag", "--sort=-creatordate"])
            if not tags_output:
                return []
            return tags_output.split('\n')
        except RuntimeError:
            return []
    
    def get_tag_info(self, tag: str) -> ReleaseInfo:
        """
        Get information about a specific tag.
        
        Args:
            tag: Tag name
            
        Returns:
            ReleaseInfo object with tag details
        """
        try:
            # Get tag commit hash
            commit_hash = self._run_git_command(["git", "rev-list", "-n", "1", tag])
            
            # Get tag date
            date = self._run_git_command(["git", "log", "-1", "--format=%ai", tag])
            
            return ReleaseInfo(
                tag=tag,
                date=date,
                commit_hash=commit_hash
            )
        except RuntimeError:
            return ReleaseInfo(
                tag=tag,
                date="Unknown",
                commit_hash="Unknown"
            )
    
    def get_first_commit(self) -> str:
        """Get the hash of the first commit in the repository."""
        try:
            return self._run_git_command(["git", "rev-list", "--max-parents=0", "HEAD"])
        except RuntimeError:
            raise RuntimeError("Could not find first commit")
    
    def find_previous_tag(self, current_tag: str) -> Optional[str]:
        """
        Find the previous tag before the current one.
        
        Args:
            current_tag: Current tag name
            
        Returns:
            Previous tag name or None if this is the first release
        """
        all_tags = self.get_all_tags()
        
        try:
            current_index = all_tags.index(current_tag)
            if current_index == len(all_tags) - 1:
                # This is the first release
                return None
            return all_tags[current_index + 1]
        except ValueError:
            # Current tag not found in list
            return None
    
    def get_commits_between_releases(self, previous_ref: str, current_ref: str, 
                                   include_first_commit: bool = False, mode: str = 'detailed') -> List[CommitInfo]:
        """
        Get all commits between two releases.
        
        Args:
            previous_ref: Previous release reference (tag or commit)
            current_ref: Current release reference (tag or commit)
            include_first_commit: Whether to include the first commit for first release
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            List of CommitInfo objects
        """
        commits = []
        
        # For first release, include the first commit
        if include_first_commit:
            try:
                first_commit = self.get_first_commit()
                commit_info = self.log_analyzer._analyze_commit(first_commit, mode)
                commits.append(commit_info)
            except RuntimeError:
                pass
        
        # Get commits in range
        try:
            range_spec = f"{previous_ref}..{current_ref}"
            commits_output = self._run_git_command([
                "git", "rev-list", "--reverse", range_spec
            ])
            
            if commits_output:
                commit_hashes = commits_output.split('\n')
                for commit_hash in commit_hashes:
                    commit_info = self.log_analyzer._analyze_commit(commit_hash, mode)
                    commits.append(commit_info)
                    
                    # If it's a merge commit, also include introduced commits
                    if commit_info.is_merge:
                        introduced_commits = self.log_analyzer.get_commits_in_merge(commit_hash)
                        for intro_commit in introduced_commits:
                            if intro_commit != commit_hash:  # Don't duplicate
                                intro_info = self.log_analyzer._analyze_commit(intro_commit, mode)
                                commits.append(intro_info)
        except RuntimeError:
            pass
        
        return commits
    
    def get_diff_between_releases(self, previous_ref: str, current_ref: str, 
                                 detailed: bool = True) -> str:
        """
        Get diff between two releases.
        
        Args:
            previous_ref: Previous release reference
            current_ref: Current release reference
            detailed: If True, return full diff; if False, return stat summary
            
        Returns:
            Diff output as string
        """
        try:
            exclude_pathspec = self.log_analyzer.exclude_pathspec
            
            if detailed:
                # Full diff with patches
                return self._run_git_command([
                    "git", "diff", f"{previous_ref}..{current_ref}", 
                    "--", ".", exclude_pathspec
                ])
            else:
                # Just statistics
                return self._run_git_command([
                    "git", "diff", "--stat", f"{previous_ref}..{current_ref}",
                    "--", ".", exclude_pathspec
                ])
        except RuntimeError:
            return "Error generating diff"
    
    def analyze_current_release(self, mode: str = 'detailed') -> Optional[ReleaseComparison]:
        """
        Analyze the current release and compare with previous.
        
        Args:
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            ReleaseComparison object or None if no releases found
        """
        if not self.is_git_repository():
            raise RuntimeError("Not in a Git repository")
        
        current_tag = self.get_current_tag()
        if not current_tag:
            return None
        
        # Get current release info
        current_release = self.get_tag_info(current_tag)
        
        # Find previous release
        previous_tag = self.find_previous_tag(current_tag)
        previous_release = None
        previous_ref = None
        is_first_release = False
        
        if previous_tag:
            previous_release = self.get_tag_info(previous_tag)
            previous_ref = previous_tag
        else:
            # This is the first release
            is_first_release = True
            current_release.is_first_release = True
            try:
                first_commit = self.get_first_commit()
                previous_ref = f"{first_commit}^{{}}"  # Use commit^{} syntax
            except RuntimeError:
                previous_ref = current_tag  # Fallback
        
        # Get commits between releases with correct mode
        commits = self.get_commits_between_releases(
            previous_ref, current_tag, include_first_commit=is_first_release, mode=mode
        )
        
        # Get diff information
        diff_stats = ""
        full_diff = ""
        
        if previous_ref:
            if mode == 'detailed':
                full_diff = self.get_diff_between_releases(previous_ref, current_tag, detailed=True)
            diff_stats = self.get_diff_between_releases(previous_ref, current_tag, detailed=False)
        
        return ReleaseComparison(
            current_release=current_release,
            previous_release=previous_release,
            commits=commits,
            diff_stats=diff_stats,
            full_diff=full_diff
        )
    
    def format_release_output(self, comparison: ReleaseComparison, mode: str = 'detailed') -> str:
        """
        Format release comparison for output.
        
        Args:
            comparison: ReleaseComparison object
            mode: Output mode ('detailed' or 'simple')
            
        Returns:
            Formatted string output
        """
        output = []
        
        # Compact header with release information
        output.append(f"CURRENT: {comparison.current_release.tag} ({comparison.current_release.date})")
        
        if comparison.previous_release:
            output.append(f"PREVIOUS: {comparison.previous_release.tag} ({comparison.previous_release.date})")
        else:
            output.append("PREVIOUS: First Release")
        
        output.append("=" * 20)
        
        # Commits section - more compact
        for commit in comparison.commits:
            commit_type = "MERGE" if commit.is_merge else "COMMIT"
            output.append(f"{commit_type}: {commit.hash[:8]} | {commit.author} | {commit.date}")
            output.append(f"  {commit.message}")
            
            # Only add body if it's not empty and different from message
            if commit.body and commit.body.strip() and commit.body.strip() != commit.message.strip():
                # Compact body - remove extra newlines
                body_lines = [line.strip() for line in commit.body.split('\n') if line.strip()]
                if body_lines:
                    output.append(f"  Body: {' '.join(body_lines)}")
            
            if mode == 'detailed' and commit.patch:
                output.append(commit.patch)
            elif mode == 'simple' and commit.files_changed:
                # Show all files with status (A/M/D/R)
                output.append("  Files:")
                for file_change in commit.files_changed:
                    output.append(f"    {file_change}")
            
            output.append("-" * 20)
        
        # Diff section - only if significant
        if mode == 'detailed' and comparison.full_diff:
            output.append("FULL DIFF:")
            output.append(comparison.full_diff)
        elif mode == 'simple' and comparison.diff_stats:
            output.append("CHANGES SUMMARY:")
            output.append(comparison.diff_stats)
        
        output.append("=" * 20)
        
        return '\n'.join(output)
    
    def save_detailed_output(self) -> Optional[str]:
        """
        Save detailed release analysis to {output_dir}/git_release_detailed.txt.
        
        Returns:
            Path to output file or None if no releases found
        """
        comparison = self.analyze_current_release('detailed')
        if not comparison:
            return None
        
        output = self.format_release_output(comparison, 'detailed')
        
        output_file = self.output_dir / "git_release_detailed.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        return str(output_file)
    
    def save_simple_output(self) -> Optional[str]:
        """
        Save simple release analysis to {output_dir}/git_release_simple.txt.
        
        Returns:
            Path to output file or None if no releases found
        """
        comparison = self.analyze_current_release('simple')
        if not comparison:
            return None
        
        output = self.format_release_output(comparison, 'simple')
        
        output_file = self.output_dir / "git_release_simple.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        return str(output_file)
    
    def analyze_release_range(self, from_tag: str, to_tag: str, mode: str = 'detailed') -> ReleaseComparison:
        """
        Analyze changes between two specific releases.
        
        Args:
            from_tag: Starting release tag
            to_tag: Ending release tag
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            ReleaseComparison object
        """
        current_release = self.get_tag_info(to_tag)
        previous_release = self.get_tag_info(from_tag)
        
        # Get commits between releases
        commits = self.get_commits_between_releases(from_tag, to_tag)
        
        # Get diff information
        diff_stats = self.get_diff_between_releases(from_tag, to_tag, detailed=False)
        full_diff = ""
        
        if mode == 'detailed':
            full_diff = self.get_diff_between_releases(from_tag, to_tag, detailed=True)
        
        return ReleaseComparison(
            current_release=current_release,
            previous_release=previous_release,
            commits=commits,
            diff_stats=diff_stats,
            full_diff=full_diff
        )


# Convenience functions for backward compatibility
def analyze_current_release_detailed() -> Optional[str]:
    """Analyze current release in detailed mode and save to .tmp/git_release_detailed.txt."""
    analyzer = GitReleaseAnalyzer()
    return analyzer.save_detailed_output()


def analyze_current_release_simple() -> Optional[str]:
    """Analyze current release in simple mode and save to .tmp/git_release_simple.txt."""
    analyzer = GitReleaseAnalyzer()
    return analyzer.save_simple_output()
