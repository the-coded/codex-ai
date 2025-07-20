"""
Git changes tracker for Codex-AI.

Provides tracking and analysis of Git repository changes, including file modifications,
additions, deletions, and repository state analysis for development workflows.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from enum import Enum
from datetime import datetime

from constants.git import EXCLUDE_PATTERNS, GIT_STATUS_COMMANDS, GIT_DIFF_COMMANDS


class ChangeType(Enum):
    """Enumeration of Git change types."""
    ADDED = "A"
    MODIFIED = "M"
    DELETED = "D"
    RENAMED = "R"
    COPIED = "C"
    UNMERGED = "U"
    UNTRACKED = "??"
    IGNORED = "!!"


class FileStatus(Enum):
    """Enumeration of Git file status."""
    STAGED = "staged"
    MODIFIED = "modified"
    UNTRACKED = "untracked"
    IGNORED = "ignored"
    CLEAN = "clean"


@dataclass
class FileChange:
    """Represents a single file change in Git."""
    path: str
    change_type: ChangeType
    status: FileStatus
    old_path: Optional[str] = None  # For renamed/copied files
    similarity: Optional[int] = None  # For renamed/copied files (0-100)
    
    @property
    def is_added(self) -> bool:
        """Check if file was added."""
        return self.change_type == ChangeType.ADDED
    
    @property
    def is_modified(self) -> bool:
        """Check if file was modified."""
        return self.change_type == ChangeType.MODIFIED
    
    @property
    def is_deleted(self) -> bool:
        """Check if file was deleted."""
        return self.change_type == ChangeType.DELETED
    
    @property
    def is_renamed(self) -> bool:
        """Check if file was renamed."""
        return self.change_type == ChangeType.RENAMED
    
    @property
    def is_staged(self) -> bool:
        """Check if change is staged."""
        return self.status == FileStatus.STAGED
    
    @property
    def is_untracked(self) -> bool:
        """Check if file is untracked."""
        return self.status == FileStatus.UNTRACKED


@dataclass
class RepositoryState:
    """Represents the current state of a Git repository."""
    staged_changes: List[FileChange]
    modified_changes: List[FileChange]
    untracked_files: List[FileChange]
    ignored_files: List[FileChange]
    clean: bool
    branch: Optional[str]
    commit_hash: Optional[str]
    ahead_behind: Optional[Tuple[int, int]]  # (ahead, behind) commits
    
    @property
    def has_changes(self) -> bool:
        """Check if repository has any changes."""
        return bool(self.staged_changes or self.modified_changes or self.untracked_files)
    
    @property
    def total_changes(self) -> int:
        """Get total number of changes."""
        return len(self.staged_changes) + len(self.modified_changes) + len(self.untracked_files)
    
    @property
    def is_dirty(self) -> bool:
        """Check if working directory is dirty."""
        return not self.clean


@dataclass
class CommitRange:
    """Represents a range of commits for comparison."""
    from_commit: str
    to_commit: str
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class ChangesTracker:
    """
    Tracks and analyzes Git repository changes.
    
    Provides comprehensive tracking of file changes, repository state,
    and change analysis for development workflows and automation.
    """
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize changes tracker.
        
        Args:
            repo_path: Path to Git repository (default: current directory)
        """
        self.repo_path = Path(repo_path)
        self.exclude_patterns = EXCLUDE_PATTERNS.copy()
    
    def get_repository_state(self) -> RepositoryState:
        """
        Get current repository state with all changes.
        
        Returns:
            RepositoryState object with current state
        """
        # Get staged changes
        staged_changes = self._get_staged_changes()
        
        # Get modified changes
        modified_changes = self._get_modified_changes()
        
        # Get untracked files
        untracked_files = self._get_untracked_files()
        
        # Get ignored files (optional)
        ignored_files = self._get_ignored_files()
        
        # Check if repository is clean
        clean = not (staged_changes or modified_changes or untracked_files)
        
        # Get branch information
        branch = self._get_current_branch()
        
        # Get commit hash
        commit_hash = self._get_current_commit()
        
        # Get ahead/behind information
        ahead_behind = self._get_ahead_behind()
        
        return RepositoryState(
            staged_changes=staged_changes,
            modified_changes=modified_changes,
            untracked_files=untracked_files,
            ignored_files=ignored_files,
            clean=clean,
            branch=branch,
            commit_hash=commit_hash,
            ahead_behind=ahead_behind
        )
    
    def get_changes_since_commit(self, commit: str) -> List[FileChange]:
        """
        Get changes since a specific commit.
        
        Args:
            commit: Commit hash or reference
            
        Returns:
            List of FileChange objects
        """
        try:
            # Get diff since commit
            result = self._run_git_command([
                "git", "diff", "--name-status", f"{commit}..HEAD"
            ])
            
            return self._parse_diff_output(result)
        
        except subprocess.CalledProcessError:
            return []
    
    def get_changes_between_commits(self, from_commit: str, to_commit: str) -> List[FileChange]:
        """
        Get changes between two commits.
        
        Args:
            from_commit: Starting commit
            to_commit: Ending commit
            
        Returns:
            List of FileChange objects
        """
        try:
            # Get diff between commits
            result = self._run_git_command([
                "git", "diff", "--name-status", f"{from_commit}..{to_commit}"
            ])
            
            return self._parse_diff_output(result)
        
        except subprocess.CalledProcessError:
            return []
    
    def get_changes_in_branch(self, branch: str, base_branch: str = "main") -> List[FileChange]:
        """
        Get changes in a branch compared to base branch.
        
        Args:
            branch: Branch to analyze
            base_branch: Base branch for comparison
            
        Returns:
            List of FileChange objects
        """
        try:
            # Get merge base
            merge_base = self._run_git_command([
                "git", "merge-base", base_branch, branch
            ]).strip()
            
            # Get changes since merge base
            return self.get_changes_since_commit(merge_base)
        
        except subprocess.CalledProcessError:
            return []
    
    def get_file_history(self, file_path: str, max_commits: int = 10) -> List[Dict[str, Any]]:
        """
        Get history of changes for a specific file.
        
        Args:
            file_path: Path to file
            max_commits: Maximum number of commits to retrieve
            
        Returns:
            List of commit information for the file
        """
        try:
            result = self._run_git_command([
                "git", "log", "--follow", "--oneline", f"-{max_commits}", "--", file_path
            ])
            
            history = []
            for line in result.strip().split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) >= 2:
                        history.append({
                            'commit': parts[0],
                            'message': parts[1],
                            'file': file_path
                        })
            
            return history
        
        except subprocess.CalledProcessError:
            return []
    
    def is_file_tracked(self, file_path: str) -> bool:
        """
        Check if a file is tracked by Git.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is tracked
        """
        try:
            result = subprocess.run(
                ["git", "ls-files", "--error-unmatch", file_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def is_file_ignored(self, file_path: str) -> bool:
        """
        Check if a file is ignored by Git.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is ignored
        """
        try:
            result = subprocess.run(
                ["git", "check-ignore", file_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            # git check-ignore returns 0 if file is ignored, 1 if not ignored
            return result.returncode == 0
        except Exception:
            return False
    
    def get_conflicted_files(self) -> List[str]:
        """
        Get list of files with merge conflicts.
        
        Returns:
            List of file paths with conflicts
        """
        try:
            result = self._run_git_command(["git", "diff", "--name-only", "--diff-filter=U"])
            return [line.strip() for line in result.split('\n') if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def _get_staged_changes(self) -> List[FileChange]:
        """Get staged changes."""
        try:
            result = self._run_git_command(["git", "diff", "--cached", "--name-status"])
            changes = self._parse_diff_output(result)
            
            # Mark as staged
            for change in changes:
                change.status = FileStatus.STAGED
            
            return changes
        except subprocess.CalledProcessError:
            return []
    
    def _get_modified_changes(self) -> List[FileChange]:
        """Get modified (unstaged) changes."""
        try:
            result = self._run_git_command(["git", "diff", "--name-status"])
            changes = self._parse_diff_output(result)
            
            # Mark as modified
            for change in changes:
                change.status = FileStatus.MODIFIED
            
            return changes
        except subprocess.CalledProcessError:
            return []
    
    def _get_untracked_files(self) -> List[FileChange]:
        """Get untracked files."""
        try:
            result = self._run_git_command(["git", "ls-files", "--others", "--exclude-standard"])
            files = [line.strip() for line in result.split('\n') if line.strip()]
            
            changes = []
            for file_path in files:
                if not self._is_excluded(file_path):
                    changes.append(FileChange(
                        path=file_path,
                        change_type=ChangeType.UNTRACKED,
                        status=FileStatus.UNTRACKED
                    ))
            
            return changes
        except subprocess.CalledProcessError:
            return []
    
    def _get_ignored_files(self) -> List[FileChange]:
        """Get ignored files."""
        try:
            result = self._run_git_command(["git", "ls-files", "--others", "--ignored", "--exclude-standard"])
            files = [line.strip() for line in result.split('\n') if line.strip()]
            
            changes = []
            for file_path in files:
                changes.append(FileChange(
                    path=file_path,
                    change_type=ChangeType.IGNORED,
                    status=FileStatus.IGNORED
                ))
            
            return changes
        except subprocess.CalledProcessError:
            return []
    
    def _get_current_branch(self) -> Optional[str]:
        """Get current branch name."""
        try:
            result = self._run_git_command(["git", "branch", "--show-current"])
            return result.strip() or None
        except subprocess.CalledProcessError:
            return None
    
    def _get_current_commit(self) -> Optional[str]:
        """Get current commit hash."""
        try:
            result = self._run_git_command(["git", "rev-parse", "HEAD"])
            return result.strip()
        except subprocess.CalledProcessError:
            return None
    
    def _get_ahead_behind(self) -> Optional[Tuple[int, int]]:
        """Get ahead/behind commit count."""
        try:
            # First check if we're in detached HEAD state
            branch = self._get_current_branch()
            if not branch:
                # In detached HEAD state, no upstream comparison possible
                return None
            
            # Check if upstream exists
            try:
                self._run_git_command(["git", "rev-parse", "@{upstream}"])
            except subprocess.CalledProcessError:
                # No upstream configured
                return None
            
            result = self._run_git_command(["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"])
            parts = result.strip().split('\t')
            if len(parts) == 2:
                ahead = int(parts[0])
                behind = int(parts[1])
                return (ahead, behind)
        except (subprocess.CalledProcessError, ValueError):
            pass
        return None
    
    def _parse_diff_output(self, output: str) -> List[FileChange]:
        """Parse git diff output into FileChange objects."""
        changes = []
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            
            status = parts[0]
            file_path = parts[1]
            
            # Handle renamed/copied files
            old_path = None
            similarity = None
            
            if status.startswith('R') or status.startswith('C'):
                # Extract similarity percentage
                if len(status) > 1:
                    try:
                        similarity = int(status[1:])
                    except ValueError:
                        similarity = None
                
                # Get old path
                if len(parts) > 2:
                    old_path = file_path
                    file_path = parts[2]
                
                change_type = ChangeType.RENAMED if status.startswith('R') else ChangeType.COPIED
            else:
                # Map status to change type
                change_type_map = {
                    'A': ChangeType.ADDED,
                    'M': ChangeType.MODIFIED,
                    'D': ChangeType.DELETED,
                    'U': ChangeType.UNMERGED,
                }
                change_type = change_type_map.get(status[0], ChangeType.MODIFIED)
            
            # Skip excluded files
            if self._is_excluded(file_path):
                continue
            
            changes.append(FileChange(
                path=file_path,
                change_type=change_type,
                status=FileStatus.CLEAN,  # Will be updated by caller
                old_path=old_path,
                similarity=similarity
            ))
        
        return changes
    
    def _is_excluded(self, file_path: str) -> bool:
        """Check if file should be excluded based on patterns."""
        for pattern in self.exclude_patterns:
            if pattern in file_path or file_path.endswith(pattern):
                return True
        return False
    
    def _run_git_command(self, command: List[str]) -> str:
        """Run a Git command and return output."""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")


class ChangeAnalyzer:
    """
    Analyzer for Git change patterns and statistics.
    
    Provides analysis of change patterns, file types, and development trends.
    """
    
    def __init__(self, repo_path: str = "."):
        """Initialize change analyzer."""
        self.tracker = ChangesTracker(repo_path)
    
    def analyze_repository_state(self) -> Dict[str, Any]:
        """
        Analyze current repository state.
        
        Returns:
            Dictionary with analysis results
        """
        state = self.tracker.get_repository_state()
        
        return {
            'total_changes': state.total_changes,
            'staged_count': len(state.staged_changes),
            'modified_count': len(state.modified_changes),
            'untracked_count': len(state.untracked_files),
            'is_clean': state.clean,
            'is_dirty': state.is_dirty,
            'branch': state.branch,
            'commit': state.commit_hash,
            'ahead_behind': state.ahead_behind,
            'file_types': self._analyze_file_types(state.staged_changes + state.modified_changes + state.untracked_files),
            'change_types': self._analyze_change_types(state.staged_changes + state.modified_changes),
        }
    
    def analyze_changes_since_commit(self, commit: str) -> Dict[str, Any]:
        """
        Analyze changes since a specific commit.
        
        Args:
            commit: Commit hash or reference
            
        Returns:
            Dictionary with analysis results
        """
        changes = self.tracker.get_changes_since_commit(commit)
        
        return {
            'total_changes': len(changes),
            'file_types': self._analyze_file_types(changes),
            'change_types': self._analyze_change_types(changes),
            'added_files': len([c for c in changes if c.is_added]),
            'modified_files': len([c for c in changes if c.is_modified]),
            'deleted_files': len([c for c in changes if c.is_deleted]),
            'renamed_files': len([c for c in changes if c.is_renamed]),
        }
    
    def _analyze_file_types(self, changes: List[FileChange]) -> Dict[str, int]:
        """Analyze distribution of file types in changes."""
        file_types = {}
        
        for change in changes:
            # Get file extension
            path = Path(change.path)
            extension = path.suffix.lower() if path.suffix else 'no-extension'
            
            file_types[extension] = file_types.get(extension, 0) + 1
        
        return file_types
    
    def _analyze_change_types(self, changes: List[FileChange]) -> Dict[str, int]:
        """Analyze distribution of change types."""
        change_types = {}
        
        for change in changes:
            change_type = change.change_type.value
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        return change_types


# Convenience functions
def get_repository_state(repo_path: str = ".") -> RepositoryState:
    """Get current repository state."""
    tracker = ChangesTracker(repo_path)
    return tracker.get_repository_state()


def get_changes_since_commit(commit: str, repo_path: str = ".") -> List[FileChange]:
    """Get changes since a specific commit."""
    tracker = ChangesTracker(repo_path)
    return tracker.get_changes_since_commit(commit)


def analyze_repository_changes(repo_path: str = ".") -> Dict[str, Any]:
    """Analyze current repository changes."""
    analyzer = ChangeAnalyzer(repo_path)
    return analyzer.analyze_repository_state()
