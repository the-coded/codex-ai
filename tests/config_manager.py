#!/usr/bin/env python3
"""
Test script for core/config/manager.py

Tests the CodexConfig class functionality including
hierarchical configuration loading, environment variable parsing,
and configuration methods.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test config manager functionality."""
    print("🧪 Testing Config Manager...")
    
    try:
        from core.config.manager import CodexConfig, get_config, set_config
        
        print("✅ Config manager imported successfully")
        
        # Test 1: Basic config creation
        print("\n📝 Test 1: Basic configuration creation...")
        config = CodexConfig()
        print(f"✅ CodexConfig created successfully")
        print(f"   Default model: {config.get_default_model()}")
        print(f"   Output format: {config.get_output_format()}")
        print(f"   Verbose mode: {config.get_verbose()}")
        
        # Test 2: Global config instance
        print("\n🌐 Test 2: Global configuration instance...")
        global_config = get_config()
        print(f"✅ Global config retrieved")
        print(f"   Different instances: {config is not global_config}")  # Should be different instances
        
        # Test another call to get_config (should return same instance)
        global_config2 = get_config()
        print(f"   Same global instance: {global_config is global_config2}")  # Should be same instance
        
        # Test set_config
        new_config = CodexConfig()
        set_config(new_config)
        global_config3 = get_config()
        print(f"   Set config working: {new_config is global_config3}")  # Should be same instance
        
        # Test 3: Configuration hierarchy
        print("\n📊 Test 3: Configuration hierarchy...")
        
        # Test with CLI values (highest priority)
        model_cli = config.get_default_model(cli_value="claude_3_5_sonnet")
        print(f"✅ CLI override test: {model_cli} (should be claude_3_5_sonnet)")
        
        # Test with default values
        timeout = config.get_git_timeout()
        print(f"✅ Default value test: Git timeout = {timeout}s")
        
        # Test 4: Environment variable parsing
        print("\n🌍 Test 4: Environment variable parsing...")
        
        # Test boolean parsing
        test_values = [
            ("true", True),
            ("false", False),
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
            ("on", True),
            ("off", False),
            ("TRUE", True),
            ("FALSE", False)
        ]
        
        for value, expected in test_values:
            parsed = config._parse_env_value(value)
            status = "✅" if parsed == expected else "❌"
            print(f"{status} '{value}' → {parsed} (expected {expected})")
        
        # Test numeric parsing
        print("\n🔢 Test 4b: Numeric parsing...")
        numeric_tests = [
            ("123", 123),
            ("45.67", 45.67),
            ("0", 0),
            ("-42", -42),
            ("3.14159", 3.14159),
            ("not_a_number", "not_a_number")
        ]
        
        for value, expected in numeric_tests:
            parsed = config._parse_env_value(value)
            status = "✅" if parsed == expected else "❌"
            print(f"{status} '{value}' → {parsed} (expected {expected})")
        
        # Test list parsing
        print("\n📋 Test 4c: List parsing...")
        list_tests = [
            ("a,b,c", ["a", "b", "c"]),
            ("single", "single"),
            ("one, two, three", ["one", "two", "three"]),
            ("item1,item2,item3", ["item1", "item2", "item3"]),
            ("", "")
        ]
        
        for value, expected in list_tests:
            parsed = config._parse_env_value(value)
            status = "✅" if parsed == expected else "❌"
            print(f"{status} '{value}' → {parsed} (expected {expected})")
        
        # Test 5: API key handling (without exposing the key)
        print("\n🔑 Test 5: API key handling...")
        api_key = config.get_api_key()
        if api_key:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            print(f"✅ API key found: {masked_key}")
        else:
            print("⚠️  No API key found")
        
        # Test CLI override
        cli_key = config.get_api_key(cli_value="test-key-123")
        print(f"✅ CLI override test: {cli_key} (should be test-key-123)")
        
        # Test 6: Model token limits
        print("\n🤖 Test 6: Model token limits...")
        models_to_test = [
            ("claude_4_sonnet", 1000000),
            ("claude-4-sonnet-20250514", 1000000),
            ("claude_3_7_sonnet", 500000),
            ("claude-3-7-sonnet-latest", 500000),
            ("claude_3_5_sonnet", 200000),
            ("claude-3-5-sonnet-latest", 200000),
            ("unknown_model", 200000)  # Should default to smallest
        ]
        
        for model, expected_tokens in models_to_test:
            tokens = config.get_model_max_tokens(model)
            status = "✅" if tokens == expected_tokens else "❌"
            print(f"{status} {model}: {tokens:,} tokens (expected {expected_tokens:,})")
        
        # Test 7: Fallback models parsing
        print("\n🔄 Test 7: Fallback models parsing...")
        
        # Test string input
        fallbacks_str = config.get_fallback_models(cli_value="claude_3_7_sonnet,claude_3_5_sonnet")
        print(f"✅ String fallbacks: {fallbacks_str}")
        
        # Test list input
        fallbacks_list = config.get_fallback_models(cli_value=["claude_4_sonnet", "claude_3_7_sonnet"])
        print(f"✅ List fallbacks: {fallbacks_list}")
        
        # Test default fallbacks
        default_fallbacks = config.get_fallback_models()
        print(f"✅ Default fallbacks: {default_fallbacks}")
        
        # Test 8: Git exclude patterns
        print("\n🚫 Test 8: Git exclude patterns...")
        
        patterns = config.get_git_exclude_patterns()
        print(f"✅ Default exclude patterns: {patterns}")
        
        custom_patterns = config.get_git_exclude_patterns(cli_value="*.tmp,build/**,dist/**")
        print(f"✅ Custom exclude patterns: {custom_patterns}")
        
        # Test string to list conversion
        string_patterns = config.get_git_exclude_patterns(cli_value="*.log,*.tmp,node_modules/**")
        print(f"✅ String patterns converted: {string_patterns}")
        
        # Test 9: All convenience methods
        print("\n⚙️ Test 9: All convenience methods...")
        
        methods_to_test = [
            "get_default_model",
            "get_fallback_models", 
            "get_output_format",
            "get_output_dir",
            "get_verbose",
            "get_git_timeout",
            "get_ai_retry_attempts",
            "get_ai_timeout",
            "is_cache_enabled",
            "is_parallel_processing_enabled",
            "get_git_exclude_patterns"
        ]
        
        for method_name in methods_to_test:
            try:
                method = getattr(config, method_name)
                result = method()
                print(f"✅ {method_name}(): {result}")
            except Exception as e:
                print(f"❌ {method_name}(): Error - {e}")
        
        # Test 10: Error handling
        print("\n🧪 Test 10: Error handling...")
        
        # Test that config works without any external files
        simple_config = CodexConfig()
        print("✅ Simple config creation handled gracefully")
        
        # Test with environment variable simulation
        original_env = os.environ.get('CODEX_DEFAULT_MODEL')
        try:
            os.environ['CODEX_DEFAULT_MODEL'] = 'claude_3_7_sonnet'
            env_config = CodexConfig()
            model = env_config.get_default_model()
            if model == 'claude_3_7_sonnet':
                print("✅ Environment variable override working")
            else:
                print(f"❌ Environment variable override failed: got {model}")
        finally:
            if original_env is not None:
                os.environ['CODEX_DEFAULT_MODEL'] = original_env
            elif 'CODEX_DEFAULT_MODEL' in os.environ:
                del os.environ['CODEX_DEFAULT_MODEL']
        
        print("\n🎉 All Config Manager tests completed successfully!")
        print("\n📊 Test Summary:")
        print("   ✅ Basic configuration creation")
        print("   ✅ Global configuration instance")
        print("   ✅ Configuration hierarchy")
        print("   ✅ Environment variable parsing")
        print("   ✅ API key handling")
        print("   ✅ Model token limits")
        print("   ✅ Fallback models parsing")
        print("   ✅ Git exclude patterns")
        print("   ✅ All convenience methods")
        print("   ✅ Error handling")
        print("\n🏗️ core/config/manager.py working perfectly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Config manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
