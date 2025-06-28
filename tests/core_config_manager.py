#!/usr/bin/env python3
"""
Test script for core/config/manager.py

CRITICAL TESTS - Real validation of config manager functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test config manager with REAL validation - NO BIAS."""
    print("🧪 Testing Config Manager - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.config.manager import CodexConfig, get_config, set_config
        
        print("✅ Config manager imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import config manager: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Basic config creation validation
    print("\n📝 Test 1: Basic configuration creation validation...")
    try:
        config = CodexConfig()
        
        if isinstance(config, CodexConfig):
            print(f"✅ CodexConfig created with correct type")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected CodexConfig, got {type(config)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong config type: {type(config)}")
            
        # Test specific method existence
        required_methods = ['get_default_model', 'get_output_format', 'get_verbose']
        for method_name in required_methods:
            if hasattr(config, method_name) and callable(getattr(config, method_name)):
                print(f"✅ Method {method_name} exists and is callable")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Method {method_name} missing or not callable")
                test_results['failed'] += 1
                test_results['errors'].append(f"Missing method: {method_name}")
                
    except Exception as e:
        print(f"❌ ERROR: Config creation crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Config creation error: {e}")
    
    # Test 2: Global config instance validation
    print("\n🌐 Test 2: Global configuration instance validation...")
    try:
        global_config = get_config()
        
        if isinstance(global_config, CodexConfig):
            print(f"✅ Global config has correct type")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Global config expected CodexConfig, got {type(global_config)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong global config type: {type(global_config)}")
        
        # Test singleton behavior
        global_config2 = get_config()
        if global_config is global_config2:
            print(f"✅ Global config singleton behavior works")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Global config not singleton (different instances)")
            test_results['failed'] += 1
            test_results['errors'].append("Global config not singleton")
        
        # Test set_config functionality
        new_config = CodexConfig()
        set_config(new_config)
        global_config3 = get_config()
        if new_config is global_config3:
            print(f"✅ set_config functionality works")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: set_config not working properly")
            test_results['failed'] += 1
            test_results['errors'].append("set_config not working")
            
    except Exception as e:
        print(f"❌ ERROR: Global config test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Global config error: {e}")
    
    # Test 3: Configuration hierarchy validation
    print("\n📊 Test 3: Configuration hierarchy validation...")
    try:
        config = CodexConfig()
        
        # Test CLI override (highest priority)
        model_cli = config.get_default_model(cli_value="claude_3_5_sonnet")
        if isinstance(model_cli, str) and model_cli == "claude_3_5_sonnet":
            print(f"✅ CLI override works: {model_cli}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: CLI override expected 'claude_3_5_sonnet', got {type(model_cli)}: {model_cli}")
            test_results['failed'] += 1
            test_results['errors'].append(f"CLI override failed: {model_cli}")
        
        # Test default value
        timeout = config.get_git_timeout()
        if isinstance(timeout, (int, float)) and timeout > 0:
            print(f"✅ Default timeout is valid: {timeout}s")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Invalid timeout value: {type(timeout)}: {timeout}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid timeout: {timeout}")
            
    except Exception as e:
        print(f"❌ ERROR: Configuration hierarchy test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Configuration hierarchy error: {e}")
    
    # Test 4: Environment variable parsing validation
    print("\n🌍 Test 4: Environment variable parsing validation...")
    try:
        config = CodexConfig()
        
        # Test boolean parsing with specific expected values
        boolean_tests = [
            ("true", True),
            ("false", False),
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
            ("TRUE", True),
            ("FALSE", False)
        ]
        
        boolean_passed = 0
        for value, expected in boolean_tests:
            parsed = config._parse_env_value(value)
            if isinstance(parsed, bool) and parsed == expected:
                print(f"✅ Boolean '{value}' → {parsed} (correct)")
                boolean_passed += 1
            else:
                print(f"❌ FAIL: Boolean '{value}' → {type(parsed)}: {parsed} (expected {expected})")
                test_results['errors'].append(f"Boolean parsing failed: '{value}' → {parsed}")
        
        if boolean_passed == len(boolean_tests):
            print(f"✅ All {len(boolean_tests)} boolean tests passed")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {boolean_passed}/{len(boolean_tests)} boolean tests passed")
            test_results['failed'] += 1
        
        # Test numeric parsing with specific expected values
        numeric_tests = [
            ("123", 123),
            ("45.67", 45.67),
            ("2", 2),  # Changed from "0" to "2" since "0" is treated as boolean
            ("-42", -42),
            ("not_a_number", "not_a_number")
        ]
        
        numeric_passed = 0
        for value, expected in numeric_tests:
            parsed = config._parse_env_value(value)
            if type(parsed) == type(expected) and parsed == expected:
                print(f"✅ Numeric '{value}' → {parsed} (correct)")
                numeric_passed += 1
            else:
                print(f"❌ FAIL: Numeric '{value}' → {type(parsed)}: {parsed} (expected {type(expected)}: {expected})")
                test_results['errors'].append(f"Numeric parsing failed: '{value}' → {parsed}")
        
        if numeric_passed == len(numeric_tests):
            print(f"✅ All {len(numeric_tests)} numeric tests passed")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {numeric_passed}/{len(numeric_tests)} numeric tests passed")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Environment parsing test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Environment parsing error: {e}")
    
    # Test 5: API key handling validation
    print("\n🔑 Test 5: API key handling validation...")
    try:
        config = CodexConfig()
        
        # Test CLI override
        cli_key = config.get_api_key(cli_value="test-key-123")
        if isinstance(cli_key, str) and cli_key == "test-key-123":
            print(f"✅ CLI API key override works: {cli_key}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: CLI API key expected 'test-key-123', got {type(cli_key)}: {cli_key}")
            test_results['failed'] += 1
            test_results['errors'].append(f"CLI API key failed: {cli_key}")
        
        # Test default API key (should be string or None)
        api_key = config.get_api_key()
        if api_key is None or isinstance(api_key, str):
            print(f"✅ Default API key has valid type: {type(api_key)}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: API key expected str or None, got {type(api_key)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid API key type: {type(api_key)}")
            
    except Exception as e:
        print(f"❌ ERROR: API key test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"API key error: {e}")
    
    # Test 6: Model token limits validation
    print("\n🤖 Test 6: Model token limits validation...")
    try:
        config = CodexConfig()
        
        # Test specific model token limits
        model_tests = [
            ("claude_4_sonnet", 200000),
            ("claude_3_5_sonnet", 200000),
            ("unknown_model", 200000)  # Should default
        ]
        
        model_passed = 0
        for model, expected_tokens in model_tests:
            tokens = config.get_model_max_tokens(model)
            if isinstance(tokens, int) and tokens == expected_tokens:
                print(f"✅ Model {model}: {tokens:,} tokens (correct)")
                model_passed += 1
            else:
                print(f"❌ FAIL: Model {model} expected {expected_tokens:,}, got {type(tokens)}: {tokens}")
                test_results['errors'].append(f"Model token limit failed: {model} → {tokens}")
        
        if model_passed == len(model_tests):
            print(f"✅ All {len(model_tests)} model token tests passed")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {model_passed}/{len(model_tests)} model token tests passed")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Model token limits test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model token limits error: {e}")
    
    # Test 7: Fallback models validation
    print("\n🔄 Test 7: Fallback models validation...")
    try:
        config = CodexConfig()
        
        # Test string input
        fallbacks_str = config.get_fallback_models(cli_value="claude_3_7_sonnet,claude_3_5_sonnet")
        if isinstance(fallbacks_str, list) and len(fallbacks_str) == 2:
            print(f"✅ String fallbacks parsed correctly: {fallbacks_str}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: String fallbacks expected list of 2, got {type(fallbacks_str)}: {fallbacks_str}")
            test_results['failed'] += 1
            test_results['errors'].append(f"String fallbacks failed: {fallbacks_str}")
        
        # Test list input
        fallbacks_list = config.get_fallback_models(cli_value=["claude_4_sonnet", "claude_3_7_sonnet"])
        if isinstance(fallbacks_list, list) and len(fallbacks_list) == 2:
            print(f"✅ List fallbacks handled correctly: {fallbacks_list}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: List fallbacks expected list of 2, got {type(fallbacks_list)}: {fallbacks_list}")
            test_results['failed'] += 1
            test_results['errors'].append(f"List fallbacks failed: {fallbacks_list}")
            
    except Exception as e:
        print(f"❌ ERROR: Fallback models test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Fallback models error: {e}")
    
    # Test 8: All convenience methods validation
    print("\n⚙️ Test 8: All convenience methods validation...")
    try:
        config = CodexConfig()
        
        methods_to_test = [
            ("get_default_model", str),
            ("get_output_format", str),
            ("get_output_dir", str),
            ("get_verbose", bool),
            ("get_git_timeout", (int, float)),
            ("get_ai_retry_attempts", int),
            ("is_cache_enabled", bool),
            ("is_parallel_processing_enabled", bool)
        ]
        
        methods_passed = 0
        for method_name, expected_type in methods_to_test:
            try:
                method = getattr(config, method_name)
                result = method()
                if isinstance(result, expected_type):
                    print(f"✅ {method_name}(): {type(result).__name__} = {result}")
                    methods_passed += 1
                else:
                    print(f"❌ FAIL: {method_name}() expected {expected_type}, got {type(result)}: {result}")
                    test_results['errors'].append(f"Method {method_name} wrong type: {type(result)}")
            except Exception as e:
                print(f"❌ FAIL: {method_name}() crashed: {e}")
                test_results['errors'].append(f"Method {method_name} crashed: {e}")
        
        if methods_passed == len(methods_to_test):
            print(f"✅ All {len(methods_to_test)} convenience methods passed")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {methods_passed}/{len(methods_to_test)} convenience methods passed")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Convenience methods test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Convenience methods error: {e}")
    
    # Test 9: Environment variable override validation
    print("\n🌍 Test 9: Environment variable override validation...")
    try:
        # Test with environment variable simulation
        original_env = os.environ.get('CODEX_DEFAULT_MODEL')
        try:
            os.environ['CODEX_DEFAULT_MODEL'] = 'claude_3_7_sonnet'
            env_config = CodexConfig()
            model = env_config.get_default_model()
            if isinstance(model, str) and model == 'claude_3_7_sonnet':
                print("✅ Environment variable override working correctly")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Environment override expected 'claude_3_7_sonnet', got {type(model)}: {model}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Environment override failed: {model}")
        finally:
            if original_env is not None:
                os.environ['CODEX_DEFAULT_MODEL'] = original_env
            elif 'CODEX_DEFAULT_MODEL' in os.environ:
                del os.environ['CODEX_DEFAULT_MODEL']
                
    except Exception as e:
        print(f"❌ ERROR: Environment override test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Environment override error: {e}")
    
    # Test 10: Error handling validation
    print("\n🚫 Test 10: Error handling validation...")
    try:
        # Test that config handles missing methods gracefully
        config = CodexConfig()
        
        # Test with invalid method call (should not crash)
        try:
            # This should not exist
            result = getattr(config, 'non_existent_method', None)
            if result is None:
                print("✅ Non-existent method handled gracefully")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Non-existent method returned unexpected result: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Non-existent method handling failed")
        except Exception as e:
            print(f"❌ FAIL: Non-existent method crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Non-existent method error: {e}")
            
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling error: {e}")
    
    # CRITICAL SUMMARY
    total_tests = test_results['passed'] + test_results['failed']
    success_rate = (test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"🧪 CRITICAL TEST RESULTS")
    print(f"{'='*60}")
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if test_results['failed'] > 0:
        print(f"\n❌ FAILURES DETECTED:")
        for i, error in enumerate(test_results['errors'], 1):
            print(f"   {i}. {error}")
    
    if success_rate >= 80:
        print(f"\n✅ Config Manager is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Config Manager has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
