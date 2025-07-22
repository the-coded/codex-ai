# Token Manager Documentation

## Overview

The `token_manager.py` module provides comprehensive token counting and management functionality for the Codex-AI project. It serves as the central hub for all token-related operations, offering both API-based and fallback token counting methods with intelligent model selection capabilities.

### Key Responsibilities
- Accurate token counting using Anthropic's official API
- Fallback token estimation when API is unavailable
- Content-type-aware token estimation
- Model recommendation based on token counts
- Token limit validation for different AI models
- Batch processing of multiple files

## Implementation Details

### Core Architecture

The module implements a multi-layered approach to token counting:

1. **Primary Layer**: Anthropic API for precise token counts
2. **Secondary Layer**: tiktoken library for GPT-4 based estimation
3. **Fallback Layer**: Content-aware character-based estimation

### Key Data Structures

```python
# Content type ratios for accurate fallback estimation
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
    ".py": "code", ".js": "code", ".ts": "code",
    ".md": "markdown", ".txt": "text",
    ".json": "json", ".yaml": "yaml",
    # ... extensive mapping for various file types
}
```

## Dependencies & Imports

### External Dependencies
- **anthropic**: Official Anthropic API client (optional)
- **tiktoken**: OpenAI's tokenizer library (optional)
- **pathlib**: File path handling
- **re**: Regular expression operations
- **os**: Environment variable access

### Internal Dependencies
- **constants.ai**: AI model configurations and constants
- **model_selector**: Model selection utilities

### Environment Requirements
- `ANTHROPIC_API_KEY`: Required for API-based token counting
- Optional dependencies are gracefully handled with fallbacks

## API Documentation

### Primary Functions

#### get_token_count_from_text()

```python
def get_token_count_from_text(
    text: str, 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> int:
```

- **Purpose**: Get accurate token count from text content
- **Parameters**:
  - `text` (str): Text content to count tokens for
  - `model` (str): Model to use for counting (affects tokenization)
  - `use_api` (bool): Whether to use official API or fallback methods
- **Returns**: int - Number of tokens in the text
- **Example**:

```python
# Basic usage
count = get_token_count_from_text("Hello, world!")
print(count)  # Output: 4

# With specific model
count = get_token_count_from_text(
    "Large text content...", 
    model="claude-3-sonnet-20240229",
    use_api=True
)
```

#### get_token_count()

```python
def get_token_count(
    file_path: str, 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> int:
```

- **Purpose**: Get token count from a file
- **Parameters**:
  - `file_path` (str): Path to the file to count tokens
  - `model` (str): Model to use for counting
  - `use_api` (bool): Whether to use official API
- **Returns**: int - Number of tokens in the file
- **Example**:

```python
# Count tokens in a Python file
count = get_token_count("src/main.py")
print(f"main.py contains {count} tokens")

# Use fallback method for faster processing
count = get_token_count("large_file.py", use_api=False)
```

#### get_multiple_files_token_count()

```python
def get_multiple_files_token_count(
    file_paths: List[str], 
    model: str = DEFAULT_MODEL,
    use_api: bool = True
) -> Dict[str, int]:
```

- **Purpose**: Get token counts for multiple files efficiently
- **Parameters**:
  - `file_paths` (List[str]): List of file paths to count
  - `model` (str): Model to use for counting
  - `use_api` (bool): Whether to use official API
- **Returns**: Dict[str, int] - Mapping of file path to token count
- **Example**:

```python
files = ["src/main.py", "docs/README.md", "config.json"]
counts = get_multiple_files_token_count(files)
for file_path, count in counts.items():
    print(f"{file_path}: {count} tokens")
```

### Model Selection Functions

#### estimate_model_for_token_count()

```python
def estimate_model_for_token_count(
    token_count: int,
    safety_margin: float = 0.95
) -> str:
```

- **Purpose**: Suggest the best model based on token count
- **Parameters**:
  - `token_count` (int): Number of tokens to process
  - `safety_margin` (float): Safety margin (0.95 = use 95% of model capacity)
- **Returns**: str - Recommended model name
- **Example**:

```python
# Get recommendation for large context
model = estimate_model_for_token_count(300000)
print(f"Recommended model: {model}")
# Output: "anthropic/claude-3-7-sonnet-latest"
```

#### validate_token_count_for_model()

```python
def validate_token_count_for_model(
    token_count: int, 
    model: str,
    safety_margin: float = 0.95
) -> bool:
```

- **Purpose**: Check if token count is within model limits
- **Parameters**:
  - `token_count` (int): Number of tokens
  - `model` (str): Model name to check against
  - `safety_margin` (float): Safety margin for the check
- **Returns**: bool - True if within limits, False otherwise

### Utility Functions

#### get_token_count_summary()

```python
def get_token_count_summary(file_paths: List[str]) -> Dict[str, Any]:
```

