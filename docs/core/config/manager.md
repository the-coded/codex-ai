# Configuration Manager Documentation

## Overview

The `manager.py` file implements a comprehensive configuration management system for Codex-AI that supports hierarchical configuration loading with clear priority ordering. This module provides a centralized way to manage application settings from multiple sources including CLI arguments, environment variables, configuration files, and built-in defaults.

The configuration manager follows a strict priority hierarchy:
1. CLI arguments (highest priority)
2. Environment variables (CODEX_* prefixed)
3. Global config file (~/.config/codex-ai/config.env)
4. Built-in defaults (lowest priority)

## Main Classes

### CodexConfig

The primary configuration management class that handles loading, parsing, and retrieving configuration values from multiple sources.

#### Key Methods

##### `__init__(self)`
- **Purpose**: Initializes the configuration manager and loads global configuration
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Loads configuration from ~/.config/codex-ai/config.env if it exists

##### `get(self, key: str, default: Any = None, cli_value: Any = None) -> Any`
- **Purpose**: Retrieves configuration values with hierarchical priority
- **Parameters**:
  - `key`: Configuration key to retrieve
  - `default`: Default value if key not found in any source
  - `cli_value`: CLI argument value (takes highest priority)
- **Returns**: Configuration value with appropriate type conversion
- **Example**:

```python
config = CodexConfig()
# Get with CLI override
verbose = config.get('verbose', default=False, cli_value=True)
# Get from environment or config file
timeout = config.get('timeout', default=30)
```

##### `get_api_key(self, cli_value: Optional[str] = None) -> Optional[str]`
- **Purpose**: Retrieves Anthropic API key with special handling for standard environment variables
- **Parameters**: 
  - `cli_value`: Optional CLI-provided API key
- **Returns**: API key string or None if not found
- **Priority**: CLI → ANTHROPIC_API_KEY env var → global config → None

##### `get_default_model(self, cli_value: Optional[str] = None) -> str`
- **Purpose**: Gets the default AI model to use
- **Parameters**: 
  - `cli_value`: Optional CLI-provided model name
- **Returns**: Model name string (defaults to 'claude_4_sonnet')

##### `get_fallback_models(self, cli_value: Optional[List[str]] = None) -> List[str]`
- **Purpose**: Gets list of fallback AI models
- **Parameters**: 
  - `cli_value`: Optional CLI-provided model list
- **Returns**: List of model names
- **Default**: ['claude_3_7_sonnet', 'claude_3_5_sonnet']

##### `get_model_max_tokens(self, model: str) -> int`
- **Purpose**: Gets maximum token limit for specified AI model
- **Parameters**: 
  - `model`: Model name to look up
- **Returns**: Maximum token count (defaults to 200000 for unknown models)
- **Dependencies**: Uses `get_model_token_limits()` from constants.ai

## Configuration File Format

The global configuration file (~/.config/codex-ai/config.env) uses a simple key=value format:

```
# Codex-AI Configuration
ANTHROPIC_API_KEY=your_api_key_here
default_model=claude_4_sonnet
verbose=true
output_dir=./output
git_timeout=60
fallback_models=claude_3_7_sonnet,claude_3_5_sonnet
```

## Dependencies

### External Dependencies
- `os`: Environment variable access
- `pathlib.Path`: File system path handling
- `typing`: Type hints (Dict, Any, Optional, List)

### Internal Dependencies
- `constants.ai.get_model_token_limits`: AI model token limit data
- `constants.ai.get_default_model_name`: Default model name retrieval

## Environment Variables

### Standard Environment Variables
- `ANTHROPIC_API_KEY`: Anthropic API key (standard pipeline variable)

### Codex-Specific Environment Variables
All configuration keys can be set via environment variables with the `CODEX_` prefix:
- `CODEX_VERBOSE`: Enable verbose output
- `CODEX_OUTPUT_DIR`: Output directory path
- `CODEX_DEFAULT_MODEL`: Default AI model
- `CODEX_GIT_TIMEOUT`: Git command timeout
- `CODEX_AI_RETRY_ATTEMPTS`: AI API retry attempts

## Usage Examples

### Basic Configuration Setup

```python
from core.config.manager import get_config

# Get global config instance
config = get_config()

# Get API key with CLI override
api_key = config.get_api_key(cli_value=args.api_key)

# Get verbose setting
verbose = config.get_verbose(cli_value=args.verbose)

# Get model configuration
model = config.get_default_model(cli_value=args.model)
fallbacks = config.get_fallback_models()
```

### Custom Configuration Values

```python
# Get custom configuration with fallback
custom_setting = config.get('custom_setting', default='default_value')

# Get with CLI override
timeout = config.get('timeout', default=30, cli_value=args.timeout)

# Boolean configuration
debug_mode = config.get('debug_mode', default=False)
```

### Working with Lists

```python
# Get list configuration (comma-separated in env/config file)
exclude_patterns = config.get_git_exclude_patterns()
# Returns: ['*.lock', 'dist/**', 'node_modules/**']

# Override with CLI
custom_patterns = config.get_git_exclude_patterns(
    cli_value=['*.tmp', '*.log']
)
```

## Type Conversion

The configuration manager automatically converts string values from environment variables and config files:

### Boolean Values
- `true`, `yes`, `on`, `1` → `True`
- `false`, `no`, `off`, `0` → `False`

### Numeric Values
- Strings containing `.` → `float`
- Integer strings (except `0`, `1`) → `int`
- `0`, `1` are treated as booleans

### List Values
- Comma-separated strings → `List[str]`
- Example: `"item1,item2,item3"` → `["item1", "item2", "item3"]`

## Global Configuration Instance

The module provides a singleton pattern for configuration access:

```python
# Get the global configuration instance
config = get_config()

# Set a custom configuration instance (for testing)
custom_config = CodexConfig()
set_config(custom_config)
```

## Implementation Notes

### Design Decisions
- **Hierarchical Priority**: Clear precedence order prevents configuration conflicts
- **Type Conversion**: Automatic type inference from string values
- **Singleton Pattern**: Global instance ensures consistent configuration across the application
- **Manual File Parsing**: Avoids external dependencies like python-dotenv

### Performance Considerations
- Configuration file is loaded once during initialization
- Environment variables are accessed on-demand
- Type conversion is performed for each access (consider caching for high-frequency access)

### Error Handling
- Missing configuration files are handled gracefully
- Invalid configuration values fall back to defaults
- Type conversion errors default to string values

### Known Limitations
- Configuration file format is simple key=value (no sections or complex structures)
- No configuration validation or schema enforcement
- Type inference may not handle all edge cases correctly

## Configuration Options Reference

### Core Settings
- `default_model`: Default AI model name
- `fallback_models`: Comma-separated list of fallback models
- `output_format`: Output format (default: 'markdown')
- `output_dir`: Output directory (default: '.tmp')
- `verbose`: Enable verbose logging (default: False)

### Timeout Settings
- `git_timeout`: Git command timeout in seconds (default: 30)
- `ai_timeout`: AI API timeout in seconds (default: 120)
- `ai_retry_attempts`: Number of AI API retry attempts (default: 3)

### Feature Flags
- `cache_enabled`: Enable caching (default: True)
- `parallel_processing`: Enable parallel processing (default: True)

### Git Integration
- `git_exclude_patterns`: Patterns to exclude from Git operations

## See Also
- [Constants AI Module](../constants/ai.md) - AI model definitions and limits
- [Core Configuration](./README.md) - Configuration module overview
- [Environment Setup Guide](../../../docs/setup.md) - Initial configuration setup
