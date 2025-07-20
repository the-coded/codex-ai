"""
Token manager for Codex-AI.

Comprehensive token counting and management functionality.
All token-related functions consolidated in this module.
"""

import os
import re
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path

from constants.ai import AI_MODELS, TOKEN_STRATEGY
from .model_selector import ModelInfo

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

# ===== CONSTANTS =====

# Default model for token counting (imported from constants)
try:
    from constants.ai import DEFAULT_MODEL, get_default_model_name
    DEFAULT_MODEL = get_default_model_name()
except ImportError:
    # Fallback if constants not available
    DEFAULT_MODEL = "anthropic/claude-4-sonnet-20250514"

# Fallback ratios for different content types (more accurate than char_count // 4)
FALLBACK_RATIOS = {
    "code": 3.2,        # Code is more token-dense
    "markdown": 3.8,    # Markdown has formatting overhead
    "text": 4.0,        # Plain text baseline
    "json": 3.5,        # JSON structure adds tokens
    "yaml": 3.6,        # YAML structure
    "html": 3.3,        # HTML tags are token-dense
    "css": 3.4,         # CSS properties
    "default": 3.8      # Conservative default
}

# File extension to content type mapping
CONTENT_TYPE_MAP = {
    # Code files
    ".py": "code", ".js": "code", ".ts": "code", ".jsx": "code", ".tsx": "code",
    ".java": "code", ".cpp": "code", ".c": "code", ".h": "code", ".cs": "code",
    ".php": "code", ".rb": "code", ".go": "code", ".rs": "code", ".swift": "code",
    
    # Markup and documentation
    ".md": "markdown", ".mdx": "markdown", ".txt": "text", ".rst": "text",
    ".html": "html", ".htm": "html", ".xml": "html", ".svg": "html",
    
    # Styles
    ".css": "css", ".scss": "css", ".sass": "css", ".less": "css",
    
    # Data formats
    ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "yaml",
    ".ini": "text", ".conf": "text", ".cfg": "text",
    
    # Default
    "default": "default"
}

# ===== HELPER FUNCTIONS =====

def _get_content_type(file_path: str) -> str:
    """
    Determine content type from file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Content type for token estimation
    """
    ext = Path(file_path).suffix.lower()
    return CONTENT_TYPE_MAP.get(ext, "default")


def _clean_text_for_counting(text: str) -> str:
    """
    Clean text for more accurate token counting.
    
    Args:
        text: Raw text content
        
    Returns:
        str: Cleaned text
    """
    # Remove excessive whitespace but preserve structure
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 consecutive newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Normalize spaces
    text = text.strip()
    
    return text


def _estimate_tokens_fallback(text: str, content_type: str = "default") -> int:
    """
    Fallback token estimation using improved character-based method.
    
    Args:
        text: Text content to count
        content_type: Type of content for ratio selection
        
    Returns:
        int: Estimated token count
    """
    if not text:
        return 0
    
    # Clean text first
    cleaned_text = _clean_text_for_counting(text)
    char_count = len(cleaned_text)
    
    # Use content-specific ratio
    ratio = FALLBACK_RATIOS.get(content_type, FALLBACK_RATIOS["default"])
    
    # Apply ratio with minimum of 1 token
    tokens = max(1, int(char_count / ratio))
    
    return tokens


def _estimate_tokens_tiktoken(text: str) -> int:
    """
    Use tiktoken for more accurate fallback estimation.
    
    Args:
        text: Text content to count
        
    Returns:
        int: Estimated token count
    """
    if not TIKTOKEN_AVAILABLE:
        return _estimate_tokens_fallback(text)
    
    try:
        # Use GPT-4 encoding as approximation for Claude
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = len(encoding.encode(text))
        
        # Claude tokens are typically 10-15% different from GPT-4
        # Apply correction factor
        return int(tokens * 1.1)
        
    except Exception:
        # Fall back to character-based method
        return _estimate_tokens_fallback(text)


# ===== MAIN FUNCTIONS =====

