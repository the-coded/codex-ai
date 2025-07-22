# Configuration Management

## Overview

The `src/core/config` folder contains the core configuration management system for Codex-AI. This module provides a hierarchical configuration loading mechanism that prioritizes settings from multiple sources, ensuring flexible and predictable configuration behavior across different deployment environments.

The configuration system follows a clear priority hierarchy:
1. CLI arguments (highest priority)
2. Environment variables (CODEX_* prefixed)
3. Global config file (~/.config/codex-ai/config.env)
4. Built-in defaults (lowest priority)

## Contents

- **manager.py**: Core configuration manager implementing hierarchical configuration loading, value parsing, and convenient accessor methods for common settings

## Architecture

### Configuration Hierarchy

The system implements a four-tier configuration hierarchy designed for maximum flexibility:

```python
# Priority order (highest to lowest):
1. CLI arguments          # --model claude_4_sonnet
2. Environment variables  # CODEX_DEFAULT_MODEL=claude_4_sonnet
3. Global config file     # ~/.config/codex-ai/config.env
4. Built-in defaults      # Hardcoded fallbacks
```

### Key Components

**CodexConfig Class**: The main configuration manager that:
- Loads global configuration from the user's config directory
- Provides type-aware value parsing (boolean, numeric, list, string)
- Offers convenience methods for common configuration keys
- Maintains a singleton pattern through the global `get_config()` function

**Value Parsing**: Intelligent type conversion that handles:
- Boolean values: `true/false`, `yes/no`, `on/off`, `1/0`
- Numeric values: Integers and floats (excluding boolean numerics)
- List values: Comma-separated strings
- String values: Default fallback

## Usage

### Basic Configuration Access

```python
from core.config.manager import get_config

config = get_config()

# Get configuration with CLI override
model = config.get('default_model', default='claude_3_5_sonnet', cli_value=args.model)

# Use convenience methods
api_key = config.get_api_key(cli_value=args.api_key)
verbose = config.get_verbose(cli_value=args.verbose)
```

### Environment Variable Configuration

```bash
# Set via environment variables
export CODEX_DEFAULT_MODEL=claude_4_sonnet
export CODEX_VERBOSE=true
export ANTHROPIC_API_KEY=your_api_key_here
```

### Global Configuration File

Create `~/.config/codex-ai/config.env`:

```
# AI Configuration
ANTHROPIC_API_KEY=your_api_key_here
CODEX_DEFAULT_MODEL=claude_4_sonnet
CODEX_FALLBACK_MODELS=claude_3_7_sonnet,claude_3_5_sonnet

# Output Configuration
CODEX_OUTPUT_FORMAT=markdown
CODEX_OUTPUT_DIR=.tmp
CODEX_VERBOSE=false

# Performance Settings
CODEX_CACHE_ENABLED=true
CODEX_PARALLEL_PROCESSING=true
CODEX_AI_TIMEOUT=120
```

### Common Configuration Patterns

```python
# Model configuration
default_model = config.get_default_model(cli_value=args.model)
fallback_models = config.get_fallback_models()
max_tokens = config.get_model_max_tokens(default_model)

# Output configuration
output_format = config.get_output_format(cli_value=args.format)
output_dir = config.get_output_dir(cli_value=args.output)

# Performance settings
cache_enabled = config.is_cache_enabled()
parallel_enabled = config.is_parallel_processing_enabled()
ai_timeout = config.get_ai_timeout()
```

## Implementation Details

### Configuration Loading Strategy

The system uses manual configuration file parsing instead of external dependencies like `python-dotenv`. This approach:
- Reduces external dependencies
- Provides predictable parsing behavior
- Maintains compatibility across different environments
- Allows for custom value type inference

### Type Inference Rules

The configuration manager applies intelligent type conversion:

1. **Boolean Detection**: Recognizes common boolean representations
2. **Numeric Parsing**: Handles integers and floats, but preserves boolean semantics for `0` and `1`
3. **List Parsing**: Splits comma-separated values into lists
4. **String Fallback**: Treats unrecognized patterns as strings

### Global Instance Management

The module provides a singleton configuration instance through:
- `get_config()`: Returns the global configuration instance
- `set_config(config)`: Allows dependency injection for testing

### API Key Handling

Special handling for Anthropic API keys follows common patterns:
- Checks `ANTHROPIC_API_KEY` environment variable (standard)
- Falls back to global configuration file
- Supports CLI override for development/testing

### Error Handling

The configuration system is designed to be resilient:
- Missing configuration files are handled gracefully
- Invalid values fall back to defaults
- Type conversion errors default to string values
- Missing keys return specified defaults

## Dependencies

### Internal Dependencies
- `constants.ai`: Provides model token limits and default model names
- Standard library modules: `os`, `pathlib`, `typing`

### External Dependencies
None - the configuration system is designed to be self-contained without external package dependencies.

## Configuration Keys Reference

### AI Model Settings
- `default_model`: Primary AI model to use
- `fallback_models`: List of fallback models
- `ai_retry_attempts`: Number of retry attempts for AI calls
- `ai_timeout`: Timeout for AI operations

### Output Settings
- `output_format`: Default output format (markdown, json, etc.)
- `output_dir`: Directory for output files

### Performance Settings
- `cache_enabled`: Enable/disable caching
- `parallel_processing`: Enable/disable parallel processing
- `git_timeout`: Timeout for Git operations

### Git Integration
- `git_exclude_patterns`: Patterns to exclude from Git operations

### System Settings
- `verbose`: Enable verbose logging
```
