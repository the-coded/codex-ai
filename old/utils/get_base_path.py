"""
Base path utility for handling different modes (development/production).

This module provides functionality to determine the correct base path by checking
if we're running from the project root (dev) or from .codex (prod).

Example usage:
    from utils.get_base_path import get_base_path

    # Will return "." if running from project root
    # Will return ".codex" if running from another project with .codex/
    base = get_base_path()
    file_path = f"{base}/config.json"

The utility helps maintain consistent path resolution across different
execution contexts by automatically detecting the environment.
"""

import os

def get_base_path() -> str:
    """
    Get the base path by checking the current environment.
    
    Returns:
        str: Base path for file operations
            - Returns ".codex" if running from another project with .codex/
            - Returns "." if running from project root
    
    Examples:
        >>> # When running from project root
        >>> get_base_path()
        '.'
        >>> # When running from another project with .codex/
        >>> get_base_path()
        '.codex'
    """
    # Check if we're in a directory that has .codex/
    if os.path.exists(".codex"):
        return ".codex"
    
    # Check if we're in the project root (has pkg/, utils/, etc.)
    if os.path.exists("pkg") and os.path.exists("utils"):
        return "."
    
    # If we're inside .codex, return .codex
    current_dir = os.getcwd()
    if "/.codex/" in current_dir or current_dir.endswith("/.codex"):
        return ".codex"
    
    # Default to "." if we can't determine
    return "."
