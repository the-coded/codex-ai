# AI Constants and Configuration Documentation

## Overview

The `src/constants/ai.py` module serves as the central configuration hub for AI model management and Aider command generation in the Codex-AI project. It provides a comprehensive system for managing multiple Anthropic Claude models with automatic fallback strategies, token management, and standardized command templates for various documentation generation tasks.

This module abstracts the complexity of AI model selection and Aider integration, enabling automated code generation and documentation processing with intelligent resource management based on token requirements.

## Key Components

### AI Models Configuration

The module defines three primary Anthropic Claude models with priority-based fallback:

- **Claude 4 Sonnet** (Priority 1): Latest and most capable model
- **Claude 3.7 Sonnet** (Priority 2): Secondary choice with same capabilities  
- **Claude 3.5 Sonnet** (Priority 3): Fallback option

Each model configuration includes:
- Full model name for API calls
- Context window size (200K tokens)
- Maximum output tokens (64K)
- Priority ranking for automatic selection

### Token Management Strategy

Implements intelligent token management with:
- Safety margins to prevent context overflow
- Automatic model selection based on content size
- Real-world overhead calculations for Aider integration
- Fallback mechanisms for oversized content

### Command Templates

Provides standardized Aider command templates for:
- **CHANGELOG**: Automated changelog generation
- **DOC_UI_REACT**: React component documentation
- **DOC_UI_SASS**: SASS/CSS documentation
- **DOC_UI_STORYBOOK**: Storybook documentation
- **DOC_GEN**: General documentation generation

## Main Functions and Classes

### Model Selection Functions

#### `get_model_by_priority(priority: int = 1) -> Optional[Dict[str, Any]]`

**Purpose**: Retrieves model configuration by priority ranking.

**Parameters**:
- `priority` (int): Model priority level (1 = highest priority)

**Returns**: Dictionary containing model configuration with key, name, token limits, and priority, or None if not found.

**Example**:
```python
model = get_model_by_priority(1)
print(model["name"])  # anthropic/claude-4-sonnet-20250514
```

#### `select_model_by_tokens(token_count: int) -> Dict[str, Any]`

**Purpose**: Automatically selects the most appropriate model based on token requirements.

**Parameters**:
- `token_count` (int): Number of tokens needed for the operation

**Returns**: Dictionary containing the selected model configuration.

**Example**:
```python
# For large content requiring 150K tokens
model = select_model_by_tokens(150000)
print(f"Selected: {model['key']}")  # CLAUDE_4_SONNET

# For smaller content
model = select_model_by_tokens(50000)
print(f"Selected: {model['key']}")  # CLAUDE_4_SONNET (still best choice)
```

### Token Management Functions

#### `get_effective_token_limit(model_key: str) -> int`

**Purpose**: Calculates the actual available tokens for content after reserving space for AI response and system overhead.

**Parameters**:
- `model_key` (str): Model identifier (e.g., "CLAUDE_4_SONNET")

**Returns**: Integer representing effective token limit for input content.

**Calculation**: `(context_window - max_output_tokens - prompt_overhead) * safety_margin`

**Example**:
```python
limit = get_effective_token_limit("CLAUDE_4_SONNET")
print(limit)  # 124450 tokens available for git log content
# Calculation: (200K - 64K - 5K) * 0.95 = 124.45K
```

### Command Generation Functions

#### `build_aider_command(command_type: str, model_key: str, **kwargs) -> str`

**Purpose**: Constructs complete Aider commands based on predefined templates and parameters.

**Parameters**:
- `command_type` (str): Template type ("CHANGELOG", "DOC_UI_REACT", etc.)
- `model_key` (str): Model to use for the operation
- `**kwargs`: Additional parameters for command template substitution

**Returns**: Complete Aider command string with expanded file flags.

**Example**:
```python
# Generate changelog command
cmd = build_aider_command(
    "CHANGELOG", 
    "CLAUDE_4_SONNET",
    log_file="git.log",
    prompt_file="changelog.prompt",
    output_file="CHANGELOG.md"
)

# Generate React documentation command with multiple files
cmd = build_aider_command(
    "DOC_UI_REACT",
    "CLAUDE_4_SONNET", 
    context_path="src/components/README.md",
    prompt_file="react.prompt",
    react_files="Button.tsx Card.tsx Modal.tsx"
)
# Result: --file Button.tsx --file Card.tsx --file Modal.tsx
```

### Utility Functions

#### `get_all_model_names() -> List[str]`

**Purpose**: Returns list of all available model names for API calls.

**Example**:
```python
models = get_all_model_names()
# ['anthropic/claude-4-sonnet-20250514', 'anthropic/claude-3-7-sonnet-latest', ...]
```

#### `get_cli_model_choices() -> List[str]`

**Purpose**: Returns model keys sorted by priority for CLI option presentation.

**Example**:
```python
choices = get_cli_model_choices()
# ['CLAUDE_4_SONNET', 'CLAUDE_3_7_SONNET', 'CLAUDE_3_5_SONNET']
```

## Dependencies & Imports

### Standard Library
- `typing`: Type hints for function signatures and return types
- `re`: Regular expressions for command string processing

