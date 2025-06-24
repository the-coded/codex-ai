"""
AI model constants and configuration for Codex-AI.

This module contains AI model definitions, token strategies, and Aider defaults
for automated code generation and documentation processing.
"""

from typing import Dict, List, Optional, Any

# ===== AI MODELS =====
#
# 📊 EXPLANATION:
# Anthropic Claude models with fallback strategy based on token requirements.
# Priority 1 = first choice, higher numbers = fallback options.

AI_MODELS = {
    "CLAUDE_4_SONNET": {
        "name": "anthropic/claude-4-sonnet-20250514",
        "max_tokens": 200000,   # 200K context window (confirmed by Anthropic docs)
        "priority": 1           # Default choice
    },
    "CLAUDE_3_7_SONNET": {
        "name": "anthropic/claude-3-7-sonnet-latest", 
        "max_tokens": 200000,   # 200K context window (confirmed by Anthropic docs)
        "priority": 2           # Fallback only
    }
}

# ===== TOKEN STRATEGY =====
#
# 📊 EXPLANATION:
# Token management strategy for automatic model selection and fallback.
# Based on the old changelog system but now dynamic per model.

TOKEN_STRATEGY = {
    "SAFETY_MARGIN": 0.95,        # Use 95% of model's max_tokens as limit
    "AUTO_MODEL_SELECTION": True,  # Automatically select model by token count
    "SIMPLE_LOG_FALLBACK": True    # Fall back to simple logs if detailed too large
}

# ===== AIDER DEFAULTS =====
#
# 📊 EXPLANATION:
# Standard Aider flags based on the old system usage patterns.
# Designed for non-interactive, automated execution.

AIDER_BASE_FLAGS = [
    "--subtree-only",     # Only consider files in current git subtree
    "--yes",              # Always say yes to confirmations (non-interactive)
    "--cache-prompts",    # Enable prompt caching for performance
    "--no-stream",        # Disable streaming for clean log output
    "--no-check-update"   # Don't check for aider updates (no interruptions)
    # Removed --no-auto-commit (was in new system but not in working old system)
]

# ===== AIDER COMMAND TEMPLATES =====
#
# 📊 EXPLANATION:
# Command templates for different use cases based on old system patterns.

AIDER_COMMAND_TEMPLATES = {
    "CHANGELOG": {
        "additional_flags": ["--no-git", "--sonnet"],  # Changelog uses --no-git and --sonnet (like old system)
        "pattern": "aider {base_flags} --read {log_file} --message-file {prompt_file} {output_file}"
    },
    "uidocs_REACT": {
        "additional_flags": [],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} {react_files}"
    },
    "uidocs_SASS": {
        "additional_flags": [],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} {sass_files}"
    },
    "uidocs_STORYBOOK": {
        "additional_flags": [],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} {storybook_files}"
    }
}

# ===== HELPER FUNCTIONS =====

def get_model_by_priority(priority: int = 1) -> Optional[Dict[str, Any]]:
    """
    Get model configuration by priority.
    
    Args:
        priority: Model priority (1 = highest priority)
        
    Returns:
        Dict[str, Any]: Model configuration or None if not found
        
    Examples:
        >>> model = get_model_by_priority(1)
        >>> print(model["name"])
        anthropic/claude-4-sonnet-20250514
    """
    for model_key, model_config in AI_MODELS.items():
        if model_config["priority"] == priority:
            return {
                "key": model_key,
                **model_config
            }
    return None


def select_model_by_tokens(token_count: int) -> Dict[str, Any]:
    """
    Select the best model based on token count requirements.
    
    Args:
        token_count: Number of tokens needed
        
    Returns:
        Dict[str, Any]: Selected model configuration
        
    Examples:
        >>> model = select_model_by_tokens(300000)
        >>> print(model["key"])
        CLAUDE_3_7_SONNET
    """
    # Sort models by priority
    sorted_models = sorted(
        AI_MODELS.items(), 
        key=lambda x: x[1]["priority"]
    )
    
    # Find first model that can handle the token count
    safety_margin = TOKEN_STRATEGY["SAFETY_MARGIN"]
    
    for model_key, model_config in sorted_models:
        effective_limit = int(model_config["max_tokens"] * safety_margin)
        if token_count <= effective_limit:
            return {
                "key": model_key,
                **model_config
            }
    
    # If no model can handle it, return the largest one
    largest_model = max(
        AI_MODELS.items(),
        key=lambda x: x[1]["max_tokens"]
    )
    
    return {
        "key": largest_model[0],
        **largest_model[1]
    }


