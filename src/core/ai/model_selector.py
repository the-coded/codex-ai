"""
AI model selector for Codex-AI.

Simple model selection - just what we need.
"""

import os
from typing import Optional
from dataclasses import dataclass

from constants.ai import AI_MODELS


@dataclass
class ModelInfo:
    """Information about an AI model."""
    name: str
    aider_model: str
    max_tokens: int


def get_default_model() -> ModelInfo:
    """Get the default model (Claude-4 by default)."""
    # Always use Claude-4 as default since all models have same 200K limit
    return ModelInfo(
        name=AI_MODELS["CLAUDE_4_SONNET"]["name"],
        aider_model=AI_MODELS["CLAUDE_4_SONNET"]["name"],
        max_tokens=AI_MODELS["CLAUDE_4_SONNET"]["max_tokens"]
    )


def get_model_by_name(model_name: str) -> Optional[ModelInfo]:
    """Get model by name."""
    # Handle both full names and short keys
    for key, model_data in AI_MODELS.items():
        if (model_data["name"] == model_name or 
            key.lower().replace("_", "-") == model_name.lower().replace("_", "-") or
            key == model_name):
            return ModelInfo(
                name=model_data["name"],
                aider_model=model_data["name"],  # Same as name for now
                max_tokens=model_data["max_tokens"]
            )
    return None


def get_model_for_tokens(token_count: int) -> ModelInfo:
    """
    Get the most economical model that can handle the token count.
    
    Logic (cost optimization):
    - Claude-3.5: up to 200K tokens (cheapest)
    - Claude-3.7: up to 500K tokens (balanced)  
    - Claude-4: up to 1M tokens (premium)
    """
    # Sort models by max_tokens (ascending) for cost optimization: 3.5 → 3.7 → 4
    sorted_models = sorted(AI_MODELS.items(), key=lambda x: x[1]["max_tokens"])
    
    # Find the cheapest model that can handle the tokens
    for key, model_data in sorted_models:
        if token_count <= model_data["max_tokens"]:
            return ModelInfo(
                name=model_data["name"],
                aider_model=model_data["name"],
                max_tokens=model_data["max_tokens"]
            )
    
    # If no model can handle it, return the largest one (Claude-4)
    return get_default_model()
