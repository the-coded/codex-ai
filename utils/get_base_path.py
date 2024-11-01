"""
Get base path utility for handling different modes (development/production).
"""

def get_base_path(mode: str = "prod") -> str:
    """
    Get the base path based on running mode.
    
    Args:
        mode (str): Running mode, either "prod" or "dev" (default: "prod")
            - "prod": Running from .nexus in another repository
            - "dev": Running locally from codex-ai repository
    
    Returns:
        str: Base path for file operations
    """
    return ".nexus" if mode == "prod" else "."