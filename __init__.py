"""
Codex-AI: AI-powered development toolkit

A comprehensive toolkit for intelligent changelog generation
and code analysis using AI integration.

Features:
- 📝 Smart Changelogs: AI-generated from Git history
- 📚 Documentation: Auto-generate docs for React/Sass/Storybook
- 📊 Code Analysis: Project insights and metrics
- 🔧 Configuration: Flexible settings management

Usage:
    pip install codex-ai
    codex-ai changelog  # Generate AI-powered changelog
    codex-ai doc-ui     # Generate documentation
    codex-ai config     # Manage configuration
"""

from constants.project import (
    get_version, 
    get_author, 
    get_author_email, 
    get_description
)

__version__ = get_version()
__author__ = get_author()
__email__ = get_author_email()
__description__ = get_description()

# Package metadata
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__"
]
