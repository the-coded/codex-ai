"""
Git log analyzer for Codex-AI.

Ports the functionality from old/bin/git_log_*.sh scripts to Python.
Provides detailed and simple analysis of Git commits, with special handling for merge commits.
"""

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from constants.git import EXCLUDE_PATTERNS, GIT_COMMANDS


@dataclass
class CommitInfo:
    """Represents information about a Git commit."""
    hash: str
    author: str
    date: str
    message: str
    body: str
    is_merge: bool = False
    parents: List[str] = None
    files_changed: List[str] = None
    patch: str = ""
    
    def __post_init__(self):
        if self.parents is None:
            self.parents = []
        if self.files_changed is None:
            self.files_changed = []


class GitLogAnalyzer:
    """
    Analyzes Git log with detailed or simple output.
    
    Provides Python equivalent of git_log_detailed.sh and git_log_simple.sh
    with improved error handling and structured data output.
    """
    
    def __init__(self, repo_path: str = ".", output_dir: Optional[str] = None):
        """
        Initialize Git log analyzer.
        
        Args:
            repo_path: Path to Git repository (default: current directory)
            output_dir: Output directory for generated files (default: .tmp)
        """
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir) if output_dir else self.repo_path / ".tmp"
        self.exclude_pathspec = self._build_exclude_pathspec()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _build_exclude_pathspec(self) -> str:
        """Build Git pathspec for excluding files from analysis."""
        excludes = []
        for pattern in EXCLUDE_PATTERNS:
            excludes.append(f":(exclude){pattern}")
        return " ".join(excludes)
    
    def _run_git_command(self, command: List[str]) -> str:
        """
        Run a Git command and return output.
        
        Args:
            command: Git command as list of strings
            
        Returns:
            Command output as string
            
        Raises:
            subprocess.CalledProcessError: If Git command fails
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
    
    def get_last_commit_hash(self) -> str:
        """Get hash of the last commit (HEAD)."""
        return self._run_git_command(["git", "rev-parse", "HEAD"])
    
    def get_commit_count(self, since_commit: Optional[str] = None, branch: Optional[str] = None) -> int:
        """
        Get count of commits in range.
        
        Args:
            since_commit: Start commit/tag/date (exclusive)
            branch: Branch to analyze (default: current)
            
        Returns:
            Number of commits
        """
        try:
            cmd = ["git", "rev-list", "--count"]
            
            if since_commit:
                if branch:
                    cmd.append(f"{since_commit}..{branch}")
                else:
                    cmd.append(f"{since_commit}..HEAD")
            else:
                if branch:
                    cmd.append(branch)
                else:
                    cmd.append("HEAD")
            
            count_output = self._run_git_command(cmd)
            return int(count_output.strip())
        except (RuntimeError, ValueError):
            return 0
    
    def generate_detailed_log(self, output_file: str, since_commit: Optional[str] = None, branch: Optional[str] = None) -> bool:
        """
        Generate detailed git log to file.
        
        Args:
            output_file: Output file path
            since_commit: Start commit/tag/date (exclusive)
            branch: Branch to analyze (default: current)
            
        Returns:
            True if successful
        """
        try:
            commits = self.analyze_commit_range(since_commit, branch, 'detailed')
            
            output_lines = []
            for commit in commits:
                output_lines.append(self.format_commit_output(commit, 'detailed'))
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            
            return True
        except Exception:
            return False
    
    def generate_simple_log(self, output_file: str, since_commit: Optional[str] = None, branch: Optional[str] = None) -> bool:
        """
        Generate simple git log to file.
        
        Args:
            output_file: Output file path
            since_commit: Start commit/tag/date (exclusive)
            branch: Branch to analyze (default: current)
            
        Returns:
            True if successful
        """
        try:
            commits = self.analyze_commit_range(since_commit, branch, 'simple')
            
            output_lines = []
            for commit in commits:
                output_lines.append(self.format_commit_output(commit, 'simple'))
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            
            return True
        except Exception:
            return False
    
    def is_merge_commit(self, commit_hash: str) -> bool:
        """
        Check if a commit is a merge commit.
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            True if commit is a merge commit
        """
        try:
            parents_output = self._run_git_command([
                "git", "rev-list", "--parents", "-n", "1", commit_hash
            ])
            # Split by space and count parents (first element is the commit itself)
            parents_count = len(parents_output.split()) - 1
            return parents_count > 1
        except RuntimeError:
            return False
    
    def get_merge_parents(self, commit_hash: str) -> Tuple[str, str]:
        """
        Get parent commits of a merge commit.
        
        Args:
            commit_hash: Git commit hash of merge commit
            
        Returns:
            Tuple of (parent1, parent2) commit hashes
            
        Raises:
            ValueError: If commit is not a merge commit
        """
        if not self.is_merge_commit(commit_hash):
            raise ValueError(f"Commit {commit_hash} is not a merge commit")
        
        parents_output = self._run_git_command([
            "git", "rev-list", "--parents", "-n", "1", commit_hash
        ])
        parents = parents_output.split()[1:]  # Skip the commit itself
        
        if len(parents) < 2:
            raise ValueError(f"Merge commit {commit_hash} has less than 2 parents")
        
        return parents[0], parents[1]
    
    def get_commits_in_merge(self, commit_hash: str) -> List[str]:
        """
        Get list of commits introduced by a merge.
        
        Args:
            commit_hash: Git commit hash of merge commit
            
        Returns:
            List of commit hashes introduced by the merge
        """
        if not self.is_merge_commit(commit_hash):
            return [commit_hash]
        
        parent1, parent2 = self.get_merge_parents(commit_hash)
        
        # Get commits from non-main parent (assuming parent1 is main branch)
        try:
            commits_output = self._run_git_command([
                "git", "rev-list", "--reverse", f"{parent1}..{commit_hash}"
            ])
            if commits_output:
                return commits_output.split('\n')
            return []
        except RuntimeError:
            return []
    
    def analyze_last_commit(self, mode: str = 'detailed') -> CommitInfo:
        """
        Analyze the last commit (HEAD).
        
        Args:
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            CommitInfo object with commit details
        """
        last_commit = self.get_last_commit_hash()
        return self._analyze_commit(last_commit, mode)
    
    def analyze_commit_range(self, since: Optional[str] = None, 
                           until: Optional[str] = None, 
                           mode: str = 'detailed') -> List[CommitInfo]:
        """
        Analyze a range of commits.
        
        Args:
            since: Start commit/tag/date (exclusive)
            until: End commit/tag/date (inclusive, default: HEAD)
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            List of CommitInfo objects
        """
        # Build commit range
        if until is None:
            until = "HEAD"
        
        if since is None:
            # Get all commits from the beginning
            try:
                commits_output = self._run_git_command([
                    "git", "rev-list", "--reverse", until
                ])
                if not commits_output:
                    return []
                
                commit_hashes = commits_output.split('\n')
                return [self._analyze_commit(commit, mode) for commit in commit_hashes]
            except RuntimeError:
                return []
        
        # Get commits in range
        range_spec = f"{since}..{until}"
        try:
            commits_output = self._run_git_command([
                "git", "rev-list", "--reverse", range_spec
            ])
            if not commits_output:
                return []
            
            commit_hashes = commits_output.split('\n')
            return [self._analyze_commit(commit, mode) for commit in commit_hashes]
        except RuntimeError:
            return []
    
    def _analyze_commit(self, commit_hash: str, mode: str = 'detailed') -> CommitInfo:
        """
        Analyze a single commit.
        
        Args:
            commit_hash: Git commit hash
            mode: Analysis mode ('detailed' or 'simple')
            
        Returns:
            CommitInfo object with commit details
        """
        is_merge = self.is_merge_commit(commit_hash)
        
        if is_merge:
            return self._analyze_merge_commit(commit_hash, mode)
        else:
            return self._analyze_regular_commit(commit_hash, mode)
    
    def _analyze_regular_commit(self, commit_hash: str, mode: str = 'detailed') -> CommitInfo:
        """Analyze a regular (non-merge) commit."""
        # Get commit info
        commit_info = self._get_commit_basic_info(commit_hash)
        
        # Get files changed and patch if needed
        if mode == 'detailed':
            commit_info.patch = self._get_commit_patch(commit_hash)
        else:
            commit_info.files_changed = self._get_commit_files(commit_hash)
        
        return commit_info
    
    def _analyze_merge_commit(self, commit_hash: str, mode: str = 'detailed') -> CommitInfo:
        """Analyze a merge commit."""
        # Get basic merge commit info
        commit_info = self._get_commit_basic_info(commit_hash)
        commit_info.is_merge = True
        
        try:
            commit_info.parents = list(self.get_merge_parents(commit_hash))
        except ValueError:
            # Fallback for malformed merge commits
            commit_info.parents = []
        
        # Get patch or files for the merge itself
        if mode == 'detailed':
            commit_info.patch = self._get_commit_patch(commit_hash)
        else:
            commit_info.files_changed = self._get_commit_files(commit_hash)
        
        return commit_info
    
    def _get_commit_basic_info(self, commit_hash: str) -> CommitInfo:
        """Get basic commit information (author, date, message, body)."""
        try:
            # Get commit details
            commit_output = self._run_git_command([
                "git", "show", "--pretty=format:%an%n%ad%n%s%n%b", 
                "--no-patch", commit_hash
            ])
            
            lines = commit_output.split('\n')
            if len(lines) < 3:
                # Fallback for malformed commits
                return CommitInfo(
                    hash=commit_hash,
                    author="Unknown",
                    date="Unknown",
                    message="Unknown",
                    body=""
                )
            
            author = lines[0]
            date = lines[1]
            message = lines[2]
            body = '\n'.join(lines[3:]).strip() if len(lines) > 3 else ""
            
            return CommitInfo(
                hash=commit_hash,
                author=author,
                date=date,
                message=message,
                body=body
            )
        except RuntimeError:
            # Fallback for Git errors
            return CommitInfo(
                hash=commit_hash,
                author="Unknown",
                date="Unknown", 
                message="Error retrieving commit info",
                body=""
            )
    
    def _get_commit_patch(self, commit_hash: str) -> str:
        """Get full patch for a commit."""
        try:
            return self._run_git_command([
                "git", "show", "--patch", commit_hash, "--", ".", self.exclude_pathspec
            ])
        except RuntimeError:
            return "Error retrieving patch"
    
    def _get_commit_files(self, commit_hash: str) -> List[str]:
        """Get list of files changed in a commit."""
        try:
            files_output = self._run_git_command([
                "git", "show", "--name-status", commit_hash, "--", ".", self.exclude_pathspec
            ])
            # Parse name-status output (e.g., "M\tfile.py", "A\tfile.js")
            files = []
            for line in files_output.split('\n'):
                if '\t' in line:
                    status, filename = line.split('\t', 1)
                    files.append(f"{status}\t{filename}")
            return files
        except RuntimeError:
            return []
    
    def format_commit_output(self, commit_info: CommitInfo, mode: str = 'detailed') -> str:
        """
        Format commit information for output.
        
        Args:
            commit_info: CommitInfo object
            mode: Output mode ('detailed' or 'simple')
            
        Returns:
            Formatted string output
        """
        output = []
        
        # Compact header
        commit_type = "MERGE" if commit_info.is_merge else "COMMIT"
        output.append(f"{commit_type}: {commit_info.hash[:8]} | {commit_info.author} | {commit_info.date}")
        output.append(f"  {commit_info.message}")
        
        # Only add body if it's not empty and different from message
        if commit_info.body and commit_info.body.strip() and commit_info.body.strip() != commit_info.message.strip():
            # Compact body - remove extra newlines
            body_lines = [line.strip() for line in commit_info.body.split('\n') if line.strip()]
            if body_lines:
                output.append(f"  Body: {' '.join(body_lines)}")
        
        if mode == 'detailed' and commit_info.patch:
            output.append(commit_info.patch)
        elif mode == 'simple' and commit_info.files_changed:
            # Show all files with status (A/M/D/R)
            output.append("  Files:")
            for file_change in commit_info.files_changed:
                output.append(f"    {file_change}")
        
        output.append("-" * 20)
        
        return '\n'.join(output)
    
    def save_detailed_output(self, commit_hash: Optional[str] = None) -> str:
        """
        Save detailed analysis to {output_dir}/git_log_detailed.txt.
        
        Args:
            commit_hash: Specific commit to analyze (default: HEAD)
            
        Returns:
            Path to output file
        """
        if commit_hash is None:
            commit_hash = self.get_last_commit_hash()
        
        commit_info = self._analyze_commit(commit_hash, 'detailed')
        output = self.format_commit_output(commit_info, 'detailed')
        
        # Handle merge commits - include introduced commits
        if commit_info.is_merge:
            introduced_commits = self.get_commits_in_merge(commit_hash)
            if introduced_commits:
                output += "\n\nCommits introduced by this merge:\n"
                for commit in introduced_commits:
                    if commit != commit_hash:  # Don't duplicate the merge commit itself
                        intro_commit = self._analyze_commit(commit, 'detailed')
                        output += "\n" + self.format_commit_output(intro_commit, 'detailed')
        
        output += "\n" + "=" * 41 + "\n"
        
        output_file = self.output_dir / "git_log_detailed.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        return str(output_file)
    
    def save_simple_output(self, commit_hash: Optional[str] = None) -> str:
        """
        Save simple analysis to {output_dir}/git_log_simple.txt.
        
        Args:
            commit_hash: Specific commit to analyze (default: HEAD)
            
        Returns:
            Path to output file
        """
        if commit_hash is None:
            commit_hash = self.get_last_commit_hash()
        
        commit_info = self._analyze_commit(commit_hash, 'simple')
        output = self.format_commit_output(commit_info, 'simple')
        
        # Handle merge commits - include introduced commits
        if commit_info.is_merge:
            introduced_commits = self.get_commits_in_merge(commit_hash)
            if introduced_commits:
                output += "\n\nNew Commits Introduced by This Merge:\n\n"
                for commit in introduced_commits:
                    if commit != commit_hash:  # Don't duplicate the merge commit itself
                        intro_commit = self._analyze_commit(commit, 'simple')
                        output += "\n" + self.format_commit_output(intro_commit, 'simple')
        
        output += "\n" + "=" * 41 + "\n"
        
        output_file = self.output_dir / "git_log_simple.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        return str(output_file)


# Convenience functions for backward compatibility
def analyze_last_commit_detailed() -> str:
    """Analyze last commit in detailed mode and save to .tmp/git_log_detailed.txt."""
    analyzer = GitLogAnalyzer()
    return analyzer.save_detailed_output()


def analyze_last_commit_simple() -> str:
    """Analyze last commit in simple mode and save to .tmp/git_log_simple.txt."""
    analyzer = GitLogAnalyzer()
    return analyzer.save_simple_output()
