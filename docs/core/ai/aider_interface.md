# Aider Interface Documentation

## Overview

The `aider_interface.py` file provides a comprehensive Python interface for executing Aider commands within the Codex-AI project. Aider is an AI-powered coding assistant that can modify code files based on natural language prompts. This interface abstracts the complexity of building and executing Aider commands, providing a clean API for various documentation generation and code modification tasks.

The interface serves as the primary bridge between the Codex-AI application and the Aider tool, handling command construction, execution, and result processing with support for multiple AI models and specialized workflows.

## Main Classes and Functions

### AiderResult (Dataclass)

A data structure that encapsulates the results of Aider command execution.

- **Purpose**: Standardize the return format for all Aider operations
- **Fields**:
  - `success: bool` - Whether the command executed successfully
  - `output: str` - Standard output from the Aider command
  - `error: str` - Error output if the command failed
  - `command: str` - The actual command that was executed

```python
@dataclass
class AiderResult:
    success: bool
    output: str
    error: str
    command: str
```

### AiderInterface (Main Class)

The core class that manages Aider command execution with AI model integration.

#### Constructor

```python
def __init__(self, model: ModelInfo, api_key: Optional[str] = None):
    """Initialize with model and API key."""
```

- **Parameters**:
  - `model: ModelInfo` - AI model configuration object
  - `api_key: Optional[str]` - API key for the AI service (optional, can be retrieved from config or environment)

#### Core Methods

##### run_changelog()

Generates changelog documentation from git logs.

```python
def run_changelog(self, log_file: str, prompt_file: str, output_file: str) -> AiderResult:
```

- **Purpose**: Generate changelog from git log using AI
- **Parameters**:
  - `log_file: str` - Path to git log file
  - `prompt_file: str` - Path to prompt template file
  - `output_file: str` - Path where changelog will be written
- **Returns**: `AiderResult` with execution details

##### run_doc_ui_react()

Generates React component documentation.

```python
def run_doc_ui_react(self, context_path: str, prompt_file: str, react_files: str) -> AiderResult:
```

- **Purpose**: Generate documentation for React components
- **Parameters**:
  - `context_path: str` - Path to context documentation
  - `prompt_file: str` - Path to prompt template
  - `react_files: str` - React files to process
- **Returns**: `AiderResult` with execution details

##### run_doc_ui_sass()

Generates Sass/SCSS documentation.

```python
def run_doc_ui_sass(self, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
```

- **Purpose**: Generate documentation for Sass/SCSS files
- **Parameters**: Similar to React documentation method
- **Returns**: `AiderResult` with execution details

##### run_doc_ui_storybook()

Generates Storybook documentation.

```python
def run_doc_ui_storybook(self, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
```

- **Purpose**: Generate documentation for Storybook files
- **Parameters**: Similar to other documentation methods
- **Returns**: `AiderResult` with execution details

##### run_with_message_file()

Generic method for running Aider with message files and flexible parameters.

```python
def run_with_message_file(
    self, 
    prompt_file: str, 
    read_files: List[str] = None, 
    output_files: List[str] = None,
    additional_flags: List[List[str]] = None,
    verbose: bool = False
) -> AiderResult:
```

- **Purpose**: Flexible Aider execution with customizable parameters
- **Parameters**:
  - `prompt_file: str` - Path to prompt file
  - `read_files: List[str]` - Files to read for context (optional)
  - `output_files: List[str]` - Files to write/modify (optional)
  - `additional_flags: List[List[str]]` - Additional command flags (optional)
  - `verbose: bool` - Enable verbose logging
- **Returns**: `AiderResult` with execution details

##### run_custom()

Execute Aider with custom parameters and inline prompts.

```python
def run_custom(self, prompt: str, files: List[str] = None, read_files: List[str] = None) -> AiderResult:
```

- **Purpose**: Run Aider with custom prompt text and file lists
- **Parameters**:
  - `prompt: str` - The prompt text to send to AI
  - `files: List[str]` - Files to modify (optional)
  - `read_files: List[str]` - Files to read for context (optional)
- **Returns**: `AiderResult` with execution details

#### Private Methods

##### _post_process_markdown_code_blocks()

Converts custom code block markers to standard markdown format.

- **Purpose**: Solve Aider's issue with triple backticks being interpreted as file delimiters
- **Process**: Converts ````` markers to standard ````` markdown syntax
- **Returns**: `bool` indicating success/failure

##### _auto_process_generated_markdown()

Automatically post-processes all markdown files mentioned in Aider commands.

- **Purpose**: Apply code block post-processing to all generated .md files
- **Trigger**: Called automatically after successful Aider execution
- **Scope**: Processes all files with .md extension found in --file flags

## Dependencies & Imports

### External Libraries
- `os` - Operating system interface for environment variables and file operations
- `re` - Regular expressions for pattern matching and text processing
- `subprocess` - Process execution for running Aider commands
- `typing` - Type hints for better code documentation and IDE support
- `dataclasses` - For creating the AiderResult data structure

### Internal Dependencies
- `constants.ai` - Contains Aider command templates and model mappings
  - `build_aider_command()` - Function to build commands from templates
  - `AIDER_BASE_FLAGS` - Base command line flags for Aider
  - `get_model_name_mapping()` - Maps model names to template keys
- `.model_selector.ModelInfo` - Model configuration data structure

### Environment Requirements
- **ANTHROPIC_API_KEY** - Environment variable for Anthropic API access
- **Aider CLI tool** - Must be installed and available in system PATH
- **Git** - Required for changelog generation functionality

## API Documentation

### Convenience Functions

