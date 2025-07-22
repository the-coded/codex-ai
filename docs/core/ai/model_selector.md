# Model Selector Documentation

## Overview

The `model_selector.py` module provides intelligent AI model selection functionality for the Codex-AI project. It implements cost-optimized model selection based on token requirements, ensuring the most economical model is chosen while meeting performance needs. The module serves as a central component for managing AI model configurations and selection logic within the `src/core/ai` directory.

## Main Functions/Classes

### ModelInfo (Dataclass)

A data structure that encapsulates information about an AI model.

- **Purpose**: Stores model metadata including name, aider model identifier, and token limits
- **Attributes**:
  - `name` (str): Human-readable model name
  - `aider_model` (str): Model identifier used by the aider system
  - `max_tokens` (int): Maximum token capacity for the model
- **Example**:

```python
model = ModelInfo(
    name="claude-3-5-sonnet-20241022",
    aider_model="claude-3-5-sonnet-20241022", 
    max_tokens=200000
)
```

### get_default_model()

Returns the default AI model configuration.

- **Purpose**: Provides a consistent default model (Claude-4) for the application
- **Parameters**: None
- **Returns**: `ModelInfo` object with Claude-4 configuration
- **Example**:

```python
default = get_default_model()
print(f"Default model: {default.name}")
# Output: Default model: claude-3-5-sonnet-20241022
```

### get_model_by_name(model_name: str)

Retrieves a model configuration by name with flexible matching.

- **Purpose**: Finds model configuration using various naming conventions
- **Parameters**: 
  - `model_name` (str): Model name, key, or identifier to search for
- **Returns**: `ModelInfo` object if found, `None` otherwise
- **Matching Logic**: Supports full names, short keys, and case-insensitive matching with underscore/hyphen normalization
- **Example**:

```python
# All of these work:
model1 = get_model_by_name("claude-3-5-sonnet-20241022")
model2 = get_model_by_name("CLAUDE_3_5_SONNET") 
model3 = get_model_by_name("claude-3-5-sonnet")

if model1:
    print(f"Found model: {model1.name}")
```

### get_model_for_tokens(token_count: int)

Selects the most cost-effective model that can handle the specified token count.

- **Purpose**: Implements cost optimization by choosing the cheapest model that meets token requirements
- **Parameters**:
  - `token_count` (int): Number of tokens that need to be processed
- **Returns**: `ModelInfo` object for the optimal model
- **Selection Logic**:
  - Claude-3.5: up to 200K tokens (cheapest)
  - Claude-3.7: up to 500K tokens (balanced)
  - Claude-4: up to 1M tokens (premium)
- **Fallback**: Returns Claude-4 if no model can handle the token count
- **Example**:

```python
# Small request - gets cheapest model
small_model = get_model_for_tokens(50000)
print(f"For 50K tokens: {small_model.name}")

# Large request - gets appropriate model
large_model = get_model_for_tokens(800000)
print(f"For 800K tokens: {large_model.name}")

# Oversized request - gets largest available
huge_model = get_model_for_tokens(2000000)
print(f"For 2M tokens: {huge_model.name}")
```

## Dependencies

### External Libraries
- `os`: Standard library for environment variable access
- `typing.Optional`: Type hinting for optional return values
- `dataclasses.dataclass`: Decorator for creating data classes

### Internal Dependencies
- `constants.ai.AI_MODELS`: Configuration dictionary containing model definitions and specifications

### Configuration Requirements
The module depends on the `AI_MODELS` constant which should contain model configurations with the following structure:

```python
AI_MODELS = {
    "MODEL_KEY": {
        "name": "model-identifier",
        "max_tokens": 200000
    }
}
```

## Usage Examples

### Basic Model Selection

```python
from core.ai.model_selector import get_default_model, get_model_for_tokens

# Get default model for general use
default_model = get_default_model()
print(f"Using default: {default_model.name}")

# Select model based on content size
token_count = 150000
optimal_model = get_model_for_tokens(token_count)
print(f"For {token_count} tokens: {optimal_model.name}")
```

### Integration with Token Management

```python
from core.ai.model_selector import get_model_for_tokens
from core.ai.token_manager import count_tokens

# Count tokens in content
content = "Your large text content here..."
token_count = count_tokens(content)

# Select appropriate model
model = get_model_for_tokens(token_count)
print(f"Content has {token_count} tokens, using {model.name}")
```

