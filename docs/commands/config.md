# Configuration Management Command Documentation

## Overview

The `config.py` file implements the configuration management system for Codex-AI, providing a comprehensive interface for managing global application settings. It handles persistent storage of user preferences, API keys, AI model configurations, and various behavioral settings through a global configuration file located at `~/.config/codex-ai/config.env`.

This module serves as the primary interface between the CLI and the application's configuration system, supporting both interactive configuration updates and programmatic access to settings.

## Main Functions and Classes

### Configuration File Management

#### `get_global_config_path() -> Path`
- **Purpose**: Returns the path to the global configuration file following XDG Base Directory specification
- **Returns**: `Path` object pointing to `~/.config/codex-ai/config.env`
- **Side Effects**: Creates the configuration directory if it doesn't exist
- **Example**:
```python
config_path = get_global_config_path()
print(f"Config stored at: {config_path}")
# Output: Config stored at: /home/user/.config/codex-ai/config.env
```

#### `load_global_config() -> Dict[str, str]`
- **Purpose**: Loads current configuration from the global config file
- **Returns**: Dictionary mapping configuration keys to their string values
- **Behavior**: Ignores comments (lines starting with #) and malformed lines
- **Example**:
```python
config = load_global_config()
api_key = config.get('ANTHROPIC_API_KEY', '')
model = config.get('CODEX_DEFAULT_MODEL', 'claude-3-5-sonnet-20241022')
```

#### `save_global_config(config_data: Dict[str, str]) -> None`
- **Purpose**: Persists configuration data to the global config file
- **Parameters**: 
  - `config_data`: Dictionary of configuration key-value pairs
- **Behavior**: Writes sorted configuration with header comments
- **Example**:
```python
config_data = {
    'ANTHROPIC_API_KEY': 'sk-ant-...',
    'CODEX_DEFAULT_MODEL': 'claude-3-5-sonnet-20241022'
}
save_global_config(config_data)
```

#### `update_global_config(updates: Dict[str, str]) -> None`
- **Purpose**: Updates existing configuration with new values
- **Parameters**:
  - `updates`: Dictionary of configuration updates to apply
- **Behavior**: Merges updates with existing configuration before saving
- **Example**:
```python
updates = {'CODEX_VERBOSE': 'true', 'CODEX_OUTPUT_FORMAT': 'json'}
update_global_config(updates)
```

#### `reset_global_config() -> None`
- **Purpose**: Resets configuration to defaults by removing the config file
- **Side Effects**: Deletes the global configuration file if it exists
- **Output**: Prints success message to console

### Configuration Display and Validation

#### `show_current_config(config: CodexConfig) -> None`
- **Purpose**: Displays current configuration in a user-friendly format
- **Parameters**:
  - `config`: CodexConfig instance containing current settings
- **Features**:
  - Masks API keys for security (shows first 8 and last 4 characters)
  - Groups settings by category (API, AI, Output, Behavior, Performance)
  - Shows global config file location and existence status
- **Example Output**:
```
🔧 Current Codex-AI Configuration:

🔑 API Key: sk-ant-a...b123
🤖 Default Model: claude-3-5-sonnet-20241022
🔄 Fallback Models: claude-3-haiku-20240307
📄 Output Format: markdown
📁 Output Directory: ./output
```

### Validation Functions

#### `validate_model(model: str) -> bool`
- **Purpose**: Validates AI model names against supported models
- **Parameters**:
  - `model`: Model name to validate (case-insensitive)
- **Returns**: `True` if model is valid, `False` otherwise
- **Implementation**: Supports both uppercase and lowercase input

#### `validate_output_format(format_name: str) -> bool`
- **Purpose**: Validates output format against supported formats
- **Parameters**:
  - `format_name`: Format name to validate (case-insensitive)
- **Returns**: `True` if format is valid, `False` otherwise

#### `validate_boolean(value: str) -> bool`
- **Purpose**: Validates boolean string values
- **Parameters**:
  - `value`: String value to validate
- **Returns**: `True` if value is 'true' or 'false' (case-insensitive)

#### `parse_fallback_models(models_str: str) -> list`
- **Purpose**: Parses and validates comma-separated fallback model list
- **Parameters**:
  - `models_str`: Comma-separated string of model names
- **Returns**: List of validated model names
- **Raises**: `ValueError` if any model is invalid

### Main Command Handler

#### `run_config(args, config: CodexConfig) -> int`
- **Purpose**: Main entry point for configuration command execution
- **Parameters**:
  - `args`: Parsed command-line arguments
  - `config`: Current CodexConfig instance
- **Returns**: Exit code (0 for success, 1 for error)
- **Supported Operations**:
  - `--list`: Display current configuration
  - `--reset`: Reset to defaults
  - Setting individual configuration values

## Dependencies & Imports

### External Dependencies
- **os**: Operating system interface for environment variables
- **pathlib.Path**: Modern path handling for configuration file management
- **typing**: Type hints for better code documentation and IDE support

### Internal Dependencies
- **core.config.CodexConfig**: Main configuration class providing application settings
- **constants.ai.get_cli_model_choices**: Available AI model definitions
- **constants.output.VALID_OUTPUT_FORMATS**: Supported output format definitions

### Environment Requirements
- **XDG Base Directory**: Uses `~/.config/codex-ai/` for configuration storage
- **File System**: Requires read/write access to user's home directory
- **Python 3.7+**: Uses modern Path and type hint features

## Configuration Schema

The global configuration file supports the following environment variables:

### API Configuration
- **ANTHROPIC_API_KEY**: Anthropic API key for Claude models
- **CODEX_DEFAULT_MODEL**: Primary AI model to use
- **CODEX_FALLBACK_MODELS**: Comma-separated list of fallback models

### Output Configuration
- **CODEX_OUTPUT_FORMAT**: Output format (markdown, json, yaml, etc.)
- **CODEX_OUTPUT_DIR**: Directory for generated output files

### Behavior Configuration
- **CODEX_VERBOSE**: Enable verbose logging (true/false)
- **CODEX_GIT_TIMEOUT**: Git operation timeout in seconds
- **CODEX_AI_TIMEOUT**: AI request timeout in seconds
- **CODEX_AI_RETRY_ATTEMPTS**: Number of retry attempts for AI requests

### Performance Configuration
- **CODEX_CACHE_ENABLED**: Enable response caching (true/false)
- **CODEX_PARALLEL_PROCESSING**: Enable parallel processing (true/false)

## Usage Examples

### Basic Configuration Management

```python
# Set API key
from commands.config import update_global_config
update_global_config({'ANTHROPIC_API_KEY': 'sk-ant-your-key-here'})

# Load current configuration
config_data = load_global_config()
current_model = config_data.get('CODEX_DEFAULT_MODEL')

# Display configuration
from core.config import CodexConfig
config = CodexConfig()
show_current_config(config)
```

### Command Line Usage

```bash
# View current configuration
codex-ai config --list

# Set API key
codex-ai config --api-key sk-ant-your-key-here

# Configure AI model
codex-ai config --model claude-3-5-sonnet-20241022

# Set multiple fallback models
codex-ai config --fallback-models "claude-3-haiku-20240307,claude-3-sonnet-20240229"

# Configure output settings
codex-ai config --output-format json --output-dir ./my-output

# Reset to defaults
codex-ai config --reset
```

### Programmatic Configuration

```python
from commands.config import (
    load_global_config, 
    update_global_config, 
    validate_model,
    get_global_config_path
)

# Check if configuration exists
config_path = get_global_config_path()
if config_path.exists():
    current_config = load_global_config()
    print(f"Found {len(current_config)} configuration settings")

# Validate and update model
new_model = "claude-3-5-sonnet-20241022"
if validate_model(new_model):
    update_global_config({'CODEX_DEFAULT_MODEL': new_model})
    print(f"Model updated to: {new_model}")
else:
    print(f"Invalid model: {new_model}")
```

## Implementation Notes

### Security Considerations
- **API Key Masking**: API keys are masked in display output, showing only first 8 and last 4 characters
- **File Permissions**: Configuration file inherits user's default permissions
- **Input Validation**: All user inputs are validated before storage

### Error Handling
- **File Access**: Gracefully handles missing configuration files
- **Malformed Data**: Ignores invalid lines in configuration files
- **Validation Errors**: Provides clear error messages for invalid inputs
- **Exception Handling**: Catches and reports configuration errors with appropriate exit codes

### Performance Considerations
- **Lazy Loading**: Configuration is loaded only when needed
- **Atomic Updates**: Configuration updates are atomic (write to temp file, then rename)
- **Minimal I/O**: Only reads/writes configuration file when necessary

### Design Patterns
- **Separation of Concerns**: Clear separation between validation, storage, and display logic
- **Immutable Updates**: Configuration updates create new state rather than modifying existing
- **Fail-Fast Validation**: Input validation occurs before any file operations

### Known Limitations
- **Single User**: Configuration is per-user, not per-project
- **Text Format**: Uses simple key=value format, not structured data
- **No Encryption**: Configuration file is stored in plain text
- **Limited Validation**: Some configuration values are validated only at usage time

### Future Improvement Opportunities
- **Project-Specific Config**: Support for project-level configuration files
- **Configuration Profiles**: Multiple named configuration profiles
- **Encrypted Storage**: Secure storage for sensitive configuration data
- **Configuration Migration**: Automatic migration between configuration versions
- **Interactive Setup**: Guided configuration setup for new users

## Integration with Other Components

### Core Configuration System
This module works closely with `core.config.CodexConfig` to provide a complete configuration management solution. The global configuration file serves as persistent storage, while CodexConfig provides runtime access and defaults.

### Command Line Interface
The `run_config` function integrates with the main CLI system, handling command-line arguments and providing user feedback through console output.

### Constants and Validation
Relies on constants defined in `constants.ai` and `constants.output` for validation of user inputs, ensuring consistency across the application.

## See Also
- [Core Configuration](../core/config.py) - Runtime configuration management
- [AI Constants](../constants/ai.py) - Available AI model definitions  
- [Output Constants](../constants/output.py) - Supported output formats
- [Commands Overview](./README.md) - Other available commands
