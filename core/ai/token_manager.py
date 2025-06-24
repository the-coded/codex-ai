"""
Token manager for Codex-AI.

Simple token counting and git log mode selection.
"""

from typing import Tuple
from utils.get_token_count import get_token_count
from constants.ai import AI_MODELS, TOKEN_STRATEGY
from .model_selector import ModelInfo


def count_tokens(content: str) -> int:
    """Count tokens in content."""
    try:
        from utils.get_token_count import get_token_count_from_text
        return get_token_count_from_text(content, use_api=False)
    except Exception:
        # Fallback: ~4 characters per token
        return len(content) // 4


def should_use_detailed_git_log(commit_count: int, model: ModelInfo) -> Tuple[bool, str]:
    """
    Decide whether to use detailed or simple git log.
    
    Args:
        commit_count: Number of commits
        model: AI model info
        
    Returns:
        Tuple of (use_detailed, reasoning)
    """
    # Estimate tokens: detailed = ~200/commit, simple = ~50/commit
    detailed_tokens = commit_count * 200
    simple_tokens = commit_count * 50
    
    # Use safety margin from constants (95% of model's max_tokens)
    threshold = int(model.max_tokens * TOKEN_STRATEGY["SAFETY_MARGIN"])
    
    if detailed_tokens <= threshold:
        return True, f"Using detailed mode: {detailed_tokens:,} tokens"
    else:
        return False, f"Using simple mode: {simple_tokens:,} tokens (detailed would be {detailed_tokens:,})"