### Model Lookup by Name

```python
from core.ai.model_selector import get_model_by_name

# Try different naming conventions
model_names = [
    "claude-3-5-sonnet-20241022",
    "CLAUDE_3_5_SONNET",
    "claude-3-5-sonnet"
]

for name in model_names:
    model = get_model_by_name(name)
    if model:
        print(f"Found {name}: {model.max_tokens} tokens")
    else:
        print(f"Model {name} not found")
```

### Cost Optimization Workflow

```python
def select_model_for_task(content_size: int, priority: str = "cost"):
    """Select model based on content size and priority."""
    
    if priority == "cost":
        # Use cost-optimized selection
        return get_model_for_tokens(content_size)
    elif priority == "performance":
        # Always use the best model
        return get_default_model()
    else:
        # Fallback to default
        return get_default_model()

# Usage
model = select_model_for_task(75000, "cost")
print(f"Selected model: {model.name} (max: {model.max_tokens})")
```

## Implementation Notes

### Design Decisions

1. **Cost Optimization Priority**: The `get_model_for_tokens()` function prioritizes cost efficiency by selecting the cheapest model that meets requirements, rather than always using the most powerful model.

2. **Flexible Name Matching**: The `get_model_by_name()` function implements robust name matching to handle various naming conventions, making the API more user-friendly.

3. **Graceful Fallbacks**: All functions provide sensible fallback behavior, ensuring the system remains functional even with invalid inputs or edge cases.

### Performance Considerations

- **Model Sorting**: The token-based selection sorts models by capacity only once per call, maintaining O(n log n) complexity where n is the number of available models.
- **Dictionary Lookups**: Model name matching uses dictionary iteration, which is acceptable given the small number of models but could be optimized with a reverse lookup table for larger model sets.

### Known Limitations

1. **Static Model Configuration**: Model definitions are loaded from constants, requiring code changes to add new models.
2. **Simple Cost Model**: Cost optimization assumes smaller token limits correlate with lower costs, which may not always be accurate.
3. **No Dynamic Pricing**: The system doesn't account for real-time pricing or usage-based cost variations.

### Edge Cases

- **Oversized Requests**: When token count exceeds all model limits, the system returns the largest available model rather than failing.
- **Invalid Model Names**: Non-existent model names return `None`, allowing calling code to handle the error appropriately.
- **Zero/Negative Tokens**: The system will return the smallest available model for zero or negative token counts.

### Future Improvement Opportunities

1. **Dynamic Model Loading**: Implement configuration-based model loading to avoid code changes for new models.
2. **Real-time Cost Optimization**: Integrate with pricing APIs to make cost-based decisions using current rates.
3. **Performance Metrics**: Add model performance tracking to inform selection decisions beyond just cost and capacity.
4. **Caching**: Implement model selection caching for repeated requests with similar token counts.

## Error Handling

The module uses defensive programming practices:

```python
# Safe model selection with fallback
def safe_model_selection(token_count: int, preferred_model: str = None):
    """Example of safe model selection with error handling."""
    
    # Try preferred model first
    if preferred_model:
        model = get_model_by_name(preferred_model)
        if model and token_count <= model.max_tokens:
            return model
    
    # Fall back to token-based selection
    return get_model_for_tokens(token_count)
```

## Testing Considerations

Key areas for testing:

1. **Model Selection Logic**: Verify correct model selection for various token counts
2. **Name Matching**: Test all supported naming conventions and edge cases
3. **Fallback Behavior**: Ensure graceful handling of invalid inputs
4. **Cost Optimization**: Validate that the cheapest suitable model is always selected

```python
# Example test cases
def test_model_selection():
    # Test cost optimization
    small_model = get_model_for_tokens(50000)
    assert small_model.max_tokens == 200000  # Should get cheapest
    
    # Test fallback for oversized requests
    huge_model = get_model_for_tokens(2000000)
    assert huge_model.name == get_default_model().name
    
    # Test name matching
    model = get_model_by_name("CLAUDE_3_5_SONNET")
    assert model is not None
```

## See Also

- [Token Manager](token_manager.md) - Token counting and management utilities
- [Aider Interface](aider_interface.md) - Integration with aider AI coding assistant
- [AI Constants](../../constants/ai.md) - Model configuration definitions
- [Core AI Module](README.md) - Overview of the AI core functionality