def get_token_count_from_text(
    text: str, 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> int:
    """
    Get accurate token count from text using Anthropic's API.
    
    Args:
        text: Text content to count tokens for
        model: Model to use for counting (affects tokenization)
        use_api: Whether to use official API (True) or fallback (False)
        
    Returns:
        int: Number of tokens in the text
        
    Examples:
        >>> count = get_token_count_from_text("Hello, world!")
        >>> print(count)
        4
        
        >>> count = get_token_count_from_text("Large text...", use_api=False)
        >>> print(count)  # Uses fallback estimation
        150
    """
    # Handle None or non-string inputs gracefully
    if text is None:
        return 0
    
    # Convert non-string inputs to string
    if not isinstance(text, str):
        text = str(text)
    
    # Check for empty text after conversion
    if not text or not text.strip():
        return 0
    
    # Try official API first if available and requested
    if use_api and ANTHROPIC_AVAILABLE:
        try:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                client = anthropic.Anthropic(api_key=api_key)
                
                # Clean model name (remove provider prefix if present)
                clean_model = model.replace("anthropic/", "")
                
                response = client.messages.count_tokens(
                    model=clean_model,
                    messages=[{
                        "role": "user",
                        "content": text
                    }]
                )
                
                return response.input_tokens
                
        except Exception as e:
            # API failed, fall back to local estimation
            print(f"Warning: API token counting failed ({e}), using fallback")
    
    # Use tiktoken if available, otherwise character-based
    if TIKTOKEN_AVAILABLE:
        return _estimate_tokens_tiktoken(text)
    else:
        return _estimate_tokens_fallback(text, "text")


def get_token_count(
    file_path: str, 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> int:
    """
    Get token count from a file.
    
    Args:
        file_path: Path to the file to count tokens
        model: Model to use for counting
        use_api: Whether to use official API
        
    Returns:
        int: Number of tokens in the file
        
    Examples:
        >>> count = get_token_count("README.md")
        >>> print(count)
        1250
        
        >>> count = get_token_count("large_file.py", use_api=False)
        >>> print(count)  # Uses fallback
        3500
    """
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If using fallback, determine content type for better estimation
        if not use_api or not ANTHROPIC_AVAILABLE:
            content_type = _get_content_type(file_path)
            return _estimate_tokens_fallback(content, content_type)
        
        return get_token_count_from_text(content, model, use_api)
        
    except (FileNotFoundError, UnicodeDecodeError, PermissionError) as e:
        print(f"Warning: Could not read file {file_path}: {e}")
        return 0
    except Exception as e:
        print(f"Error counting tokens in {file_path}: {e}")
        return 0


def get_multiple_files_token_count(
    file_paths: List[str], 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> Dict[str, int]:
    """
    Get token counts for multiple files.
    
    Args:
        file_paths: List of file paths to count
        model: Model to use for counting
        use_api: Whether to use official API
        
    Returns:
        Dict[str, int]: Mapping of file path to token count
        
    Examples:
        >>> counts = get_multiple_files_token_count(["file1.py", "file2.md"])
        >>> print(counts)
        {"file1.py": 500, "file2.md": 300}
    """
    results = {}
    
    for file_path in file_paths:
        results[file_path] = get_token_count(file_path, model, use_api)
    
    return results


def get_total_token_count(
    file_paths: List[str], 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> int:
    """
    Get total token count across multiple files.
    
    Args:
        file_paths: List of file paths to count
        model: Model to use for counting
        use_api: Whether to use official API
        
    Returns:
        int: Total token count across all files
        
    Examples:
        >>> total = get_total_token_count(["file1.py", "file2.md"])
        >>> print(total)
        800
    """
    counts = get_multiple_files_token_count(file_paths, model, use_api)
    return sum(counts.values())


def estimate_model_for_token_count(
    token_count: int,
    safety_margin: float = 0.95
) -> str:
    """
    Suggest the best model based on token count.
    
    Args:
        token_count: Number of tokens to process
        safety_margin: Safety margin (0.95 = use 95% of model capacity)
        
    Returns:
        str: Recommended model name
        
    Examples:
        >>> model = estimate_model_for_token_count(300000)
        >>> print(model)
        "anthropic/claude-3-7-sonnet-latest"
    """
    # Import here to avoid circular imports
    from constants.ai import AI_MODELS, select_model_by_tokens
    
    try:
        selected = select_model_by_tokens(token_count)
        return selected["name"]
    except Exception:
        # Fallback to default model
        return DEFAULT_MODEL


def validate_token_count_for_model(
    token_count: int, 
    model: str,
    safety_margin: float = 0.95
) -> bool:
    """
    Check if token count is within model limits.
    
    Args:
        token_count: Number of tokens
        model: Model name to check against
        safety_margin: Safety margin for the check
        
    Returns:
        bool: True if within limits, False otherwise
        
    Examples:
        >>> valid = validate_token_count_for_model(100000, "claude-4-sonnet")
        >>> print(valid)
        True
    """
    try:
        from constants.ai import AI_MODELS, get_effective_token_limit
        
        # Find model key from name
        model_key = None
        for key, config in AI_MODELS.items():
            if config["name"] == model or config["name"] == f"anthropic/{model}":
                model_key = key
                break
        
        if not model_key:
            # Unknown model, assume it can handle the tokens
            return True
        
        limit = get_effective_token_limit(model_key)
        return token_count <= limit
        
    except Exception:
        # If we can't determine limits, assume it's valid
        return True


# ===== UTILITY FUNCTIONS =====

def get_token_count_summary(file_paths: List[str]) -> Dict[str, Any]:
    """
    Get comprehensive token count summary for files.
    
    Args:
        file_paths: List of file paths to analyze
        
    Returns:
        Dict[str, Any]: Summary with counts, recommendations, etc.
        
    Examples:
        >>> summary = get_token_count_summary(["file1.py", "file2.md"])
        >>> print(summary["total_tokens"])
        800
        >>> print(summary["recommended_model"])
        "claude-4-sonnet"
    """
    # Get individual counts
    counts = get_multiple_files_token_count(file_paths)
    total = sum(counts.values())
    
    # Get model recommendation
    recommended_model = estimate_model_for_token_count(total)
    
    # Check if within limits
    within_limits = validate_token_count_for_model(total, recommended_model)
    
    return {
        "file_counts": counts,
        "total_tokens": total,
        "file_count": len(file_paths),
        "average_tokens_per_file": total // len(file_paths) if file_paths else 0,
        "recommended_model": recommended_model,
        "within_model_limits": within_limits,
        "api_available": ANTHROPIC_AVAILABLE,
        "tiktoken_available": TIKTOKEN_AVAILABLE
    }


# ===== BACKWARDS COMPATIBILITY =====

def get_token_count_legacy(file_path: str) -> int:
    """
    Legacy function for backwards compatibility.
    Uses the old char_count // 4 method.
    
    Args:
        file_path: Path to file
        
    Returns:
        int: Token count using old method
        
    Note:
        This function is deprecated. Use get_token_count() instead.
    """
    import subprocess
    
    try:
        result = subprocess.run(
            f"wc -m < {file_path}",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        char_count = int(result.stdout.strip())
        return char_count // 4
    except (subprocess.CalledProcessError, ValueError):
        return 0


# ===== SIMPLIFIED API FUNCTIONS =====

def count_tokens(content: str) -> int:
    """
    Count tokens in content using local functions.
    
    Args:
        content: Content to count tokens for
        
    Returns:
        int: Number of tokens
    """
    try:
        return get_token_count_from_text(content, use_api=False)
    except Exception:
        # Fallback: ~4 characters per token
        return len(content) // 4


# ===== EXPORT =====

__all__ = [
    # Main functions
    "get_token_count",
    "get_token_count_from_text",
    "get_multiple_files_token_count",
    "get_total_token_count",
    
    # Model selection
    "estimate_model_for_token_count",
    "validate_token_count_for_model",
    
    # Utilities
    "get_token_count_summary",
    
    # Legacy
    "get_token_count_legacy",
    
    # Simplified API
    "count_tokens"
]
