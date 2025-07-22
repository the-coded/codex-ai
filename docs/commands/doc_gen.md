# Doc-Gen Command Documentation

## Overview

The `doc_gen.py` module implements the Doc-Gen command, a comprehensive AI-powered documentation generation system for software projects. This command can automatically generate documentation for any programming language or project type using intelligent file detection, customizable output strategies, and AI-driven content creation.

The module serves as the core implementation for the `codex-ai doc-gen` CLI command, providing both simple folder-level documentation and detailed file-by-file documentation generation capabilities.

## Key Features

- **Universal Language Support**: Works with any programming language through configurable presets
- **Intelligent File Detection**: Automatic Git-based file discovery with multiple detection modes
- **Flexible Output Strategies**: Supports both separated (`docs/`) and inline (`./docs/`) documentation structures
- **AI-Powered Generation**: Uses advanced AI models to create contextual, high-quality documentation
- **Customizable Filtering**: Preset-based and custom file filtering with extension and exclusion patterns
- **Token Management**: Built-in token counting and limit validation to prevent API overuse

## Main Components

### Core Functions

#### `run_doc_gen()`
The primary entry point for documentation generation.

- **Purpose**: Orchestrates the entire documentation generation process
- **Parameters**:
  - `mode`: Documentation mode ('simple' or 'detailed')
  - `git_mode`: Git detection mode ('local', 'pipeline', or None for auto-detect)
  - `path`: Specific directory/file path to process
  - `shallow`: Process only immediate directory (no recursion)
  - `docs_dir`: Output directory for documentation
  - `strip_prefix`: Comma-separated prefixes to remove from paths
  - `preset`: File preset ('python', 'javascript', or None for all)
  - `ext`: Comma-separated custom extensions
  - `exclude`: Comma-separated custom exclusions
  - `since_commit`: For pipeline mode - compare since this commit
  - `model_name`: AI model to use
  - `verbose`: Enable verbose output
  - `dry_run`: Preview mode without AI generation
- **Returns**: `bool` - True if successful, False otherwise

#### `detect_doc_gen_files()`
Filters files based on doc-gen criteria using presets and custom filters.

- **Purpose**: Identifies relevant files for documentation generation
- **Parameters**:
  - `files`: List of file paths to filter
  - `preset`: Preset name or None for default
  - `custom_extensions`: Custom extensions to override preset
  - `custom_excludes`: Custom excludes to override preset
- **Returns**: `List[str]` - Filtered list of relevant files

#### `map_output_paths()`
Maps input files to output documentation paths based on strategy and mode.

- **Purpose**: Determines where documentation files should be created
- **Parameters**:
  - `files`: List of input file paths
  - `mode`: Documentation mode ('simple' or 'detailed')
  - `docs_dir`: Documentation directory
  - `strip_prefixes`: List of prefixes to remove from paths
- **Returns**: `Dict[str, Dict[str, Any]]` - Mapping of folder paths to documentation info

### AI Generation Functions

#### `generate_folder_readme()`
Generates README.md files for folders using AI.

- **Purpose**: Creates comprehensive folder-level documentation
- **Parameters**:
  - `folder_path`: Path to the folder being documented
  - `folder_files`: List of files in the folder
  - `readme_path`: Output path for README.md
  - `strategy`: Output strategy ('separated' or 'inline')
  - `model`: AI model instance
  - `verbose`: Enable verbose output
- **Returns**: `bool` - True if generation successful

#### `generate_file_documentation()`
Generates detailed documentation for individual files.

- **Purpose**: Creates comprehensive file-level documentation
- **Parameters**:
  - `file_path`: Path to the file being documented
  - `doc_path`: Output path for documentation
  - `folder_path`: Parent folder path for context
  - `model`: AI model instance
  - `verbose`: Enable verbose output
- **Returns**: `bool` - True if generation successful

### Configuration and Presets

#### File Presets
The module includes predefined file filtering presets:

```python
DOC_GEN_PRESETS = {
    "python": {
        "extensions": [".py", ".pyi", ".yaml", ".toml"],
        "exclude": ["*.pyc", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info", "__init__.py"],
        "description": "Python files and configuration"
    },
    "javascript": {
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".json", ".mjs"],
        "exclude": ["node_modules", "*.min.js", "*.min.css", "*.map", "build", "dist", ".next", "index.js"],
        "description": "JavaScript/TypeScript files and configuration"
    },
    "generic": {
        "extensions": [".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".bash"],
        "exclude": [".git", ".tmp", "*.log", ".DS_Store", "Thumbs.db", ".vscode", ".idea", "__init__.py"],
        "description": "Documentation and configuration files"
    }
}
```

## Dependencies

### External Dependencies
- **pathlib**: Modern path handling
- **shutil**: File operations and cleanup
- **os**: Operating system interface

### Internal Dependencies
- **core.git**: Git integration and file detection
- **core.ai.model_selector**: AI model selection and management
- **core.ai.token_manager**: Token counting and validation
- **core.ai.aider_interface**: AI generation interface
- **core.ai.prompt_processor**: Template loading and processing
- **core.config**: Configuration management
- **constants.ai**: AI-related constants and templates
- **constants.output**: Output formatting utilities

## Usage Examples

### Basic Documentation Generation