- **Purpose**: Get comprehensive token count summary for files
- **Returns**: Dictionary containing:
  - `file_counts`: Individual file token counts
  - `total_tokens`: Sum of all tokens
  - `file_count`: Number of files processed
  - `average_tokens_per_file`: Average tokens per file
  - `recommended_model`: Suggested model for the total count
  - `within_model_limits`: Whether total fits in recommended model
  - `api_available`: Whether Anthropic API is available
  - `tiktoken_available`: Whether tiktoken library is available

## Usage Examples

### Basic Token Counting

```python
from src.core.ai.token_manager import get_token_count_from_text, get_token_count

# Count tokens in text
text = "This is a sample text for token counting."
tokens = get_token_count_from_text(text)
print(f"Text contains {tokens} tokens")

# Count tokens in a file
file_tokens = get_token_count("README.md")
print(f"README.md contains {file_tokens} tokens")
```

### Batch Processing

```python
from src.core.ai.token_manager import (
    get_multiple_files_token_count, 
    get_total_token_count,
    get_token_count_summary
)

# Process multiple files
files = ["src/main.py", "src/utils.py", "docs/api.md"]

# Get individual counts
counts = get_multiple_files_token_count(files)

# Get total count
total = get_total_token_count(files)

# Get comprehensive summary
summary = get_token_count_summary(files)
print(f"Total tokens: {summary['total_tokens']}")
print(f"Recommended model: {summary['recommended_model']}")
print(f"Within limits: {summary['within_model_limits']}")
```

### Model Selection and Validation

```python
from src.core.ai.token_manager import (
    estimate_model_for_token_count,
    validate_token_count_for_model
)

# Get model recommendation
token_count = 150000
recommended_model = estimate_model_for_token_count(token_count)
print(f"For {token_count} tokens, use: {recommended_model}")

# Validate token count for specific model
is_valid = validate_token_count_for_model(
    token_count, 
    "claude-3-sonnet-20240229"
)
print(f"Valid for Claude Sonnet: {is_valid}")
```

### Fallback Usage

```python
# Use fallback methods when API is unavailable
count = get_token_count_from_text(
    "Large text content...", 
    use_api=False  # Force fallback
)

# Content-aware estimation
count = get_token_count("complex_code.py", use_api=False)
# Automatically uses "code" content type for better estimation
```

## Implementation Notes

### Performance Considerations

1. **API Rate Limits**: The module respects Anthropic API rate limits and gracefully falls back to local estimation
2. **Caching**: Consider implementing caching for frequently counted files
3. **Batch Processing**: Use `get_multiple_files_token_count()` for better performance when processing many files

### Error Handling

The module implements comprehensive error handling:
- Graceful degradation when dependencies are missing
- File reading error handling with informative warnings
- API failure fallbacks with automatic retry logic

### Content Type Detection

The module uses file extensions to determine content types for more accurate fallback estimation:

```python
# Different content types have different token densities
code_tokens = get_token_count("script.py", use_api=False)      # Uses 3.2 ratio
markdown_tokens = get_token_count("README.md", use_api=False)  # Uses 3.8 ratio
json_tokens = get_token_count("config.json", use_api=False)    # Uses 3.5 ratio
```

### Known Limitations

1. **Fallback Accuracy**: Character-based estimation is approximate (±20% accuracy)
2. **Model Variations**: Different models may tokenize text differently
3. **Large Files**: Very large files may hit memory limits during processing
4. **Binary Files**: Module doesn't handle binary files gracefully

### Future Improvements

1. **Caching Layer**: Implement file-based caching for token counts
2. **Streaming Support**: Add support for streaming large files
3. **Custom Tokenizers**: Support for additional tokenizer libraries
4. **Parallel Processing**: Multi-threaded processing for large file sets

## Integration with Other Components

### With Model Selector

```python
from src.core.ai.token_manager import get_token_count_summary
from src.core.ai.model_selector import select_optimal_model

# Get token summary
summary = get_token_count_summary(file_paths)

# Use with model selector
optimal_model = select_optimal_model(
    token_count=summary['total_tokens'],
    task_type="code_analysis"
)
```

### With Prompt Processor

```python
# Validate prompt size before processing
from src.core.ai.token_manager import validate_token_count_for_model

prompt_tokens = get_token_count_from_text(prompt_text)
if validate_token_count_for_model(prompt_tokens, selected_model):
    # Process prompt
    result = process_prompt(prompt_text, selected_model)
else:
    # Handle oversized prompt
    print("Prompt too large for selected model")
```

## See Also

- [Model Selector Documentation](model_selector.md)
- [AI Constants Configuration](../../constants/ai.md)
- [Prompt Processor Documentation](prompt_processor.md)
- [Aider Interface Documentation](aider_interface.md)
