"""
Configuration management for Codex-AI.

Supports hierarchical configuration loading:
1. CLI arguments (highest priority)
2. Environment variables
3. .env files
4. Config files (YAML/JSON)
5. Built-in defaults (lowest priority)
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
import json

# Try to import python-dotenv, install if not available
try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing python-dotenv for .env file support...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv


class CodexConfig:
    """Configuration manager with hierarchical loading."""
    
    def __init__(self, config_path: Optional[str] = None):
        self._config_data = {}
        self._load_env_files()
        if config_path:
            self._load_config_file(config_path)
    
    def _load_env_files(self):
        """Load .env files in order of priority."""
        env_files = [
            Path.cwd() / '.env',                    # Project .env
            Path.cwd() / '.env.local',             # Local overrides
            Path.home() / '.codex' / '.env',       # Global config
        ]
        
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)  # Don't override existing vars
    
    def _load_config_file(self, config_path: str):
        """Load configuration from YAML or JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yml', '.yaml']:
                    self._config_data = yaml.safe_load(f) or {}
                elif config_file.suffix.lower() == '.json':
                    self._config_data = json.load(f)
                else:
                    print(f"Warning: Unsupported config file format: {config_file}")
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def get(self, key: str, default: Any = None, cli_value: Any = None) -> Any:
        """
        Get configuration value with hierarchical priority.
        
        Args:
            key: Configuration key
            default: Default value if not found
            cli_value: Value from CLI argument (highest priority)
        
        Returns:
            Configuration value
        """
        # 1. CLI argument (highest priority)
        if cli_value is not None:
            return cli_value
        
        # 2. Environment variable
        env_key = f"CODEX_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._parse_env_value(env_value)
        
        # 3. Config file
        if key in self._config_data:
            return self._config_data[key]
        
        # 4. Default value
        return default
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        # Boolean values
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        if value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # Numeric values
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # List values (comma-separated)
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        
        # String value
        return value
    
    # Convenience methods for common configuration values
    
    def get_api_key(self, cli_value: Optional[str] = None) -> Optional[str]:
        """Get Anthropic API key."""
        return self.get('api_key', cli_value=cli_value) or os.getenv('ANTHROPIC_API_KEY')
    
    def get_default_model(self, cli_value: Optional[str] = None) -> str:
        """Get default AI model."""
        return self.get('default_model', default='claude_4_sonnet', cli_value=cli_value)
    
    def get_fallback_models(self, cli_value: Optional[List[str]] = None) -> List[str]:
        """Get fallback AI models."""
        fallbacks = self.get('fallback_models', 
                           default=['claude_3_7_sonnet', 'claude_3_5_sonnet'], 
                           cli_value=cli_value)
        if isinstance(fallbacks, str):
            return [model.strip() for model in fallbacks.split(',')]
        return fallbacks
    
    def get_output_format(self, cli_value: Optional[str] = None) -> str:
        """Get default output format."""
        return self.get('output_format', default='markdown', cli_value=cli_value)
    
    def get_output_dir(self, cli_value: Optional[str] = None) -> str:
        """Get output directory."""
        return self.get('output_dir', default='.tmp', cli_value=cli_value)
    
    def get_verbose(self, cli_value: Optional[bool] = None) -> bool:
        """Get verbose mode setting."""
        return self.get('verbose', default=False, cli_value=cli_value)
    
    def get_model_max_tokens(self, model: str) -> int:
        """Get maximum tokens for specific AI model."""
        model_tokens = {
            'claude_4_sonnet': 1000000,      # 1M tokens
            'claude-4-sonnet-20250514': 1000000,
            'claude_3_7_sonnet': 500000,     # 500K tokens  
            'claude-3-7-sonnet-latest': 500000,
            'claude_3_5_sonnet': 200000,     # 200K tokens
            'claude-3-5-sonnet-latest': 200000,
        }
        return model_tokens.get(model, 200000)  # Default to smallest if unknown
    
    def get_git_timeout(self, cli_value: Optional[int] = None) -> int:
        """Get Git command timeout."""
        return self.get('git_timeout', default=30, cli_value=cli_value)
    
    def get_ai_retry_attempts(self, cli_value: Optional[int] = None) -> int:
        """Get AI retry attempts."""
        return self.get('ai_retry_attempts', default=3, cli_value=cli_value)
    
    def get_ai_timeout(self, cli_value: Optional[int] = None) -> int:
        """Get AI command timeout."""
        return self.get('ai_timeout', default=120, cli_value=cli_value)
    
    def is_cache_enabled(self, cli_value: Optional[bool] = None) -> bool:
        """Check if caching is enabled."""
        return self.get('cache_enabled', default=True, cli_value=cli_value)
    
    def is_parallel_processing_enabled(self, cli_value: Optional[bool] = None) -> bool:
        """Check if parallel processing is enabled."""
        return self.get('parallel_processing', default=True, cli_value=cli_value)
    
    def get_git_exclude_patterns(self, cli_value: Optional[List[str]] = None) -> List[str]:
        """Get Git exclude patterns."""
        patterns = self.get('git_exclude_patterns', 
                          default=['*.lock', 'dist/**', 'node_modules/**'], 
                          cli_value=cli_value)
        if isinstance(patterns, str):
            return [pattern.strip() for pattern in patterns.split(',')]
        return patterns
    
    def create_default_config(self, path: str = 'codex.config.yaml'):
        """Create a default configuration file."""
        default_config = {
            'ai': {
                'default_model': 'claude_4_sonnet',
                'fallback_models': ['claude_3_7_sonnet', 'claude_3_5_sonnet'],
                'retry_attempts': 3,
                'timeout': 120
            },
            'output': {
                'default_format': 'markdown',
                'directory': '.tmp',
                'verbose': False
            },
            'git': {
                'exclude_patterns': ['*.lock', 'dist/**', 'node_modules/**'],
                'timeout': 30
            },
            'performance': {
                'cache_enabled': True,
                'parallel_processing': True
            }
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Default configuration created: {path}")
        print("💡 Edit this file to customize your settings")
        print("🔑 Don't forget to set ANTHROPIC_API_KEY in .env file")


# Global config instance
_config_instance = None

def get_config() -> CodexConfig:
    """Get global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = CodexConfig()
    return _config_instance

def set_config(config: CodexConfig):
    """Set global configuration instance."""
    global _config_instance
    _config_instance = config
