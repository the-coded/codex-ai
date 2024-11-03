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

import sys

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

def main():
    """
    Main function to demonstrate get_base_path usage.
    Called when running as a module: python -m utils.get_base_path
    """
    if len(sys.argv) > 2:
        print("❌ Error: Too many arguments")
        print("💡 Usage: python -m utils.get_base_path [mode]")
        sys.exit(1)

    mode = sys.argv[1] if len(sys.argv) == 2 else "prod"
    if mode not in ["dev", "prod"]:
        print("❌ Error: Mode must be 'dev' or 'prod'")
        sys.exit(1)

    base_path = get_base_path(mode)
    print(f"🔍 Base path for {mode} mode: {base_path}")
    print(f"💡 Example usage: {base_path}/config.json")

if __name__ == "__main__":
    main()
