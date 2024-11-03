"""
Shared utilities for the codex project.

Available modules:
    - require_aider: Install and verify aider-chat package
"""

# Import specific functions to expose at package level
from .require_aider import (
    is_package_installed,
    install_aider,
)

# Define what should be available when using 'from shared import *'
__all__ = [
    'is_package_installed',
    'install_aider',
]
