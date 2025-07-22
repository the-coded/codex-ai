# Commands Module

## Overview

The `src/commands` directory contains the core command implementations for the Codex-AI CLI tool. This module provides specialized AI-powered documentation generation commands that leverage Git integration, intelligent file detection, and advanced prompt engineering to create comprehensive project documentation.

Each command follows a consistent architectural pattern with mode detection, file filtering, token management, and AI generation capabilities, making them both powerful and user-friendly for different documentation workflows.

## Contents

- **changelog.py**: Generates AI-powered changelogs from Git commit history with intelligent version detection and token optimization
- **config.py**: Manages global configuration settings for API keys, models, output formats, and user preferences
- **doc_gen.py**: Provides generic documentation generation for any programming language with flexible presets and output strategies
- **doc_ui.py**: Specialized documentation generator for React, Sass, and Storybook files with cross-type triggers and sibling detection

## Architecture

### Common Patterns

All command modules follow a consistent architectural pattern:

```python
def run_command(args...) -> bool:
    """Main command logic with error handling"""
    
def command_handler(args):
    """CLI argument parser integration"""
    
def add_arguments(parser):
    """Argument parser configuration"""
    
def get_help() -> str:
    """Command help documentation"""
```

### Core Dependencies

The commands module integrates with several core systems:

- **Git Integration**: Uses `core.git` for file detection and change tracking
- **AI Processing**: Leverages `core.ai` for model selection, token management, and generation
- **Configuration**: Integrates with `core.config` for user preferences and settings
- **Constants**: Uses `constants.ai` and `constants.output` for consistent behavior

### File Detection Modes

Commands support multiple file detection strategies:

- **Local Mode**: Processes staged and modified files (`git status`)
- **Pipeline Mode**: Processes files changed since a specific commit or branch
- **Path Mode**: Processes specific directories or files directly
- **Auto-Detection**: Intelligently selects between local and pipeline modes

## Usage

### Basic Command Structure

```bash
codex-ai <command> [options]
codex-ai <command> --help
codex-ai <command> --dry-run --verbose
```

### Common Options

Most commands support these standard options:

- `--verbose, -v`: Enable detailed output for debugging
- `--dry-run`: Preview mode without AI costs
- `--model`: Specify AI model to use
- `--path`: Process specific directory/file path
- `--since`: For pipeline mode, compare since specific commit

### Configuration Management

```bash
# View current settings
codex-ai config --list

# Set API key
codex-ai config --api-key sk-ant-...

# Configure default model
codex-ai config --model claude-4-sonnet
```

### Documentation Generation

```bash
# Generate changelog
codex-ai changelog --dry-run

# Generate UI documentation
codex-ai doc-ui --doc react --verbose

# Generate generic documentation
codex-ai doc-gen --mode detailed --preset python
```

## Implementation Details

### Error Handling

All commands implement comprehensive error handling:

- Git availability checks
- File existence validation
- Token limit enforcement
- Model availability verification
- Graceful degradation for missing dependencies

### Token Management

Commands implement intelligent token optimization:

```python
# Calculate token usage before AI calls
prompt_tokens = count_tokens(prompt_content)
context_tokens = sum(count_tokens(file) for file in context_files)
total_tokens = prompt_tokens + context_tokens

if total_tokens > token_limit:
    # Implement fallback strategy
```

### Dry Run Support

All commands support preview mode for cost-free analysis:

- Shows files that would be processed
- Displays token usage estimates
- Previews AI prompts and commands
- Calculates potential costs without API calls

### Artifact Management

Commands properly manage temporary files and artifacts:

- Use `.tmp/` directory for working files
- Move Aider history to artifacts for pipeline integration
- Clean up temporary files after processing
- Preserve important logs for debugging

### Configuration Integration

Commands respect both global and local configuration:

```python
config = CodexConfig()
verbose = verbose or config.get_verbose()
model = model_name or config.get_default_model()
```

## Command-Specific Features

### Changelog Generation
- Intelligent version detection from Git tags
- Automatic range calculation between versions
- Token-optimized log generation with fallbacks
- Support for both tagged releases and development builds

### Configuration Management
- XDG Base Directory compliant configuration storage
- Secure API key handling with masking
- Validation for all configuration values
- Global configuration file management

### Generic Documentation
- Multi-language preset support (Python, JavaScript, Generic)
- Flexible output strategies (separated vs inline)
- Custom file filtering with extensions and exclusions
- Hierarchical documentation generation

### UI Documentation
- Cross-type trigger system (Component → React + Storybook)
- Intelligent sibling file detection
- Workspace-aware configuration discovery
- Component-centric documentation mapping

## Development Guidelines

### Adding New Commands

1. Follow the established architectural pattern
2. Implement comprehensive error handling
3. Add dry-run support for cost-free testing
4. Include verbose output for debugging
5. Integrate with the configuration system
6. Add comprehensive help documentation

### Testing Commands

```bash
# Always test with dry-run first
codex-ai <command> --dry-run --verbose

# Test with different modes
codex-ai <command> --local --dry-run
codex-ai <command> --pipeline --dry-run
codex-ai <command> --path src/ --dry-run
```

### Performance Considerations

- Implement token limit checks before AI calls
- Use file filtering to reduce processing overhead
- Cache expensive operations where possible
- Provide progress feedback for long-running operations

The commands module represents the user-facing interface of Codex-AI, providing powerful yet intuitive tools for AI-powered documentation generation across different use cases and project types.