```bash
# Generate simple documentation (README per folder)
codex-ai doc-gen --mode simple

# Generate detailed documentation (README + individual file docs)
codex-ai doc-gen --mode detailed

# Use specific preset for Python projects
codex-ai doc-gen --mode detailed --preset python
```

### Advanced Usage

```bash
# Process specific directory with custom output
codex-ai doc-gen --path src/utils/ --mode detailed --docs-dir ./docs/

# Pipeline mode with custom commit range
codex-ai doc-gen --mode detailed --pipeline --since HEAD~5

# Custom file filtering
codex-ai doc-gen --mode detailed --ext .py,.js,.md --exclude *.pyc,node_modules

# Dry run to preview without AI costs
codex-ai doc-gen --mode detailed --dry-run --verbose
```

### Programmatic Usage

```python
from src.commands.doc_gen import run_doc_gen

# Generate documentation programmatically
success = run_doc_gen(
    mode="detailed",
    git_mode="local",
    docs_dir="docs/",
    preset="python",
    verbose=True,
    dry_run=False
)

if success:
    print("Documentation generated successfully!")
```

## Documentation Modes

### Simple Mode
- Generates one README.md per folder
- Provides overview of folder contents and structure
- Suitable for high-level project documentation
- Faster generation with lower token usage

### Detailed Mode
- Generates README.md per folder plus individual file documentation
- Creates comprehensive file-by-file documentation
- Suitable for API documentation and detailed technical references
- Higher token usage but more comprehensive coverage

## Output Strategies

### Separated Strategy (`--docs-dir docs/`)
- Creates documentation in separate docs directory
- Mirrors project structure: `docs/src/utils/README.md`
- Keeps documentation separate from source code
- Ideal for centralized documentation management

### Inline Strategy (`--docs-dir ./docs/`)
- Creates documentation within source directories
- Places docs alongside code: `src/utils/docs/README.md`
- Keeps documentation close to implementation
- Ideal for component-level documentation

## Implementation Notes

### Token Management
The module includes sophisticated token counting and validation:

```python
# Token calculation example
prompt_tokens = count_tokens(filled_template)
total_context_tokens = sum(count_tokens(file_content) for file_content in context_files)
estimated_input_tokens = prompt_tokens + total_context_tokens

if estimated_input_tokens > token_limit:
    print(f"⚠️ Files exceed token limit ({estimated_input_tokens:,} > {token_limit:,})")
```

### File Detection Logic
The module uses intelligent file detection with multiple strategies:

1. **Auto-detection**: Automatically chooses between local and pipeline modes
2. **Local mode**: Processes staged and modified files from Git status
3. **Pipeline mode**: Processes files changed since a specific commit
4. **Path mode**: Processes files in a specific directory path

### Error Handling
Comprehensive error handling ensures graceful degradation:

- File access errors are logged but don't stop processing
- AI generation failures are reported per folder
- Token limit violations skip problematic folders
- Partial success scenarios are clearly communicated

### Performance Considerations

- **File Limit**: Maximum 100 files per run to prevent excessive API usage
- **Token Validation**: Pre-generation token counting prevents API failures
- **Batch Processing**: Processes files by folder for optimal context
- **Cleanup**: Automatic cleanup of temporary files and Aider history

## Configuration Options

### Default Configuration

```python
DOC_GEN_DEFAULTS = {
    "docs_dir": "docs/",
    "strip_prefixes": ["src/"],
    "mode": "simple",
    "preset": None,  # None means merge all presets
    "shallow": False
}
```

### Validation Limits

```python
DOC_GEN_VALIDATION = {
    "max_files_per_run": 100,
    "supported_extensions": [
        ".py", ".pyi", ".js", ".ts", ".jsx", ".tsx", ".json", ".mjs",
        ".md", ".txt", ".yaml", ".yml", ".sh", ".bash", ".toml"
    ]
}
```

## CLI Integration

The module provides complete CLI integration through:

- **Argument Parser**: `add_doc_gen_arguments()` adds all CLI options
- **Command Handler**: `doc_gen_command()` processes CLI arguments
- **Help System**: `get_doc_gen_help()` provides comprehensive usage help

## Template System

The module uses a template-based approach for AI prompts:

```python
DOC_GEN_TEMPLATES = {
    "folder_readme": "templates/prompts/doc_gen_folder_readme_prompt.md",
    "folder_index": "templates/prompts/doc_gen_folder_index_prompt.md", 
    "file_detailed": "templates/prompts/doc_gen_file_detailed_prompt.md"
}
```

Templates are loaded and filled with context-specific information before being sent to the AI model.

## Future Improvements

- **Multi-language Support**: Enhanced language-specific documentation patterns
- **Custom Templates**: User-defined documentation templates
- **Incremental Updates**: Update only changed documentation
- **Integration Testing**: Automated testing of generated documentation quality
- **Performance Optimization**: Parallel processing for large codebases

## See Also

- [Doc-UI Command](doc_ui.md) - Interactive documentation generation
- [Changelog Command](changelog.md) - Automated changelog generation
- [Core Git Module](../core/git.md) - Git integration functionality
- [AI Interface](../core/ai/aider_interface.md) - AI generation interface
- [Configuration System](../core/config.md) - Project configuration management