def get_effective_token_limit(model_key: str) -> int:
    """
    Get the effective token limit for a model (with safety margin).
    
    Args:
        model_key: Model key (e.g., "CLAUDE_4_SONNET")
        
    Returns:
        int: Effective token limit
        
    Examples:
        >>> limit = get_effective_token_limit("CLAUDE_4_SONNET")
        >>> print(limit)
        900000
    """
    if model_key not in AI_MODELS:
        raise ValueError(f"Unknown model: {model_key}")
    
    max_tokens = AI_MODELS[model_key]["max_tokens"]
    safety_margin = TOKEN_STRATEGY["SAFETY_MARGIN"]
    
    return int(max_tokens * safety_margin)


def build_aider_command(command_type: str, model_key: str, **kwargs) -> str:
    """
    Build an aider command based on template and parameters.
    
    Args:
        command_type: Type of command ("CHANGELOG", "uidocs_REACT", "uidocs_SASS", "uidocs_STORYBOOK")
        model_key: Model to use
        **kwargs: Additional parameters for command template
        
    Returns:
        str: Complete aider command
        
    Examples:
        >>> cmd = build_aider_command(
        ...     "CHANGELOG",
        ...     "CLAUDE_4_SONNET",
        ...     log_file="git.log",
        ...     prompt_file="prompt.md",
        ...     output_file="changelog.md"
        ... )
    """
    if command_type not in AIDER_COMMAND_TEMPLATES:
        raise ValueError(f"Unknown command type: {command_type}")
    
    if model_key not in AI_MODELS:
        raise ValueError(f"Unknown model: {model_key}")
    
    template = AIDER_COMMAND_TEMPLATES[command_type]
    model_name = AI_MODELS[model_key]["name"]
    
    # Build base flags
    base_flags = AIDER_BASE_FLAGS.copy()
    base_flags.extend(template["additional_flags"])
    base_flags_str = " ".join(base_flags)
    
    # Format command
    command = template["pattern"].format(
        base_flags=base_flags_str,
        model=model_name,
        **kwargs
    )
    
    return command


def get_all_model_names() -> List[str]:
    """
    Get list of all available model names.
    
    Returns:
        List[str]: List of model names
        
    Examples:
        >>> models = get_all_model_names()
        >>> print(models[0])
        anthropic/claude-4-sonnet-20250514
    """
    return [config["name"] for config in AI_MODELS.values()]


def get_model_by_name(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Get model configuration by model name.
    
    Args:
        model_name: Full model name (e.g., "anthropic/claude-4-sonnet-20250514")
        
    Returns:
        Dict[str, Any]: Model configuration or None if not found
    """
    for model_key, model_config in AI_MODELS.items():
        if model_config["name"] == model_name:
            return {
                "key": model_key,
                **model_config
            }
    return None


# ===== VALIDATION CONSTANTS =====

VALID_COMMAND_TYPES = list(AIDER_COMMAND_TEMPLATES.keys())
VALID_MODEL_KEYS = list(AI_MODELS.keys())
DEFAULT_MODEL = get_model_by_priority(1)

# ===== EXPORT CONSTANTS =====

__all__ = [
    # Main constants
    "AI_MODELS",
    "TOKEN_STRATEGY", 
    "AIDER_BASE_FLAGS",
    "AIDER_COMMAND_TEMPLATES",
    
    # Helper functions
    "get_model_by_priority",
    "select_model_by_tokens",
    "get_effective_token_limit",
    "build_aider_command",
    "get_all_model_names",
    "get_model_by_name",
    
    # Validation constants
    "VALID_COMMAND_TYPES",
    "VALID_MODEL_KEYS",
    "DEFAULT_MODEL"
]
