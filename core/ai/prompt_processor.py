"""
Prompt processor for Codex-AI.

Loads prompt templates from markdown files.
"""

import os
import pkg_resources
from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """
    Load prompt from markdown file.
    
    Args:
        prompt_name: Name of prompt file (without .md extension)
        
    Returns:
        Prompt content as string
    """
    try:
        # Use pkg_resources to get absolute path from installed package
        prompt_path = pkg_resources.resource_filename(
            'codex_ai', 
            f'templates/prompts/{prompt_name}.md'
        )
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except (FileNotFoundError, pkg_resources.DistributionNotFound, ModuleNotFoundError):
        # Fallback: try relative path (for development mode)
        try:
            prompt_file = Path("templates/prompts") / f"{prompt_name}.md"
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback: try absolute path based on this file location
            try:
                # Get the directory where this Python file is located
                current_dir = Path(__file__).parent
                # Go up to project root (../../ from core/ai/)
                project_root = current_dir.parent.parent
                prompt_file = project_root / "templates/prompts" / f"{prompt_name}.md"
                
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except FileNotFoundError:
                # Final fallback to basic prompt if file doesn't exist
                return f"Process the provided data for {prompt_name} task."


def get_changelog_prompt() -> str:
    """Get changelog generation prompt."""
    return load_prompt("changelog_prompt")


def get_uidocs_prompt(doc_type: str) -> str:
    """Get uidocs documentation prompt."""
    return load_prompt(f"uidocs_{doc_type}_prompt")