### Internal Dependencies
- Part of `src/constants` module alongside:
  - `git.py`: Git operation constants
  - `output.py`: Output formatting constants  
  - `project.py`: Project-specific constants

### External Dependencies
- **Anthropic API**: Requires valid API credentials for model access
- **Aider**: Command-line AI coding assistant tool
- **Git**: Version control system for subtree operations

## Configuration Constants

### AI_MODELS Dictionary

```python
AI_MODELS = {
    "CLAUDE_4_SONNET": {
        "name": "anthropic/claude-4-sonnet-20250514",
        "max_tokens": 200000,
        "max_output_tokens": 64000,
        "priority": 1
    },
    # ... additional models
}
```

### TOKEN_STRATEGY Configuration

```python
TOKEN_STRATEGY = {
    "SAFETY_MARGIN": 0.95,        # Use 95% of model capacity
    "PROMPT_OVERHEAD": 5000,       # Aider system overhead
    "AUTO_MODEL_SELECTION": True,  # Enable automatic selection
    "SIMPLE_LOG_FALLBACK": True    # Fallback for oversized content
}
```

### AIDER_BASE_FLAGS

Standard flags applied to all Aider commands:
- `--subtree-only`: Limit to current git subtree
- `--yes`: Non-interactive mode
- `--no-stream`: Clean log output
- `--no-check-update`: Prevent interruptions
- `--map-tokens 0`: Disable token mapping for performance

## Usage Examples

### Basic Model Selection

```python
from src.constants.ai import get_model_by_priority, select_model_by_tokens

# Get default model (highest priority)
default_model = get_model_by_priority(1)
print(f"Using: {default_model['name']}")

# Select model based on content size
large_content_tokens = 180000
selected_model = select_model_by_tokens(large_content_tokens)
print(f"Selected: {selected_model['key']} for {large_content_tokens} tokens")
```

### Command Generation Workflow

```python
from src.constants.ai import build_aider_command, get_effective_token_limit

# Check if content fits in model
model_key = "CLAUDE_4_SONNET"
content_tokens = 100000
limit = get_effective_token_limit(model_key)

if content_tokens <= limit:
    # Generate documentation command
    cmd = build_aider_command(
        "DOC_GEN",
        model_key,
        context_files="src/utils/helpers.py src/utils/validators.py",
        prompt_file="doc_generation.prompt", 
        output_file="utils_documentation.md"
    )
    print(f"Command: {cmd}")
else:
    print("Content too large, consider splitting or using simple fallback")
```

### Multi-File Documentation

```python
# Document multiple React components
react_files = [
    "src/components/Button.tsx",
    "src/components/Card.tsx", 
    "src/components/Modal.tsx"
]

cmd = build_aider_command(
    "DOC_UI_REACT",
    "CLAUDE_4_SONNET",
    context_path="src/components/README.md",
    prompt_file="react_docs.prompt",
    react_files=" ".join(react_files)
)

# Command automatically expands to:
# --file src/components/Button.tsx --file src/components/Card.tsx --file src/components/Modal.tsx
```

## Implementation Notes

### Token Calculation Strategy

The module uses a conservative approach to token management:

1. **Safety Margin**: Uses 95% of model capacity to prevent overflow
2. **Real Overhead**: Based on actual Aider usage (5K tokens) rather than estimates
3. **Output Reservation**: Reserves 64K tokens for AI responses
4. **Dynamic Selection**: Automatically chooses appropriate model based on content size

### Command Template Design

Command templates support flexible parameter substitution:

- **Base Flags**: Applied to all commands for consistency
- **Additional Flags**: Template-specific flags with array format support
- **File Expansion**: Automatically expands multi-file parameters
- **Pattern Substitution**: Uses Python string formatting for parameter injection

### Model Priority System

Priority-based fallback ensures reliability:

1. **Primary**: Claude 4 Sonnet (latest capabilities)
2. **Secondary**: Claude 3.7 Sonnet (proven reliability)
3. **Fallback**: Claude 3.5 Sonnet (stable baseline)

### Error Handling

The module includes robust error handling:

- **Unknown Models**: Raises ValueError for invalid model keys
- **Token Overflow**: Returns largest available model as fallback
- **Missing Templates**: Validates command types before execution

### Performance Considerations

- **Token Mapping Disabled**: `--map-tokens 0` improves performance
- **No Streaming**: `--no-stream` reduces overhead for batch operations
- **Subtree Only**: `--subtree-only` limits file scanning scope

## Known Limitations

1. **Model Availability**: Depends on Anthropic API availability and quotas
2. **Token Estimation**: Uses approximations; actual usage may vary
3. **Command Length**: Very long file lists may exceed shell limits
4. **Git Dependency**: Requires git repository for subtree operations

## Future Improvement Opportunities

1. **Dynamic Token Counting**: Real-time token counting for precise limits
2. **Model Health Checking**: API availability verification before selection
3. **Caching Strategy**: Cache model responses for repeated operations
4. **Parallel Processing**: Support for concurrent documentation generation
5. **Custom Templates**: User-defined command templates for specialized workflows

## See Also

- [Git Constants](git.md) - Git operation configuration
- [Output Constants](output.md) - Output formatting standards
- [Project Constants](project.md) - Project-specific settings
- [Constants Module](../README.md) - Overview of constants directory
