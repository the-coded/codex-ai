"""
Project metadata constants for Codex-AI.

Centralizes project information by reading from pyproject.toml as single source of truth.
"""

import sys
from pathlib import Path

# Import tomllib for Python 3.11+ or tomli for older versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "tomli is required for Python < 3.11. Install with: pip install tomli"
        )

# ===== PYPROJECT.TOML LOADER =====

def _load_pyproject_data():
    """
    Load project data from pyproject.toml.
    
    Returns:
        dict: Project configuration from pyproject.toml
        
    Raises:
        FileNotFoundError: If pyproject.toml is not found
        tomllib.TOMLDecodeError: If pyproject.toml is invalid
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")
    
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)

# Load data once on import
_PYPROJECT_DATA = _load_pyproject_data()
PROJECT_INFO = _PYPROJECT_DATA["project"]

# ===== SIMPLE GETTERS =====

def get_version():
    """Get project version from pyproject.toml."""
    return PROJECT_INFO["version"]

def get_name():
    """Get project name from pyproject.toml."""
    return PROJECT_INFO["name"]

def get_author():
    """Get project author from pyproject.toml."""
    return PROJECT_INFO["authors"][0]["name"]

def get_author_email():
    """Get project author email from pyproject.toml."""
    return PROJECT_INFO["authors"][0]["email"]

def get_description():
    """Get project description from pyproject.toml."""
    return PROJECT_INFO["description"]

def get_url():
    """Get project URL from pyproject.toml."""
    return PROJECT_INFO.get("urls", {}).get("Homepage", "")

# ===== EXPORT =====

__all__ = [
    "PROJECT_INFO", 
    "get_version", 
    "get_name", 
    "get_author",
    "get_author_email",
    "get_description", 
    "get_url"
]
