"""
Prompt processor for Codex-AI.

Loads prompt templates from markdown files.
"""

import os
from pathlib import Path
try:
    # Python 3.9+
    from importlib.resources import files
except ImportError:
    # Python 3.7-3.8 compatibility
    from importlib_resources import files


def load_prompt(prompt_name: str) -> str:
    """
    Load prompt from markdown file.
    
    Args:
        prompt_name: Name of prompt file (without .md extension)
        
    Returns:
        Prompt content as string
    """
    try:
        # Use importlib.resources to get content from installed package
        template_files = files('templates.prompts')
        prompt_file = template_files / f"{prompt_name}.md"
        
        if prompt_file.is_file():
            return prompt_file.read_text(encoding='utf-8').strip()
        else:
            raise FileNotFoundError(f"Prompt file not found: {prompt_name}.md")
            
    except (ImportError, FileNotFoundError, AttributeError):
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


def get_doc_ui_prompt(doc_type: str) -> str:
    """Get doc-ui documentation prompt."""
    return load_prompt(f"doc_ui_{doc_type}_prompt")


def get_react_prompt() -> str:
    """Get React documentation prompt."""
    return load_prompt("doc_ui_react_prompt")


def get_sass_prompt() -> str:
    """Get Sass documentation prompt."""
    return load_prompt("doc_ui_sass_prompt")


def get_storybook_prompt() -> str:
    """Get Storybook documentation prompt."""
    return load_prompt("doc_ui_storybook_prompt")
