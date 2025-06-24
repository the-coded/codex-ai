"""
Prompt processor for Codex-AI.

Loads prompt templates from markdown files.
"""

import os
from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """
    Load prompt from markdown file.
    
    Args:
        prompt_name: Name of prompt file (without .md extension)
        
    Returns:
        Prompt content as string
    """
    prompt_file = Path("templates/prompts") / f"{prompt_name}.md"
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback to basic prompt if file doesn't exist
        return f"Process the provided data for {prompt_name} task."


def get_changelog_prompt() -> str:
    """Get changelog generation prompt."""
    return load_prompt("changelog_prompt")


def get_uidocs_prompt(doc_type: str) -> str:
    """Get uidocs documentation prompt."""
    return load_prompt(f"uidocs_{doc_type}_prompt")
