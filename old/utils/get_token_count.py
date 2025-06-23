"""
Token count utility.

This module provides functionality to count tokens in a file,
where tokens are calculated as characters divided by 4.
"""

import subprocess

def get_token_count(file_path: str) -> int:
    """
    Get the token count of a file (character count divided by 4).
    
    Args:
        file_path (str): Path to the file to count tokens
    
    Returns:
        int: Number of tokens in the file (char count / 4)
    
    Example:
        >>> get_token_count("file.txt")
        1000  # if file has 4000 characters
    """
    try:
        result = subprocess.run(
            f"wc -m < {file_path}",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        char_count = int(result.stdout.strip())
        return char_count // 4
    except (subprocess.CalledProcessError, ValueError):
        return 0
