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
        "max_output_tokens": 64000,  # Aider default max_tokens for response
        "priority": 1           # Default choice
    },
    "CLAUDE_3_7_SONNET": {
        "name": "anthropic/claude-3-7-sonnet-latest", 
        "max_tokens": 200000,   # 200K context window (confirmed by Anthropic docs)
        "max_output_tokens": 64000,  # Aider default max_tokens for response
        "priority": 2           # Second choice
    },
    "CLAUDE_3_5_SONNET": {
        "name": "anthropic/claude-3-5-sonnet-latest",
        "max_tokens": 200000,   # 200K context window (confirmed by Anthropic docs)
        "max_output_tokens": 64000,  # Aider default max_tokens for response
        "priority": 3           # Third choice / fallback
    }
}

# ===== TOKEN STRATEGY =====
#
# 📊 EXPLANATION:
# Token management strategy for automatic model selection and fallback.
# Based on the old changelog system but now dynamic per model.

TOKEN_STRATEGY = {
    "SAFETY_MARGIN": 0.95,        # Use 95% of model's max_tokens as limit
    "PROMPT_OVERHEAD": 5000,       # Real Aider overhead only (was 15k estimated)
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
    "--no-stream",        # Disable streaming for clean log output
    "--no-check-update",   # Don't check for aider updates (no interruptions)
    "--map-tokens 0",     # Disable token mapping for performance
]

# ===== AIDER COMMAND TEMPLATES =====
#
# 📊 EXPLANATION:
# Command templates for different use cases based on old system patterns.

AIDER_COMMAND_TEMPLATES = {
    "CHANGELOG": {
        "additional_flags": [
            ["--no-git"], 
            ["--thinking-tokens", "4k"]
        ],
        "pattern": "aider {base_flags} --read {log_file} --message-file {prompt_file} {output_file}"
    },
    "ui-lib_REACT": {
        "additional_flags": [
            ["--no-git"],
        ],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} --file {react_files}"
    },
    "ui-lib_SASS": {
        "additional_flags": [
            ["--no-git"], 
        ],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} --file {sass_files}"
    },
    "ui-lib_STORYBOOK": {
        "additional_flags": [
            ["--no-git"], 
        ],
        "pattern": "aider {base_flags} --model {model} --read {context_path} --message-file {prompt_file} --file {storybook_files}"
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
    Get the effective token limit for git log content only.
    
    This calculates the maximum tokens available for git log content by subtracting:
    - max_output_tokens (reserved for AI response)
    - prompt overhead (5K tokens for Aider internal overhead only)
    - safety margin
    
    Args:
        model_key: Model key (e.g., "CLAUDE_4_SONNET")
        
    Returns:
        int: Effective token limit for git log content
        
    Examples:
        >>> limit = get_effective_token_limit("CLAUDE_4_SONNET")
        >>> print(limit)
        124450  # (200K - 64K - 5K) * 0.95 = 124.45K
    """
    if model_key not in AI_MODELS:
        raise ValueError(f"Unknown model: {model_key}")
    
    model_config = AI_MODELS[model_key]
    context_window = model_config["max_tokens"]
    max_output = model_config["max_output_tokens"]
    
    # Reserve tokens for different components
    prompt_overhead = TOKEN_STRATEGY["PROMPT_OVERHEAD"]
    
    # Available tokens for git log = total - output - prompt - safety margin
    available_for_input = context_window - max_output - prompt_overhead
    safety_margin = TOKEN_STRATEGY["SAFETY_MARGIN"]
    
    return int(available_for_input * safety_margin)


def build_aider_command(command_type: str, model_key: str, **kwargs) -> str:
    """
    Build an aider command based on template and parameters.
    
    Args:
        command_type: Type of command ("CHANGELOG", "ui-lib_REACT", "ui-lib_SASS", "ui-lib_STORYBOOK")
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
    
    # Process additional_flags - support both old format (strings) and new format (arrays)
    for flag_item in template["additional_flags"]:
        if isinstance(flag_item, list):
            # New format: ["--flag", "value"] or ["--flag"]
            if len(flag_item) == 1:
                base_flags.append(flag_item[0])  # Flag without value
            elif len(flag_item) == 2:
                base_flags.append(f"{flag_item[0]} {flag_item[1]}")  # Flag with value
        else:
            # Old format: "--flag value" (backward compatibility)
            base_flags.append(flag_item)
    
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


def get_cli_model_choices() -> List[str]:
    """
    Get CLI model choices sorted by priority.
    
    Returns:
        List[str]: List of model keys sorted by priority
        
    Examples:
        >>> choices = get_cli_model_choices()
        >>> print(choices)
        ['CLAUDE_4_SONNET', 'CLAUDE_3_7_SONNET', 'CLAUDE_3_5_SONNET']
    """
    # Sort models by priority and return keys directly
    sorted_models = sorted(
        AI_MODELS.items(),
        key=lambda x: x[1]['priority']
    )
    
    return [model_key for model_key, _ in sorted_models]


def get_model_token_limits() -> Dict[str, int]:
    """
    Get token limits for all models in various naming formats.
    
    Returns:
        Dict[str, int]: Mapping of model names to max tokens
        
    Examples:
        >>> limits = get_model_token_limits()
        >>> print(limits['claude_4_sonnet'])
        200000
    """
    token_limits = {}
    
    for model_key, model_config in AI_MODELS.items():
        max_tokens = model_config["max_tokens"]
        model_name = model_config["name"]
        
        # Add various naming formats
        cli_name = model_key.lower()  # CLAUDE_4_SONNET -> claude_4_sonnet
        token_limits[cli_name] = max_tokens
        token_limits[model_name] = max_tokens  # Full anthropic name
        
        # Add additional common variations
        if "claude-4-sonnet" in model_name:
            token_limits["claude-4-sonnet-20250514"] = max_tokens
        elif "claude-3-7-sonnet" in model_name:
            token_limits["claude-3-7-sonnet-latest"] = max_tokens
        elif "claude-3-5-sonnet" in model_name:
            token_limits["claude-3-5-sonnet-latest"] = max_tokens
    
    return token_limits


def get_model_name_mapping() -> Dict[str, str]:
    """
    Get mapping from full model names to AI_MODELS keys.
    
    Returns:
        Dict[str, str]: Mapping of model names to keys
        
    Examples:
        >>> mapping = get_model_name_mapping()
        >>> print(mapping['anthropic/claude-4-sonnet-20250514'])
        'CLAUDE_4_SONNET'
    """
    mapping = {}
    
    for model_key, model_config in AI_MODELS.items():
        model_name = model_config["name"]
        mapping[model_name] = model_key
    
    return mapping


def get_default_model_name() -> str:
    """
    Get the default model name (priority 1).
    
    Returns:
        str: Full model name
        
    Examples:
        >>> model_name = get_default_model_name()
        >>> print(model_name)
        'anthropic/claude-4-sonnet-20250514'
    """
    default_model = get_model_by_priority(1)
    return default_model["name"] if default_model else "anthropic/claude-4-sonnet-20250514"


# ===== VALIDATION CONSTANTS =====

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
    "get_cli_model_choices",
    "get_model_token_limits",
    "get_model_name_mapping",
    "get_default_model_name",
    
    # Validation constants
    "DEFAULT_MODEL"
]
