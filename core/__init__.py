"""
Core functionality for Codex-AI.

This module provides the main business logic and processing capabilities
for all Codex-AI operations including git analysis, AI integration,
and documentation generation.
"""

# ===== GIT OPERATIONS =====
#
# 📊 EXPLANATION:
# Git-related functionality for analyzing repositories, commits, and changes.
# Ports shell scripts from old/bin/ to Python classes.

try:
    from .git import (
        GitLogAnalyzer,
        GitReleaseAnalyzer,
        GitTreeGenerator,
        CommitParser,
        ChangesTracker
    )
    GIT_AVAILABLE = True
except ImportError:
    # Git modules not yet implemented
    GIT_AVAILABLE = False
    GitLogAnalyzer = None
    GitReleaseAnalyzer = None
    GitTreeGenerator = None
    CommitParser = None
    ChangesTracker = None

# ===== AI OPERATIONS =====
#
# 📊 EXPLANATION:
# AI model integration, token management, and Aider interface.
# Handles model selection, prompt processing, and AI command generation.

try:
    from .ai import (
        ModelSelector,
        AiderInterface,
        TokenManager,
        PromptProcessor
    )
    AI_AVAILABLE = True
except ImportError:
    # AI modules not yet implemented
    AI_AVAILABLE = False
    ModelSelector = None
    AiderInterface = None
    TokenManager = None
    PromptProcessor = None

# ===== DOC-UI DOCUMENTATION =====
#
# 📊 EXPLANATION:
# Documentation generation for React, Sass, and Storybook files.
# Implemented in commands/doc_ui.py following the same pattern as other commands.

# Doc-UI functionality is implemented in commands/doc_ui.py
# No separate core module needed - follows same pattern as other commands
DOC_UI_AVAILABLE = True
ReactProcessor = None
SassProcessor = None
StorybookProcessor = None
DocumentationGenerator = None
SourceManager = None

# ===== AVAILABILITY STATUS =====
#
# 📊 EXPLANATION:
# Track which core modules are available for runtime checks.

CORE_STATUS = {
    "git": GIT_AVAILABLE,
    "ai": AI_AVAILABLE,
    "doc-ui": DOC_UI_AVAILABLE
}

# ===== HELPER FUNCTIONS =====

def get_available_modules() -> list:
    """
    Get list of available core modules.
    
    Returns:
        list: Names of available modules
        
    Examples:
        >>> modules = get_available_modules()
        >>> print(modules)
        ['git', 'ai']
    """
    return [name for name, available in CORE_STATUS.items() if available]


def is_module_available(module_name: str) -> bool:
    """
    Check if a core module is available.
    
    Args:
        module_name: Name of the module to check
        
    Returns:
        bool: True if module is available
        
    Examples:
        >>> if is_module_available('git'):
        ...     analyzer = GitLogAnalyzer()
    """
    return CORE_STATUS.get(module_name, False)


def get_core_status() -> dict:
    """
    Get complete status of all core modules.
    
    Returns:
        dict: Status of each core module
        
    Examples:
        >>> status = get_core_status()
        >>> print(status)
        {'git': True, 'ai': False, 'doc-ui': True}
    """
    return CORE_STATUS.copy()


def require_module(module_name: str) -> None:
    """
    Require a module to be available, raise error if not.
    
    Args:
        module_name: Name of the required module
        
    Raises:
        ImportError: If module is not available
        
    Examples:
        >>> require_module('git')  # Raises if git not available
    """
    if not is_module_available(module_name):
        raise ImportError(
            f"Core module '{module_name}' is not available. "
            f"Available modules: {get_available_modules()}"
        )

# ===== EXPORT CONSTANTS =====

__all__ = [
    # Git operations
    "GitLogAnalyzer",
    "GitReleaseAnalyzer", 
    "GitTreeGenerator",
    "CommitParser",
    "ChangesTracker",
    
    # AI operations
    "ModelSelector",
    "AiderInterface",
    "TokenManager", 
    "PromptProcessor",
    
    
    # Doc-UI documentation
    "ReactProcessor",
    "SassProcessor",
    "StorybookProcessor",
    "DocumentationGenerator",
    "SourceManager",
    
    # Status and utilities
    "CORE_STATUS",
    "get_available_modules",
    "is_module_available", 
    "get_core_status",
    "require_module",
    
    # Availability flags
    "GIT_AVAILABLE",
    "AI_AVAILABLE",
    "DOC_UI_AVAILABLE"
]

# ===== VERSION INFO =====

from constants.project import get_version, get_author

__version__ = get_version()
__author__ = get_author()
__description__ = "Core functionality for Codex-AI toolkit"

# ===== INITIALIZATION =====

def _initialize_core():
    """Initialize core modules and perform startup checks."""
    available = get_available_modules()
    
    if not available:
        import warnings
        warnings.warn(
            "No core modules are available. "
            "This may indicate incomplete installation.",
            RuntimeWarning
        )
    
    return available

# Initialize on import
_AVAILABLE_MODULES = _initialize_core()
