"""
Base path utility for handling different modes (development/production).

This module provides functionality to determine the correct base path depending
on whether the code is running in development or production mode.

Example usage:
    from utils.get_base_path import get_base_path

    # Development mode (running directly from codex)
    base = get_base_path("dev")  # Returns "."
    file_path = f"{base}/config.json"  # "./config.json"

    # Production mode (running from .codex in another repository)
    base = get_base_path("prod")  # Returns ".codex"
    file_path = f"{base}/config.json"  # ".codex/config.json"

The utility helps maintain consistent path resolution across different
execution contexts, ensuring files are accessed from the correct location
whether running in development or production mode.
"""

def get_base_path(mode: str = "prod") -> str:
    """
    Get the base path based on running mode.
    
    Args:
        mode (str): Running mode, either "prod" or "dev" (default: "prod")
            - "prod": Running from .codex in another repository
            - "dev": Running locally from codex repository
    
    Returns:
        str: Base path for file operations
            - Returns ".codex" for prod mode
            - Returns "." for dev mode
    
    Examples:
        >>> get_base_path("prod")
        '.codex'
        >>> get_base_path("dev")
        '.'
        >>> get_base_path()  # defaults to "prod"
        '.codex'
    """
    return ".codex" if mode == "prod" else "."
