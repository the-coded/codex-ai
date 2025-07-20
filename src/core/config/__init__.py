"""
Configuration management for Codex-AI.

This module provides hierarchical configuration loading and management
for the Codex-AI toolkit.
"""

from .manager import CodexConfig, get_config, set_config

__all__ = [
    'CodexConfig',
    'get_config', 
    'set_config'
]
