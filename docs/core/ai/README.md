# AI Core Module

## Overview

The AI core module (`src/core/ai`) provides the foundational AI integration layer for Codex-AI. This module abstracts AI model interactions, manages token counting and limits, processes prompts from templates, and provides a unified interface to the Aider AI coding assistant. It serves as the central hub for all AI-related operations in the project.

## Contents

- **token_manager.py**: Comprehensive token counting and management system with support for multiple estimation methods (Anthropic API, tiktoken, fallback ratios). Handles token validation, model selection based on limits, and provides utilities for analyzing token usage across files.

- **model_selector.py**: Simple model selection logic that chooses the most cost-effective AI model based on token requirements. Implements a tiered approach (Claude-3.5 → Claude-3.7 → Claude-4) to optimize costs while ensuring adequate capacity.

- **aider_interface.py**: High-level interface to the Aider AI coding assistant. Provides templated command execution for common tasks like changelog generation and documentation creation, with automatic markdown post-processing and comprehensive error handling.

- **prompt_processor.py**: Template-based prompt loading system that retrieves prompt templates from markdown files. Supports multiple fallback strategies for different deployment scenarios (package installation, development mode, relative paths).

## Architecture

The AI core module follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│                 (Commands, Workflows)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   AI Interface Layer                        │
│              (aider_interface.py)                          │
│  • Command templating    • Result processing               │
│  • Execution management  • Error handling                  │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
┌─────────────▼─────────────┐   ┌─────────▼─────────────┐
│     Model Management      │   │   Prompt Management   │
│   (model_selector.py)     │   │ (prompt_processor.py) │
│ • Cost optimization       │   │ • Template loading    │
│ • Capacity planning       │   │ • Fallback strategies │
└─────────────┬─────────────┘   └───────────────────────┘
              │
┌─────────────▼─────────────┐
│    Token Management       │
│   (token_manager.py)      │
│ • Accurate counting       │
│ • Limit validation        │
│ • Usage analysis          │
└───────────────────────────┘
```

### Key Dependencies

- **External**: `anthropic`, `tiktoken` (optional), `subprocess` for Aider execution
- **Internal**: `constants.ai` for model configurations and command templates
- **Configuration**: Environment variables (`ANTHROPIC_API_KEY`) and global config system

### Data Flow

1. **Token Analysis**: Files are analyzed for token count using the most accurate available method
2. **Model Selection**: Optimal model is chosen based on token requirements and cost considerations  
3. **Prompt Loading**: Templates are loaded from markdown files with fallback strategies
4. **Command Execution**: Aider commands are built from templates and executed with proper error handling
5. **Result Processing**: Outputs are post-processed (e.g., markdown code block conversion) and returned

## Usage

### Basic Token Counting

```python
from core.ai.token_manager import get_token_count, get_token_count_from_text

# Count tokens in a file
token_count = get_token_count("path/to/file.py")

# Count tokens in text
text_tokens = get_token_count_from_text("Hello, world!")

# Get comprehensive analysis
from core.ai.token_manager import get_token_count_summary
summary = get_token_count_summary(["file1.py", "file2.md"])
print(f"Total tokens: {summary['total_tokens']}")
print(f"Recommended model: {summary['recommended_model']}")
```

### Model Selection

```python
from core.ai.model_selector import get_model_for_tokens, get_default_model

# Get optimal model for token count
model = get_model_for_tokens(150000)  # Returns Claude-3.5 (most economical)

# Get default model
default_model = get_default_model()  # Returns Claude-4 Sonnet
```

### Aider Integration

```python
from core.ai.aider_interface import AiderInterface
from core.ai.model_selector import get_model_for_tokens

# Initialize with appropriate model
model = get_model_for_tokens(50000)
aider = AiderInterface(model)

# Generate changelog
result = aider.run_changelog(
    log_file="git_log.txt",
    prompt_file="changelog_prompt.md", 
    output_file="CHANGELOG.md"
)

# Custom Aider execution
result = aider.run_custom(
    prompt="Refactor this function for better readability",
    files=["src/utils.py"],
    read_files=["docs/style_guide.md"]
)

if result.success:
    print("✅ Aider completed successfully")
else:
    print(f"❌ Aider failed: {result.error}")
```

### Prompt Management

```python
from core.ai.prompt_processor import load_prompt, get_changelog_prompt

# Load specific prompt template
prompt = load_prompt("custom_task_prompt")

# Load predefined prompts
changelog_prompt = get_changelog_prompt()
react_prompt = get_react_prompt()
```

## Implementation Details

### Token Counting Strategy

The token manager implements a three-tier approach for maximum accuracy:

1. **Primary**: Anthropic API (`messages.count_tokens`) - Most accurate for Claude models
2. **Secondary**: tiktoken library with Claude correction factor (~10-15% adjustment)
3. **Fallback**: Content-aware character ratios (code: 3.2, markdown: 3.8, text: 4.0)

### Model Selection Logic

Cost optimization follows a tiered approach:
- **Claude-3.5 Sonnet**: Up to 200K tokens (most economical)
- **Claude-3.7 Sonnet**: Up to 500K tokens (balanced performance/cost)  
- **Claude-4 Sonnet**: Up to 1M tokens (premium, highest capability)

### Aider Command Templates

Commands are built from templates in `constants.ai` with parameter substitution:

```python
# Template example
AIDER_COMMANDS = {
    "CHANGELOG": {
        "CLAUDE_4_SONNET": [
            ["--model", "{model_name}"],
            ["--read", "{log_file}"],
            ["--message-file", "{prompt_file}"],
            ["--file", "{output_file}"]
        ]
    }
}
```

### Error Handling

- **Graceful Degradation**: Falls back to less accurate methods when APIs fail
- **Timeout Management**: 10-minute timeout for Aider operations
- **Comprehensive Logging**: Detailed error reporting with context
- **Resource Cleanup**: Proper handling of subprocess resources

### Markdown Post-Processing

Automatic conversion of ````` markers to standard triple backticks prevents Aider from incorrectly parsing generated markdown as multiple files.

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Required for API-based token counting and Aider execution
- Standard shell environment for subprocess execution

### File Dependencies

- `templates/prompts/*.md`: Prompt template files
- `constants/ai.py`: Model configurations and command templates
- Global configuration system for API key management

## Performance Considerations

- **Token Counting**: API calls are cached where possible; fallback methods are fast
- **Model Selection**: Lightweight logic with minimal computational overhead
- **Aider Execution**: Subprocess management with proper timeout and resource handling
- **Memory Usage**: Efficient text processing with minimal memory footprint

## Error Recovery

The module implements comprehensive error recovery:

- **API Failures**: Automatic fallback to local estimation methods
- **File Access**: Graceful handling of missing or unreadable files
- **Subprocess Errors**: Detailed error capture and reporting
- **Template Loading**: Multiple fallback paths for different deployment scenarios