The module provides several convenience functions for common operations:

```python
def run_changelog_generation(model: ModelInfo, log_file: str, prompt_file: str, output_file: str) -> AiderResult:
    """Generate changelog using Aider."""

def run_react_documentation(model: ModelInfo, context_path: str, prompt_file: str, react_files: str) -> AiderResult:
    """Generate React documentation using Aider."""

def run_sass_documentation(model: ModelInfo, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
    """Generate Sass documentation using Aider."""

def run_storybook_documentation(model: ModelInfo, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
    """Generate Storybook documentation using Aider."""

def run_doc_ui_generation(model: ModelInfo, file_type: str, files: List[str], prompt_file: str, output_dir: List[str], verbose: bool = False) -> AiderResult:
    """Generate documentation using Aider for specific file type."""
```

These functions provide a simplified interface for common documentation generation tasks without requiring direct instantiation of the AiderInterface class.

## Usage Examples

### Basic Changelog Generation

```python
from core.ai.aider_interface import AiderInterface, run_changelog_generation
from core.ai.model_selector import ModelInfo

# Using convenience function
model = ModelInfo(name="claude-3-sonnet-20240229", provider="anthropic")
result = run_changelog_generation(
    model=model,
    log_file="git_log.txt",
    prompt_file="prompts/changelog.md",
    output_file="CHANGELOG.md"
)

if result.success:
    print("Changelog generated successfully!")
else:
    print(f"Error: {result.error}")
```

### React Documentation Generation

```python
# Using the interface directly
interface = AiderInterface(model)
result = interface.run_doc_ui_react(
    context_path="docs/context.md",
    prompt_file="prompts/react_docs.md",
    react_files="src/components/*.tsx"
)

if result.success:
    print("React documentation generated!")
    print(f"Output: {result.output}")
```

### Custom Aider Execution

```python
# Custom prompt with specific files
interface = AiderInterface(model, api_key="your-api-key")
result = interface.run_custom(
    prompt="Add comprehensive JSDoc comments to all functions",
    files=["src/utils/helpers.js"],
    read_files=["docs/coding-standards.md"]
)
```

### Generic Message File Execution

```python
# Using the generic method with verbose logging
result = interface.run_with_message_file(
    prompt_file="prompts/refactor.md",
    read_files=["src/config.js", "docs/architecture.md"],
    output_files=["src/new-config.js"],
    verbose=True
)

# Check execution details
print(f"Command executed: {result.command}")
print(f"Success: {result.success}")
```

### Error Handling Pattern

```python
def safe_aider_execution(interface, operation_func, **kwargs):
    """Safely execute Aider operations with error handling."""
    try:
        result = operation_func(**kwargs)
        
        if result.success:
            print("✅ Operation completed successfully")
            return result
        else:
            print(f"❌ Operation failed: {result.error}")
            print(f"Command: {result.command}")
            return None
            
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")
        return None

# Usage
result = safe_aider_execution(
    interface,
    interface.run_changelog,
    log_file="git.log",
    prompt_file="changelog.md",
    output_file="CHANGELOG.md"
)
```

## Implementation Notes

### Design Decisions

1. **Command Template System**: The interface uses a template-based approach for building Aider commands, centralizing command construction logic in the `constants.ai` module.

2. **Model Abstraction**: The `ModelInfo` abstraction allows the interface to work with different AI models without hardcoding model-specific details.

3. **Result Standardization**: The `AiderResult` dataclass provides a consistent return format across all operations, making error handling and result processing uniform.

### Performance Considerations

1. **Timeout Management**: Commands have a 10-minute timeout to prevent hanging operations.

2. **Environment Isolation**: Each command runs with its own environment copy to avoid interference.

3. **Subprocess Management**: Uses `subprocess.run()` with proper timeout and output capture for reliable execution.

### Markdown Processing

The interface includes automatic post-processing for generated markdown files:

- **Problem**: Aider interprets triple backticks (```) as file delimiters, breaking markdown generation
- **Solution**: Uses custom ````` markers that are automatically converted to standard markdown
- **Process**: Automatic conversion happens after successful Aider execution

### Known Limitations

1. **Command Length**: Very long file lists may exceed command line length limits on some systems.

2. **API Key Management**: Currently supports Anthropic API keys; other providers may require additional configuration.

3. **Error Recovery**: Limited automatic retry mechanisms for transient failures.

### Future Improvement Opportunities

1. **Refactoring Opportunity**: The TODO comment in `run_with_message_file()` suggests consolidating the specialized methods (changelog, React, Sass, Storybook) to use the generic method, reducing code duplication.

2. **Enhanced Error Handling**: Could benefit from more sophisticated error categorization and recovery strategies.

3. **Streaming Output**: For long-running operations, streaming output could provide better user feedback.

4. **Caching**: Command results could be cached to avoid redundant AI calls for identical inputs.

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` - Required for Anthropic model access
- Additional model-specific API keys may be required based on the model used

### Global Configuration Integration

The interface integrates with the global configuration system:

```python
def _get_api_key_from_config(self) -> Optional[str]:
    """Get API key from global config."""
    try:
        from core.config import get_config
        config = get_config()
        if config:
            return config.get_api_key()
    except Exception:
        pass
    return None
```

This allows API keys to be managed centrally rather than requiring environment variables.

## See Also

- [Model Selector Documentation](model_selector.md) - AI model configuration and selection
- [Constants Documentation](../../constants/ai.md) - Aider command templates and configurations
- [Core Configuration](../config.md) - Global configuration management
- [AI Module Overview](README.md) - Overview of the AI integration module
