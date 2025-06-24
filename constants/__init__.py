"""
Constants package for Codex-AI.

This package contains all constants used throughout the Codex-AI system,
organized by functionality and purpose.

Available modules:
- timetrack: Time tracking constants and multipliers
- git: Git operations and conventional commit types
- files: File categories and language mappings
- ai: AI models and token strategies
- output: Output formats and styling
"""

# Import main constants for easy access
from .timetrack import (
    FILE_TYPE_MULTIPLIERS,
    COMMIT_TYPE_MULTIPLIERS,
    COMPLEXITY_THRESHOLDS,
    STRUCTURAL_PATTERNS,
    ALGORITHMIC_PATTERNS,
    PLANNING_BASE,
    DELETION_TIME_FACTOR
)

from .git import (
    CONVENTIONAL_COMMIT_TYPES,
    EXCLUDE_PATTERNS,
    GIT_COMMANDS,
    GIT_STATUS_COMMANDS,
    GIT_DIFF_COMMANDS,
    build_exclude_pathspec
)

# Version info from centralized project metadata
from .project import get_version, get_author

__version__ = get_version()
__author__ = get_author()

# Export commonly used constants
__all__ = [
    # Timetrack constants
    "FILE_TYPE_MULTIPLIERS",
    "COMMIT_TYPE_MULTIPLIERS", 
    "COMPLEXITY_THRESHOLDS",
    "STRUCTURAL_PATTERNS",
    "ALGORITHMIC_PATTERNS",
    "PLANNING_BASE",
    "DELETION_TIME_FACTOR",
    
    # Git constants
    "CONVENTIONAL_COMMIT_TYPES",
    "EXCLUDE_PATTERNS",
    "GIT_COMMANDS", 
    "GIT_STATUS_COMMANDS",
    "GIT_DIFF_COMMANDS",
    "build_exclude_pathspec",
    
    # Package info
    "__version__",
    "__author__"
]
