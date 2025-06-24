"""
Git tree generator for Codex-AI.

Ports the functionality from old/bin/tree_*.sh scripts to Python.
Generates JSON tree structures for project files, Git changes, and sibling files.
"""

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Union
from datetime import datetime

from constants.tree import (
    EXCLUDE_DIRECTORIES, TREE_OUTPUTS, GIT_CHANGE_TYPES, TREE_STRUCTURE,
    DEFAULT_CONFIG, is_excluded_directory, get_output_filename, 
    is_change_type, validate_file_path, split_file_path
)
from constants.git import EXCLUDE_PATTERNS


@dataclass
class TreeGenerationResult:
    """Represents the result of a tree generation operation."""
    tree_type: str
    output_file: str
    file_count: int
    success: bool
    error_message: Optional[str] = None
    generation_time: Optional[float] = None


class GitTreeGenerator:
    """
    Generates JSON tree structures from Git repositories.
    
    Provides Python equivalent of tree_*.sh scripts with improved error handling,
    structured data output, and unified API for all tree generation operations.
    """
    
    def __init__(self, repo_path: str = ".", output_dir: Optional[str] = None):
        """
        Initialize Git tree generator.
        
        Args:
            repo_path: Path to Git repository (default: current directory)
            output_dir: Output directory for generated files (default: .tmp)
        """
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir) if output_dir else self.repo_path / DEFAULT_CONFIG["output_directory"]
        self.config = DEFAULT_CONFIG.copy()
        
        # Ensure output directory exists
        if self.config["create_output_dir"]:
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
    
    def _is_git_repository(self) -> bool:
        """Check if current directory is a Git repository."""
        try:
            self._run_git_command(["git", "rev-parse", "--is-inside-work-tree"])
            return True
        except RuntimeError:
            return False
    
    def _save_tree_json(self, tree_data: Dict[str, Any], output_file: str) -> str:
        """
        Save tree data to JSON file.
        
        Args:
            tree_data: Tree structure to save
            output_file: Output filename
            
        Returns:
            Full path to saved file
        """
        output_path = self.output_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if self.config["pretty_print"]:
                json.dump(tree_data, f, indent=self.config["indent"], ensure_ascii=False)
            else:
                json.dump(tree_data, f, ensure_ascii=False)
        
        return str(output_path)
    
    def _build_tree_from_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Build a nested tree structure from a list of file paths.
        
        This implements the jq logic from the shell scripts in Python.
        
        Args:
            file_paths: List of file paths to organize into tree
            
        Returns:
            Nested dictionary representing the tree structure
        """
        tree = {}
        
        # Sort and deduplicate file paths
        unique_paths = sorted(set(file_paths))
        
        for filepath in unique_paths:
            if not validate_file_path(filepath):
                continue
            
            # Split path into directory parts and filename
            dir_parts, filename = split_file_path(filepath)
            
            # Navigate/create the nested structure
            current_level = tree
            
            # Create nested directories
            for dir_name in dir_parts:
                if dir_name not in current_level:
                    current_level[dir_name] = {}
                current_level = current_level[dir_name]
            
            # Add file to the files array
            files_key = TREE_STRUCTURE["root_files_key"]
            if files_key not in current_level:
                current_level[files_key] = []
            current_level[files_key].append(filename)
        
        # Sort all arrays if configured
        if self.config["sort_output"]:
            tree = self._sort_tree_arrays(tree)
        
        return tree
    
    def _sort_tree_arrays(self, tree: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively sort all arrays in the tree structure.
        
        Args:
            tree: Tree structure to sort
            
        Returns:
            Tree with sorted arrays
        """
        if isinstance(tree, dict):
            result = {}
            for key, value in tree.items():
                if key == TREE_STRUCTURE["root_files_key"] and isinstance(value, list):
                    result[key] = sorted(value)
                else:
                    result[key] = self._sort_tree_arrays(value)
            return result
        elif isinstance(tree, list):
            return sorted([self._sort_tree_arrays(item) for item in tree])
        else:
            return tree
    
    def generate_project_tree(self, start_path: Optional[str] = None) -> TreeGenerationResult:
        """
        Generate complete project tree structure.
        
        Equivalent to old/bin/tree_project.sh
        
        Args:
            start_path: Starting directory path (default: repo_path)
            
        Returns:
            TreeGenerationResult with generation details
        """
        start_time = datetime.now()
        
        try:
            if start_path is None:
                start_path = str(self.repo_path)
            
            start_path = Path(start_path).resolve()
            
            if not start_path.is_dir():
                return TreeGenerationResult(
                    tree_type="project",
                    output_file="",
                    file_count=0,
                    success=False,
                    error_message=f"Start path is not a valid directory: {start_path}"
                )
            
            # Generate tree structure recursively
            tree = self._generate_directory_tree(start_path, start_path)
            
            # Save to file
            output_file = get_output_filename("project")
            output_path = self._save_tree_json(tree, output_file)
            
            # Count total files
            file_count = self._count_files_in_tree(tree)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return TreeGenerationResult(
                tree_type="project",
                output_file=output_path,
                file_count=file_count,
                success=True,
                generation_time=generation_time
            )
            
        except Exception as e:
            return TreeGenerationResult(
                tree_type="project",
                output_file="",
                file_count=0,
                success=False,
                error_message=str(e)
            )
    
    def _generate_directory_tree(self, current_dir: Path, base_path: Path) -> Dict[str, Any]:
        """
        Recursively generate directory tree structure.
        
        Args:
            current_dir: Current directory being processed
            base_path: Base path for relative path calculation
            
        Returns:
            Dictionary representing directory structure
        """
        tree = {}
        
        try:
            # Get all items in current directory
            items = list(current_dir.iterdir())
            
            # Separate directories and files
            directories = []
            files = []
            
            for item in items:
                # Skip hidden files and excluded directories
                if item.name.startswith('.') and item.name not in ['.gitignore', '.env.example']:
                    continue
                
                if item.is_dir():
                    if not is_excluded_directory(item.name):
                        directories.append(item)
                elif item.is_file():
                    files.append(item)
            
            # Add subdirectories
            for directory in sorted(directories):
                tree[directory.name] = self._generate_directory_tree(directory, base_path)
            
            # Add files
            if files:
                tree[TREE_STRUCTURE["root_files_key"]] = sorted([f.name for f in files])
            
        except PermissionError:
            # Skip directories we can't read
            pass
        
        return tree
    
    def _count_files_in_tree(self, tree: Dict[str, Any]) -> int:
        """
        Count total number of files in a tree structure.
        
        Args:
            tree: Tree structure to count
            
        Returns:
            Total number of files
        """
        count = 0
        
        for key, value in tree.items():
            if key == TREE_STRUCTURE["root_files_key"] and isinstance(value, list):
                count += len(value)
            elif isinstance(value, dict):
                count += self._count_files_in_tree(value)
        
        return count
    
    def generate_git_changes_trees(self) -> List[TreeGenerationResult]:
        """
        Generate trees for Git changes (changed, removed, all).
        
        Equivalent to old/bin/tree_git_changes.sh
        
        Returns:
            List of TreeGenerationResult for each tree type
        """
        if not self._is_git_repository():
            error_result = TreeGenerationResult(
                tree_type="git_changes",
                output_file="",
                file_count=0,
                success=False,
                error_message="Not in a Git repository"
            )
            return [error_result]
        
        results = []
        
        try:
            # Get Git changes from last commit
            changed_files, removed_files = self._get_git_changes()
            
            # Generate changed files tree
            if changed_files:
                changed_tree = self._build_tree_from_files(changed_files)
                changed_output = self._save_tree_json(changed_tree, get_output_filename("git_changed"))
                results.append(TreeGenerationResult(
                    tree_type="git_changed",
                    output_file=changed_output,
                    file_count=len(changed_files),
                    success=True
                ))
            
            # Generate removed files tree
            if removed_files:
                removed_tree = self._build_tree_from_files(removed_files)
                removed_output = self._save_tree_json(removed_tree, get_output_filename("git_removed"))
                results.append(TreeGenerationResult(
                    tree_type="git_removed",
                    output_file=removed_output,
                    file_count=len(removed_files),
                    success=True
                ))
            
            # Generate combined tree
            all_files = changed_files + removed_files
            if all_files:
                all_tree = self._build_tree_from_files(all_files)
                all_output = self._save_tree_json(all_tree, get_output_filename("git_all"))
                results.append(TreeGenerationResult(
                    tree_type="git_all",
                    output_file=all_output,
                    file_count=len(all_files),
                    success=True
                ))
            
            # If no changes found
            if not results:
                results.append(TreeGenerationResult(
                    tree_type="git_changes",
                    output_file="",
                    file_count=0,
                    success=True,
                    error_message="No changes found in last commit"
                ))
            
        except Exception as e:
            results.append(TreeGenerationResult(
                tree_type="git_changes",
                output_file="",
                file_count=0,
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def _get_git_changes(self) -> tuple[List[str], List[str]]:
        """
        Get changed and removed files from last Git commit.
        
        Returns:
            Tuple of (changed_files, removed_files)
        """
        changed_files = []
        removed_files = []
        
        try:
            # Get changes from last commit
            git_output = self._run_git_command([
                "git", "show", "--name-status", "--format=", "HEAD"
            ])
            
            for line in git_output.split('\n'):
                if not line.strip():
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                status = parts[0]
                filepath = parts[1]
                
                # Handle renamed files (R100 old_path new_path)
                if len(parts) > 2 and status.startswith('R'):
                    filepath = parts[2]  # Use new path for renamed files
                
                # Categorize by status
                if is_change_type(status[0], "REMOVED"):
                    removed_files.append(filepath)
                elif is_change_type(status[0], "CHANGED"):
                    changed_files.append(filepath)
        
        except RuntimeError:
            pass  # No commits or other Git error
        
        return changed_files, removed_files
    
    def generate_release_changes_trees(self) -> List[TreeGenerationResult]:
        """
        Generate trees for release changes (changed, removed, all).
        
        Equivalent to old/bin/tree_git_release_changes.sh
        
        Returns:
            List of TreeGenerationResult for each tree type
        """
        if not self._is_git_repository():
            error_result = TreeGenerationResult(
                tree_type="release_changes",
                output_file="",
                file_count=0,
                success=False,
                error_message="Not in a Git repository"
            )
            return [error_result]
        
        results = []
        
        try:
            # Get current and previous tags
            current_tag, previous_ref = self._get_release_refs()
            
            if not current_tag:
                results.append(TreeGenerationResult(
                    tree_type="release_changes",
                    output_file="",
                    file_count=0,
                    success=True,
                    error_message="No tags/releases found in repository"
                ))
                return results
            
            # Get release changes
            changed_files, removed_files = self._get_release_changes(previous_ref, current_tag)
            
            # Generate trees similar to git changes, but only if we have changes
            if changed_files or removed_files:
                # Generate changed files tree
                if changed_files:
                    changed_tree = self._build_tree_from_files(changed_files)
                    changed_output = self._save_tree_json(changed_tree, get_output_filename("release_changed"))
                    results.append(TreeGenerationResult(
                        tree_type="release_changed",
                        output_file=changed_output,
                        file_count=len(changed_files),
                        success=True
                    ))
                else:
                    # Create empty file for consistency
                    empty_tree = {}
                    changed_output = self._save_tree_json(empty_tree, get_output_filename("release_changed"))
                    results.append(TreeGenerationResult(
                        tree_type="release_changed",
                        output_file=changed_output,
                        file_count=0,
                        success=True
                    ))
                
                # Generate removed files tree
                if removed_files:
                    removed_tree = self._build_tree_from_files(removed_files)
                    removed_output = self._save_tree_json(removed_tree, get_output_filename("release_removed"))
                    results.append(TreeGenerationResult(
                        tree_type="release_removed",
                        output_file=removed_output,
                        file_count=len(removed_files),
                        success=True
                    ))
                else:
                    # Create empty file for consistency
                    empty_tree = {}
                    removed_output = self._save_tree_json(empty_tree, get_output_filename("release_removed"))
                    results.append(TreeGenerationResult(
                        tree_type="release_removed",
                        output_file=removed_output,
                        file_count=0,
                        success=True
                    ))
                
                # Generate combined tree
                all_files = changed_files + removed_files
                if all_files:
                    all_tree = self._build_tree_from_files(all_files)
                    all_output = self._save_tree_json(all_tree, get_output_filename("release_all"))
                    results.append(TreeGenerationResult(
                        tree_type="release_all",
                        output_file=all_output,
                        file_count=len(all_files),
                        success=True
                    ))
            
            if not results:
                results.append(TreeGenerationResult(
                    tree_type="release_changes",
                    output_file="",
                    file_count=0,
                    success=True,
                    error_message="No changes found between releases"
                ))
        
        except Exception as e:
            results.append(TreeGenerationResult(
                tree_type="release_changes",
                output_file="",
                file_count=0,
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def _get_release_refs(self) -> tuple[Optional[str], Optional[str]]:
        """
        Get current and previous release references.
        
        Returns:
            Tuple of (current_tag, previous_ref)
        """
        try:
            # Get current tag
            current_tag = self._run_git_command(["git", "describe", "--tags", "--abbrev=0"])
            
            # Try to get previous tag
            try:
                previous_tag = self._run_git_command([
                    "git", "describe", "--tags", "--abbrev=0", f"{current_tag}^"
                ])
                return current_tag, previous_tag
            except RuntimeError:
                # This is the first release, use first commit
                first_commit = self._run_git_command(["git", "rev-list", "--max-parents=0", "HEAD"])
                return current_tag, first_commit
        
        except RuntimeError:
            return None, None
    
    def _get_release_changes(self, previous_ref: str, current_ref: str) -> tuple[List[str], List[str]]:
        """
        Get changed and removed files between releases.
        
        Args:
            previous_ref: Previous release reference
            current_ref: Current release reference
            
        Returns:
            Tuple of (changed_files, removed_files)
        """
        changed_files = []
        removed_files = []
        
        try:
            # Get changes between releases
            git_output = self._run_git_command([
                "git", "diff", "--name-status", f"{previous_ref}..{current_ref}"
            ])
            
            for line in git_output.split('\n'):
                if not line.strip():
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                status = parts[0]
                filepath = parts[1]
                
                # Handle renamed files
                if len(parts) > 2 and status.startswith('R'):
                    filepath = parts[2]  # Use new path
                
                # Apply the same filtering logic as the shell script:
                # For changed files, check if file exists (except for removed files)
                if is_change_type(status[0], "REMOVED"):
                    removed_files.append(filepath)
                elif is_change_type(status[0], "CHANGED"):
                    # Only include changed files that currently exist
                    file_path = self.repo_path / filepath
                    if file_path.exists():
                        changed_files.append(filepath)
        
        except RuntimeError:
            pass
        
        return changed_files, removed_files
    
    def generate_siblings_tree(self) -> TreeGenerationResult:
        """
        Generate tree of sibling files for changed files.
        
        Equivalent to old/bin/tree_git_siblings.sh
        
        Returns:
            TreeGenerationResult with generation details
        """
        start_time = datetime.now()
        
        try:
            # Check if required input files exist
            changed_file = self.output_dir / get_output_filename("git_changed")
            project_file = self.output_dir / get_output_filename("project")
            
            if not changed_file.exists() or not project_file.exists():
                return TreeGenerationResult(
                    tree_type="git_siblings",
                    output_file="",
                    file_count=0,
                    success=False,
                    error_message=f"Required input files not found: {changed_file}, {project_file}"
                )
            
            # Load input files
            with open(changed_file, 'r', encoding='utf-8') as f:
                changed_tree = json.load(f)
            
            with open(project_file, 'r', encoding='utf-8') as f:
                project_tree = json.load(f)
            
            # Generate siblings tree
            siblings_tree = self._build_siblings_tree(changed_tree, project_tree)
            
            # Save result
            output_file = get_output_filename("git_siblings")
            output_path = self._save_tree_json(siblings_tree, output_file)
            
            file_count = self._count_files_in_tree(siblings_tree)
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return TreeGenerationResult(
                tree_type="git_siblings",
                output_file=output_path,
                file_count=file_count,
                success=True,
                generation_time=generation_time
            )
            
        except Exception as e:
            return TreeGenerationResult(
                tree_type="git_siblings",
                output_file="",
                file_count=0,
                success=False,
                error_message=str(e)
            )
    
    def _build_siblings_tree(self, changed_tree: Dict[str, Any], project_tree: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build tree of sibling files based on changed files and project structure.
        
        For each directory that contains changed files, include ALL files from that directory.
        This helps identify related files that might be affected by changes.
        
        Args:
            changed_tree: Tree of changed files
            project_tree: Complete project tree
            
        Returns:
            Tree containing sibling files
        """
        siblings_tree = {}
        
        # Process each level of the changed tree
        self._extract_siblings_recursive(changed_tree, project_tree, siblings_tree)
        
        return siblings_tree
    
    def _extract_siblings_recursive(self, changed_node: Dict[str, Any], project_node: Dict[str, Any], 
                                  siblings_node: Dict[str, Any]):
        """
        Recursively extract sibling files from project tree based on changed files.
        
        Args:
            changed_node: Current node in changed tree
            project_node: Current node in project tree
            siblings_node: Current node in siblings tree being built
        """
        files_key = TREE_STRUCTURE["root_files_key"]
        
        # If there are files in this directory in the changed tree,
        # copy ALL files from the project tree (siblings)
        if files_key in changed_node and files_key in project_node:
            siblings_node[files_key] = project_node[files_key].copy()
        
        # Recursively process subdirectories that exist in both trees
        for key, value in changed_node.items():
            if key != files_key and isinstance(value, dict):
                if key in project_node and isinstance(project_node[key], dict):
                    if key not in siblings_node:
                        siblings_node[key] = {}
                    self._extract_siblings_recursive(
                        value, project_node[key], siblings_node[key]
                    )
    
    def generate_all_trees(self) -> List[TreeGenerationResult]:
        """
        Generate all tree structures.
        
        Equivalent to old/bin/tree_generate_all.sh
        
        Returns:
            List of TreeGenerationResult for all generated trees
        """
        all_results = []
        
        # Generate project tree
        project_result = self.generate_project_tree()
        all_results.append(project_result)
        
        # Generate git changes trees
        git_results = self.generate_git_changes_trees()
        all_results.extend(git_results)
        
        # Generate release changes trees
        release_results = self.generate_release_changes_trees()
        all_results.extend(release_results)
        
        # Generate siblings tree (only if git changes were successful)
        git_changed_success = any(r.success and r.tree_type == "git_changed" for r in git_results)
        if project_result.success and git_changed_success:
            siblings_result = self.generate_siblings_tree()
            all_results.append(siblings_result)
        
        return all_results
    
    def get_generation_summary(self, results: List[TreeGenerationResult]) -> Dict[str, Any]:
        """
        Generate a summary of tree generation results.
        
        Args:
            results: List of TreeGenerationResult objects
            
        Returns:
            Summary dictionary with statistics and file paths
        """
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        summary = {
            "total_trees": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_files": sum(r.file_count for r in successful),
            "output_directory": str(self.output_dir),
            "generated_files": {r.tree_type: r.output_file for r in successful if r.output_file},
            "errors": {r.tree_type: r.error_message for r in failed if r.error_message}
        }
        
        return summary


# Convenience functions for backward compatibility
def generate_project_tree(start_path: str = ".", output_file: str = ".tmp/tree_project.json") -> str:
    """Generate project tree and save to file."""
    generator = GitTreeGenerator()
    result = generator.generate_project_tree(start_path)
    return result.output_file if result.success else ""


def generate_git_changes_trees() -> List[str]:
    """Generate Git changes trees and return output file paths."""
    generator = GitTreeGenerator()
    results = generator.generate_git_changes_trees()
    return [r.output_file for r in results if r.success and r.output_file]


def generate_all_trees() -> List[str]:
    """Generate all trees and return output file paths."""
    generator = GitTreeGenerator()
    results = generator.generate_all_trees()
    return [r.output_file for r in results if r.success and r.output_file]
