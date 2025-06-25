"""
Base path utility for handling different execution contexts.

This module provides functionality to determine the correct base path by checking
the current execution environment and project structure.

The utility helps maintain consistent path resolution across different
execution contexts by automatically detecting the environment.

NOTE: After publishing codex-ai to PyPI, the .codex directory pattern may become
obsolete since users will install via `pip install codex-ai` instead of cloning
the repository. This module should be reviewed for deprecation in future versions.
"""

import os
from pathlib import Path
from typing import Optional


def get_base_path() -> str:
    """
    Get the base path by checking the current environment.
    
    This function detects the execution context and returns the appropriate
    base path for file operations. It handles multiple scenarios:
    
    1. Running from project root (development)
    2. Running from .codex directory (pipeline/CI)
    3. Running from another project with .codex/ (external usage)
    
    Returns:
        str: Base path for file operations
            - Returns "." if running from project root
            - Returns ".codex" if running from another project with .codex/
            - Returns current directory if inside .codex
    
    Examples:
        >>> # When running from project root (development)
        >>> get_base_path()
        '.'
        
        >>> # When running from another project with .codex/ (pipeline)
        >>> get_base_path()
        '.codex'
        
        >>> # When running from inside .codex directory
        >>> get_base_path()
        '.'
    """
    current_path = Path.cwd()
    
    # Check if we're inside a .codex directory
    if current_path.name == ".codex" or ".codex" in current_path.parts:
        return "."
    
    # Check if we're in a directory that has .codex/ (external project)
    codex_path = current_path / ".codex"
    if codex_path.exists() and codex_path.is_dir():
        return ".codex"
    
    # Check if we're in the project root (has core/, utils/, etc.)
    project_indicators = ["core", "utils", "commands", "constants"]
    if all((current_path / indicator).exists() for indicator in project_indicators):
        return "."
    
    # Legacy check for old structure (pkg/, utils/)
    legacy_indicators = ["pkg", "utils"]
    if all((current_path / indicator).exists() for indicator in legacy_indicators):
        return "."
    
    # Default to current directory
    return "."


def get_project_root() -> Path:
    """
    Get the project root directory as a Path object.
    
    Returns:
        Path: Project root directory path
    
    Examples:
        >>> root = get_project_root()
        >>> config_file = root / "config.yaml"
    """
    base_path = get_base_path()
    return Path(base_path).resolve()


def resolve_path(relative_path: str) -> Path:
    """
    Resolve a relative path from the project base.
    
    Args:
        relative_path: Path relative to project base
        
    Returns:
        Path: Resolved absolute path
        
    Examples:
        >>> # Resolve config file path
        >>> config_path = resolve_path("config/settings.yaml")
        
        >>> # Resolve template path
        >>> template_path = resolve_path("templates/changelog.md")
    """
    base = get_project_root()
    return base / relative_path


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
        
    Returns:
        Path: The directory path
        
    Examples:
        >>> # Ensure output directory exists
        >>> output_dir = ensure_directory(".tmp")
        
        >>> # Ensure nested directory exists
        >>> docs_dir = ensure_directory("docs/generated")
    """
    dir_path = resolve_path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_output_path(filename: str, output_dir: str = ".tmp") -> Path:
    """
    Get a standardized output file path.
    
    Args:
        filename: Name of the output file
        output_dir: Output directory (default: .tmp)
        
    Returns:
        Path: Full path to output file
        
    Examples:
        >>> # Get path for changelog output
        >>> changelog_path = get_output_path("changelog.md")
        
        >>> # Get path for custom output directory
        >>> report_path = get_output_path("report.json", "reports")
    """
    output_directory = ensure_directory(output_dir)
    return output_directory / filename


def is_development_mode() -> bool:
    """
    Check if running in development mode.
    
    Development mode is detected by:
    1. Running from project root
    2. Presence of development files (.git, pyproject.toml, etc.)
    
    Returns:
        bool: True if in development mode
        
    Examples:
        >>> if is_development_mode():
        ...     print("Running in development mode")
    """
    base_path = get_project_root()
    
    # Check for development indicators
    dev_indicators = [".git", "pyproject.toml", "setup.py", "requirements-dev.txt"]
    return any((base_path / indicator).exists() for indicator in dev_indicators)


def is_pipeline_mode() -> bool:
    """
    Check if running in pipeline/CI mode.
    
    Pipeline mode is detected by:
    1. Running from .codex directory
    2. Environment variables indicating CI
    
    Returns:
        bool: True if in pipeline mode
        
    Examples:
        >>> if is_pipeline_mode():
        ...     print("Running in pipeline mode")
    """
    # Check if we're in .codex context
    if get_base_path() == ".codex":
        return True
    
    # Check for CI environment variables
    ci_indicators = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"]
    return any(os.getenv(indicator) for indicator in ci_indicators)


def find_file_in_hierarchy(filename: str, start_path: Optional[str] = None) -> Optional[Path]:
    """
    Find a file by searching up the directory hierarchy.
    
    Args:
        filename: Name of file to find
        start_path: Starting directory (default: current directory)
        
    Returns:
        Path: Path to found file, or None if not found
        
    Examples:
        >>> # Find .env file
        >>> env_file = find_file_in_hierarchy(".env")
    """
    if start_path:
        current = Path(start_path).resolve()
    else:
        current = Path.cwd()
    
    # Search up the hierarchy
    while current != current.parent:
        target_file = current / filename
        if target_file.exists():
            return target_file
        current = current.parent
    
    return None


# Legacy compatibility
def get_base_path_legacy() -> str:
    """
    Legacy function for backward compatibility.
    
    Returns:
        str: Base path as string (same as get_base_path())
    """
    return get_base_path()


# Export main functions
__all__ = [
    "get_base_path",
    "get_project_root", 
    "resolve_path",
    "ensure_directory",
    "get_output_path",
    "is_development_mode",
    "is_pipeline_mode",
    "find_file_in_hierarchy",
    "get_base_path_legacy"
]
