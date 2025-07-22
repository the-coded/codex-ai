# Prompt Processor Documentation

## Overview

The `prompt_processor.py` module serves as the central prompt management system for Codex-AI, providing a robust and flexible way to load and manage prompt templates from markdown files. This module acts as the bridge between the AI system and its prompt templates, offering multiple fallback mechanisms to ensure reliable prompt loading across different deployment scenarios.

The module is designed to handle various deployment contexts, from development environments to packaged installations, making it a critical component for maintaining consistent AI behavior across different runtime environments.

## Main Functions

### load_prompt(prompt_name: str) -> str

**Purpose**: Loads prompt content from markdown files using a multi-tier fallback system to ensure reliability across different deployment scenarios.

**Parameters**:
- `prompt_name` (str): Name of the prompt file without the `.md` extension

**Returns**: 
- `str`: The complete prompt content as a string, stripped of leading/trailing whitespace

**Fallback Strategy**:
1. **Package Resource Path**: Uses `pkg_resources` to locate prompts in installed packages
2. **Relative Path**: Falls back to relative path resolution for development mode
3. **Absolute Path**: Uses file location-based absolute path resolution
4. **Default Fallback**: Returns a basic prompt template if all else fails

**Example**:
```python
# Load a changelog generation prompt
changelog_content = load_prompt("changelog_prompt")
print(changelog_content)  # Outputs the full prompt template

# Load a custom prompt
custom_prompt = load_prompt("my_custom_prompt")
```

### get_changelog_prompt() -> str

**Purpose**: Convenience function to retrieve the changelog generation prompt template.

**Parameters**: None

**Returns**: 
- `str`: Changelog prompt content

**Example**:
```python
prompt = get_changelog_prompt()
# Use prompt for changelog generation
```

### get_doc_ui_prompt(doc_type: str) -> str

**Purpose**: Retrieves documentation prompts for UI components based on the specified documentation type.

**Parameters**:
- `doc_type` (str): Type of documentation prompt to load (e.g., "react", "sass", "storybook")

**Returns**: 
- `str`: UI documentation prompt content

**Example**:
```python
# Load React-specific documentation prompt
react_prompt = get_doc_ui_prompt("react")

# Load Sass-specific documentation prompt  
sass_prompt = get_doc_ui_prompt("sass")
```

### get_react_prompt() -> str

**Purpose**: Convenience function specifically for React documentation prompts.

**Parameters**: None

**Returns**: 
- `str`: React documentation prompt content

**Example**:
```python
react_docs_prompt = get_react_prompt()
```

### get_sass_prompt() -> str

**Purpose**: Convenience function specifically for Sass documentation prompts.

**Parameters**: None

**Returns**: 
- `str`: Sass documentation prompt content

**Example**:
```python
sass_docs_prompt = get_sass_prompt()
```

### get_storybook_prompt() -> str

**Purpose**: Convenience function specifically for Storybook documentation prompts.

**Parameters**: None

**Returns**: 
- `str`: Storybook documentation prompt content

**Example**:
```python
storybook_docs_prompt = get_storybook_prompt()
```

## Dependencies & Imports

### External Libraries
- **os**: Operating system interface utilities
- **pkg_resources**: Package resource management for installed packages
- **pathlib.Path**: Modern path handling and manipulation

### Internal Dependencies
- Part of the `codex_ai` package structure
- Expects prompt templates in `templates/prompts/` directory
- Integrates with other AI core modules in `src/core/ai/`

### File Structure Requirements
The module expects the following directory structure:
```
templates/
└── prompts/
    ├── changelog_prompt.md
    ├── doc_ui_react_prompt.md
    ├── doc_ui_sass_prompt.md
    ├── doc_ui_storybook_prompt.md
    └── [other_prompt_files].md
```

## Implementation Details

### Multi-Tier Fallback System

The `load_prompt` function implements a sophisticated fallback mechanism:

1. **Package Resource Resolution**: First attempts to load prompts using `pkg_resources.resource_filename()`, which works for installed packages
2. **Development Mode Fallback**: Falls back to relative path resolution for development environments
3. **Absolute Path Resolution**: Uses the current file's location to construct absolute paths
4. **Graceful Degradation**: Provides a basic prompt template if all file loading attempts fail

