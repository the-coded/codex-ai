"""
Output formatting constants for Codex-AI.

This module contains constants for output formatting, colors, emojis, and report
templates used throughout the Codex-AI system for consistent user experience.
"""

from typing import Dict, List, Any

# ===== OUTPUT FORMATS =====
#
# 📊 EXPLANATION:
# Supported output formats for different types of reports and data export.
# Each format has specific use cases and target audiences.

OUTPUT_FORMATS = {
    "JSON": {
        "extension": ".json",
        "mime_type": "application/json",
        "description": "Machine-readable JSON format",
        "use_cases": ["API responses", "data export", "pipeline integration"],
        "pretty": True
    },
    "YAML": {
        "extension": ".yaml",
        "mime_type": "application/x-yaml",
        "description": "Human-readable YAML format",
        "use_cases": ["configuration", "documentation", "CI/CD"],
        "pretty": True
    },
    "MARKDOWN": {
        "extension": ".md",
        "mime_type": "text/markdown",
        "description": "Markdown documentation format",
        "use_cases": ["documentation", "reports", "README files"],
        "pretty": True
    },
    "HTML": {
        "extension": ".html",
        "mime_type": "text/html",
        "description": "HTML web format",
        "use_cases": ["web reports", "dashboards", "presentations"],
        "pretty": True
    },
    "TEXT": {
        "extension": ".txt",
        "mime_type": "text/plain",
        "description": "Plain text format",
        "use_cases": ["logs", "simple reports", "terminal output"],
        "pretty": False
    },
    "CSV": {
        "extension": ".csv",
        "mime_type": "text/csv",
        "description": "Comma-separated values format",
        "use_cases": ["data analysis", "spreadsheets", "exports"],
        "pretty": False
    }
}

# ===== EMOJIS =====
#
# 📊 EXPLANATION:
# Standardized emojis used throughout the system for consistent visual feedback.
# Based on emojis already used in the existing codebase.

EMOJIS = {
    # Status indicators
    "SUCCESS": "✅",
    "ERROR": "❌", 
    "WARNING": "⚠️",
    "INFO": "ℹ️",
    "QUESTION": "❓",
    
    # Actions
    "PROCESSING": "⚙️",
    "GENERATING": "🔄",
    "ANALYZING": "🔍",
    "BUILDING": "🏗️",
    "CLEANING": "🗑️",
    "SAVING": "💾",
    "LOADING": "📂",
    
    # Content types
    "FILE": "📄",
    "FOLDER": "📁",
    "CODE": "💻",
    "DOCS": "📚",
    "CONFIG": "⚙️",
    "LOG": "📝",
    "REPORT": "📊",
    "CHANGELOG": "📋",
    
    # Git operations
    "GIT": "🔀",
    "COMMIT": "📝",
    "BRANCH": "🌿",
    "MERGE": "🔀",
    "TAG": "🏷️",
    "RELEASE": "📦",
    
    # AI operations
    "AI": "🤖",
    "BRAIN": "🧠",
    "MAGIC": "✨",
    "ROCKET": "🚀",
    "TARGET": "🎯",
    "TROPHY": "🏆",
    
    # Time tracking
    "CLOCK": "🕐",
    "TIMER": "⏱️",
    "CALENDAR": "📅",
    "STOPWATCH": "⏰",
    
    # Progress indicators
    "PROGRESS": "📈",
    "COMPLETE": "🎉",
    "PARTIAL": "🔄",
    "PENDING": "⏳",
    "BLOCKED": "🚫"
}

# ===== COLORS =====
#
# 📊 EXPLANATION:
# ANSI color codes for terminal output formatting.
# Provides consistent color scheme across the application.