### Error Handling Strategy

The module uses nested try-catch blocks to handle various exception types:
- `FileNotFoundError`: When prompt files don't exist
- `pkg_resources.DistributionNotFound`: When package isn't properly installed
- `ModuleNotFoundError`: When the codex_ai package isn't available

### Path Resolution Logic

```python
# Example of the path resolution hierarchy:
# 1. Package resource path
prompt_path = pkg_resources.resource_filename('codex_ai', f'templates/prompts/{prompt_name}.md')

# 2. Relative path fallback
prompt_file = Path("templates/prompts") / f"{prompt_name}.md"

# 3. Absolute path based on file location
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
prompt_file = project_root / "templates/prompts" / f"{prompt_name}.md"
```

## Usage Examples

### Basic Prompt Loading

```python
from src.core.ai.prompt_processor import load_prompt, get_changelog_prompt

# Load any prompt by name
custom_prompt = load_prompt("my_analysis_prompt")

# Use convenience functions for common prompts
changelog_prompt = get_changelog_prompt()
```

### Integration with AI Processing

```python
from src.core.ai.prompt_processor import get_react_prompt, get_sass_prompt

def generate_documentation(file_type, content):
    if file_type == "react":
        prompt = get_react_prompt()
    elif file_type == "sass":
        prompt = get_sass_prompt()
    else:
        prompt = load_prompt(f"doc_ui_{file_type}_prompt")
    
    # Combine prompt with content for AI processing
    full_prompt = f"{prompt}\n\nContent to process:\n{content}"
    return full_prompt
```

### Error Handling in Applications

```python
def safe_prompt_loading(prompt_name):
    try:
        prompt = load_prompt(prompt_name)
        if prompt.startswith("Process the provided data"):
            # This indicates fallback was used
            print(f"Warning: Using fallback prompt for {prompt_name}")
        return prompt
    except Exception as e:
        print(f"Error loading prompt {prompt_name}: {e}")
        return "Please process the provided data."
```

## Implementation Notes

### Design Decisions

1. **Multiple Fallback Paths**: The module prioritizes reliability over simplicity, ensuring prompts can be loaded in various deployment scenarios
2. **Graceful Degradation**: Rather than failing completely, the system provides basic functionality even when prompt files are missing
3. **Convenience Functions**: Specific getter functions reduce the likelihood of typos and provide better IDE support

### Performance Considerations

- **File I/O Caching**: Each prompt is loaded fresh from disk on every call. Consider implementing caching for high-frequency usage
- **Path Resolution Overhead**: The fallback mechanism involves multiple file system checks, which could be optimized for production use
- **Memory Usage**: Prompt content is loaded entirely into memory as strings

### Known Limitations

1. **No Caching**: Prompts are re-read from disk on every access
2. **Limited Error Context**: Fallback prompts don't indicate which specific file failed to load
3. **Encoding Assumptions**: Assumes UTF-8 encoding for all prompt files
4. **No Validation**: Doesn't validate prompt content or structure

### Future Improvement Opportunities

1. **Prompt Caching**: Implement in-memory caching with optional cache invalidation
2. **Prompt Validation**: Add schema validation for prompt templates
3. **Dynamic Prompt Loading**: Support for runtime prompt registration and modification
4. **Metrics Integration**: Add logging and metrics for prompt loading performance
5. **Template Variables**: Support for parameterized prompt templates

### Testing Considerations

When testing this module, consider:
- Testing all fallback paths independently
- Verifying behavior with missing prompt files
- Testing in both development and packaged environments
- Validating UTF-8 encoding handling
- Performance testing with large prompt files

## Integration with Related Components

### token_manager.py
The prompt processor works closely with token management to ensure prompts fit within model context limits.

### aider_interface.py
Provides prompts that are specifically formatted for Aider AI interactions.

### model_selector.py
Different models may require different prompt formats, which this module can provide through specialized prompt files.

## See Also

- [Token Manager Documentation](token_manager.md)
- [Aider Interface Documentation](aider_interface.md)
- [AI Core Module Overview](../README.md)
- [Prompt Template Guidelines](../../templates/prompts/README.md)