COLORS = {
    # Basic colors
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "UNDERLINE": "\033[4m",
    
    # Foreground colors
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    
    # Bright foreground colors
    "BRIGHT_BLACK": "\033[90m",
    "BRIGHT_RED": "\033[91m",
    "BRIGHT_GREEN": "\033[92m",
    "BRIGHT_YELLOW": "\033[93m",
    "BRIGHT_BLUE": "\033[94m",
    "BRIGHT_MAGENTA": "\033[95m",
    "BRIGHT_CYAN": "\033[96m",
    "BRIGHT_WHITE": "\033[97m",
    
    # Background colors
    "BG_BLACK": "\033[40m",
    "BG_RED": "\033[41m",
    "BG_GREEN": "\033[42m",
    "BG_YELLOW": "\033[43m",
    "BG_BLUE": "\033[44m",
    "BG_MAGENTA": "\033[45m",
    "BG_CYAN": "\033[46m",
    "BG_WHITE": "\033[47m"
}

# ===== SEMANTIC COLORS =====
#
# 📊 EXPLANATION:
# Semantic color mappings for different types of messages and status.

SEMANTIC_COLORS = {
    "SUCCESS": COLORS["BRIGHT_GREEN"],
    "ERROR": COLORS["BRIGHT_RED"],
    "WARNING": COLORS["BRIGHT_YELLOW"],
    "INFO": COLORS["BRIGHT_BLUE"],
    "DEBUG": COLORS["BRIGHT_MAGENTA"],
    "MUTED": COLORS["DIM"],
    "HIGHLIGHT": COLORS["BRIGHT_CYAN"],
    "EMPHASIS": COLORS["BOLD"],
    "HEADER": COLORS["BOLD"] + COLORS["BRIGHT_WHITE"],
    "SUBHEADER": COLORS["BRIGHT_CYAN"],
    "CODE": COLORS["BRIGHT_MAGENTA"],
    "PATH": COLORS["BRIGHT_BLUE"],
    "NUMBER": COLORS["BRIGHT_YELLOW"],
    "TIMESTAMP": COLORS["BRIGHT_BLACK"]
}

# ===== REPORT TEMPLATES =====
#
# 📊 EXPLANATION:
# Standard templates for different types of reports and outputs.

REPORT_TEMPLATES = {
    "CHANGELOG": {
        "header": "# {title}\n\n## {version} - {date}\n\n",
        "section": "### {section_title}\n\n{content}\n\n",
        "item": "- {emoji} **{type}**: {description}\n",
        "footer": "\n---\n\n*Generated by Codex-AI on {timestamp}*\n"
    },
    
    "ANALYSIS": {
        "header": "# {title}\n\n🔍 **Analysis Report**\n\n",
        "overview": "## Overview\n\n{overview_content}\n\n",
        "metrics": "## Metrics\n\n{metrics_content}\n\n",
        "details": "## Detailed Analysis\n\n{details_content}\n\n",
        "recommendations": "## Recommendations\n\n{recommendations_content}\n\n",
        "footer": "\n---\n\n*Generated by Codex-AI Analyzer on {timestamp}*\n"
    },
    
    "DOCS": {
        "header": "# {title}\n\n{description}\n\n",
        "toc": "## Table of Contents\n\n{toc_content}\n\n",
        "section": "## {section_title}\n\n{content}\n\n",
        "code_block": "```{language}\n{code}\n```\n\n",
        "footer": "\n---\n\n*Documentation generated by Codex-AI on {timestamp}*\n"
    },
    
    "ERROR": {
        "header": "# ❌ Error Report\n\n",
        "error_info": "**Error**: {error_type}\n**Message**: {error_message}\n**Timestamp**: {timestamp}\n\n",
        "context": "## Context\n\n{context_info}\n\n",
        "stack_trace": "## Stack Trace\n\n```\n{stack_trace}\n```\n\n",
        "suggestions": "## Suggestions\n\n{suggestions}\n\n"
    }
}

# ===== PROGRESS INDICATORS =====
#
# 📊 EXPLANATION:
# Characters and patterns for progress indicators and status displays.

PROGRESS_INDICATORS = {
    "SPINNER": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "DOTS": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
    "BARS": ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
    "ARROWS": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
    "BLOCKS": ["▖", "▘", "▝", "▗"],
    "BRAILLE": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
}

# ===== HELPER FUNCTIONS =====

def colorize(text: str, color: str) -> str:
    """
    Apply color to text for terminal output.
    
    Args:
        text: Text to colorize
        color: Color name from COLORS or SEMANTIC_COLORS
        
    Returns:
        str: Colorized text with reset at the end
        
    Examples:
        >>> print(colorize("Success!", "SUCCESS"))
        >>> print(colorize("Error occurred", "ERROR"))
    """
    if color in SEMANTIC_COLORS:
        color_code = SEMANTIC_COLORS[color]
    elif color in COLORS:
        color_code = COLORS[color]
    else:
        return text  # Return unchanged if color not found
    
    return f"{color_code}{text}{COLORS['RESET']}"


def format_with_emoji(text: str, emoji_name: str) -> str:
    """
    Format text with emoji prefix.
    
    Args:
        text: Text to format
        emoji_name: Emoji name from EMOJIS
        
    Returns:
        str: Text with emoji prefix
        
    Examples:
        >>> format_with_emoji("Task completed", "SUCCESS")
        "✅ Task completed"
    """
    emoji = EMOJIS.get(emoji_name, "")
    return f"{emoji} {text}" if emoji else text


def get_output_extension(format_name: str) -> str:
    """
    Get file extension for output format.
    
    Args:
        format_name: Format name from OUTPUT_FORMATS
        
    Returns:
        str: File extension including dot
        
    Examples:
        >>> get_output_extension("JSON")
        ".json"
    """
    format_info = OUTPUT_FORMATS.get(format_name.upper())
    return format_info["extension"] if format_info else ".txt"


def build_report(template_name: str, **kwargs) -> str:
    """
    Build a report using a template.
    
    Args:
        template_name: Template name from REPORT_TEMPLATES
        **kwargs: Template variables
        
    Returns:
        str: Formatted report
        
    Examples:
        >>> report = build_report("CHANGELOG", 
        ...                      title="My Project", 
        ...                      version="1.0.0", 
        ...                      date="2024-01-01")
    """
    template = REPORT_TEMPLATES.get(template_name.upper())
    if not template:
        return f"Template '{template_name}' not found"
    
    # Build report by combining template parts
    report_parts = []
    
    # Add header if present
    if "header" in template and "title" in kwargs:
        report_parts.append(template["header"].format(**kwargs))
    
    # Add main content sections
    for key, value in template.items():
        if key not in ["header", "footer"] and key in kwargs:
            report_parts.append(value.format(**kwargs))
    
    # Add footer if present
    if "footer" in template:
        import datetime
        kwargs.setdefault("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report_parts.append(template["footer"].format(**kwargs))
    
    return "".join(report_parts)


def format_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a progress bar string.
    
    Args:
        current: Current progress value
        total: Total/maximum value
        width: Width of progress bar in characters
        
    Returns:
        str: Formatted progress bar
        
    Examples:
        >>> print(format_progress_bar(30, 100))
        [███████████████               ] 30%
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    percentage = min(100, (current * 100) // total)
    filled = (current * width) // total
    bar = "█" * filled + " " * (width - filled)
    
    return f"[{bar}] {percentage}%"


def strip_colors(text: str) -> str:
    """
    Remove ANSI color codes from text.
    
    Args:
        text: Text with potential color codes
        
    Returns:
        str: Text without color codes
        
    Examples:
        >>> clean_text = strip_colors(colorize("Hello", "RED"))
        >>> print(clean_text)
        Hello
    """
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


# ===== VALIDATION CONSTANTS =====

VALID_OUTPUT_FORMATS = list(OUTPUT_FORMATS.keys())

# ===== EXPORT CONSTANTS =====

__all__ = [
    # Main constants
    "OUTPUT_FORMATS",
    "EMOJIS",
    "COLORS",
    "SEMANTIC_COLORS",
    "REPORT_TEMPLATES",
    "PROGRESS_INDICATORS",
    
    # Helper functions
    "colorize",
    "format_with_emoji",
    "get_output_extension",
    "build_report",
    "format_progress_bar",
    "strip_colors",
    
    # Validation constants
    "VALID_OUTPUT_FORMATS"
]
