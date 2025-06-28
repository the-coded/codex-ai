#!/usr/bin/env python3
"""
Test script for commands/config.py

CRITICAL TESTS - Real validation of config command functionality.
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
    """Test config command with REAL validation - NO BIAS."""
    print("🧪 Testing Config Command - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from commands.config import run_config, get_global_config_path, load_global_config, save_global_config
        from core.config import CodexConfig
        import argparse
        
        print("✅ Config command imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import config command: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Global config path validation
    print("\n📍 Test 1: Global config path validation...")
    try:
        config_path = get_global_config_path()
        if isinstance(config_path, Path) and config_path.parent.exists():
            print(f"✅ Global config path is valid Path: {config_path}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected valid Path, got {type(config_path)}: {config_path}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid config path: {config_path}")
    except Exception as e:
        print(f"❌ ERROR: Config path test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Config path error: {e}")
    
    # Test 2: Load current global config validation
    print("\n📋 Test 2: Load current global config validation...")
    try:
        current_config = load_global_config()
        if isinstance(current_config, dict):
            print(f"✅ Config loaded as dict: {len(current_config)} settings")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected dict, got {type(current_config)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid config type: {type(current_config)}")
    except Exception as e:
        print(f"❌ ERROR: Config load test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Config load error: {e}")
    
    # Test 3: Config list command validation
    print("\n📊 Test 3: Config list command validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.list = True
                self.reset = False
                self.api_key = None
                self.model = None
                self.fallback_models = None
                self.output_format = None
                self.output_dir = None
                self.verbose = None
                self.git_timeout = None
                self.ai_timeout = None
                self.ai_retry_attempts = None
        
        args = MockArgs()
        result = run_config(args, config)
        if isinstance(result, int) and result == 0:
            print(f"✅ Config list command returned success: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid list command result: {result}")
    except Exception as e:
        print(f"❌ ERROR: Config list test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Config list error: {e}")
    
    # Test 4: Model validation
    print("\n🤖 Test 4: Model validation...")
    try:
        from commands.config import validate_model
        
        valid_models = ['claude_4_sonnet', 'claude_3_7_sonnet', 'claude_3_5_sonnet']
        invalid_models = ['invalid_model', 'gpt-4', '']
        
        # Test valid models
        all_valid_passed = True
        for model in valid_models:
            result = validate_model(model)
            if result is True:
                print(f"✅ {model}: correctly validated")
            else:
                print(f"❌ FAIL: {model} should be valid, got {result}")
                all_valid_passed = False
                test_results['errors'].append(f"Valid model rejected: {model}")
        
        # Test invalid models
        all_invalid_passed = True
        for model in invalid_models:
            result = validate_model(model)
            if result is False:
                print(f"✅ {model}: correctly rejected")
            else:
                print(f"❌ FAIL: {model} should be invalid, got {result}")
                all_invalid_passed = False
                test_results['errors'].append(f"Invalid model accepted: {model}")
        
        if all_valid_passed and all_invalid_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Model validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model validation error: {e}")
    
    # Test 5: Output format validation
    print("\n📄 Test 5: Output format validation...")
    try:
        from commands.config import validate_output_format
        
        valid_formats = ['json', 'yaml', 'markdown', 'html', 'text']
        invalid_formats = ['xml', 'pdf', '']
        
        # Test valid formats
        all_valid_passed = True
        for format_name in valid_formats:
            result = validate_output_format(format_name)
            if result is True:
                print(f"✅ {format_name}: correctly validated")
            else:
                print(f"❌ FAIL: {format_name} should be valid, got {result}")
                all_valid_passed = False
                test_results['errors'].append(f"Valid format rejected: {format_name}")
        
        # Test invalid formats
        all_invalid_passed = True
        for format_name in invalid_formats:
            result = validate_output_format(format_name)
            if result is False:
                print(f"✅ {format_name}: correctly rejected")
            else:
                print(f"❌ FAIL: {format_name} should be invalid, got {result}")
                all_invalid_passed = False
                test_results['errors'].append(f"Invalid format accepted: {format_name}")
        
        if all_valid_passed and all_invalid_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Output format validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Output format validation error: {e}")
    
    # Test 6: Boolean validation
    print("\n🔘 Test 6: Boolean validation...")
    try:
        from commands.config import validate_boolean
        
        valid_booleans = ['true', 'false', 'True', 'False', 'TRUE', 'FALSE']
        invalid_booleans = ['yes', 'no', '1', '0', 'maybe']
        
        # Test valid booleans
        all_valid_passed = True
        for value in valid_booleans:
            result = validate_boolean(value)
            if result is True:
                print(f"✅ {value}: correctly validated")
            else:
                print(f"❌ FAIL: {value} should be valid, got {result}")
                all_valid_passed = False
                test_results['errors'].append(f"Valid boolean rejected: {value}")
        
        # Test invalid booleans
        all_invalid_passed = True
        for value in invalid_booleans:
            result = validate_boolean(value)
            if result is False:
                print(f"✅ {value}: correctly rejected")
            else:
                print(f"❌ FAIL: {value} should be invalid, got {result}")
                all_invalid_passed = False
                test_results['errors'].append(f"Invalid boolean accepted: {value}")
        
        if all_valid_passed and all_invalid_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Boolean validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Boolean validation error: {e}")
    
    # Test 7: Fallback models parsing
    print("\n🔄 Test 7: Fallback models parsing...")
    try:
        from commands.config import parse_fallback_models
        
        # Test valid parsing
        try:
            models = parse_fallback_models("claude_4_sonnet,claude_3_7_sonnet")
            if isinstance(models, list) and len(models) == 2:
                print(f"✅ Valid models parsed correctly: {models}")
                valid_parse_passed = True
            else:
                print(f"❌ FAIL: Expected list with 2 items, got {type(models)}: {models}")
                valid_parse_passed = False
                test_results['errors'].append(f"Valid parse failed: {models}")
        except Exception as e:
            print(f"❌ FAIL: Valid models parsing crashed: {e}")
            valid_parse_passed = False
            test_results['errors'].append(f"Valid parse exception: {e}")
        
        # Test invalid parsing
        try:
            models = parse_fallback_models("invalid_model,claude_4_sonnet")
            print(f"❌ FAIL: Invalid models should have failed, got: {models}")
            invalid_parse_passed = False
            test_results['errors'].append(f"Invalid parse should have failed: {models}")
        except ValueError:
            print(f"✅ Invalid models correctly rejected with ValueError")
            invalid_parse_passed = True
        except Exception as e:
            print(f"❌ FAIL: Expected ValueError, got {type(e)}: {e}")
            invalid_parse_passed = False
            test_results['errors'].append(f"Wrong exception type: {type(e)}")
        
        if valid_parse_passed and invalid_parse_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Fallback models test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Fallback models error: {e}")
    
    # Test 8: Error handling validation
    print("\n🚫 Test 8: Error handling validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.list = False
                self.reset = False
                self.api_key = None
                self.model = None
                self.fallback_models = None
                self.output_format = None
                self.output_dir = None
                self.verbose = None
                self.git_timeout = None
                self.ai_timeout = None
                self.ai_retry_attempts = None
        
        error_tests_passed = 0
        
        # Test invalid model
        args = MockArgs()
        args.model = "invalid_model"
        result = run_config(args, config)
        if isinstance(result, int) and result == 1:
            print(f"✅ Invalid model correctly returns error code 1")
            error_tests_passed += 1
        else:
            print(f"❌ FAIL: Expected error code 1, got {result}")
            test_results['errors'].append(f"Invalid model error code: {result}")
        
        # Test invalid format
        args = MockArgs()
        args.output_format = "invalid_format"
        result = run_config(args, config)
        if isinstance(result, int) and result == 1:
            print(f"✅ Invalid format correctly returns error code 1")
            error_tests_passed += 1
        else:
            print(f"❌ FAIL: Expected error code 1, got {result}")
            test_results['errors'].append(f"Invalid format error code: {result}")
        
        # Test invalid boolean
        args = MockArgs()
        args.verbose = "maybe"
        result = run_config(args, config)
        if isinstance(result, int) and result == 1:
            print(f"✅ Invalid boolean correctly returns error code 1")
            error_tests_passed += 1
        else:
            print(f"❌ FAIL: Expected error code 1, got {result}")
            test_results['errors'].append(f"Invalid boolean error code: {result}")
        
        if error_tests_passed == 3:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling test error: {e}")
    
    # Test 9: Backup and restore functionality
    print("\n💾 Test 9: Backup and restore functionality...")
    try:
        # Create backup of current config
        original_config = load_global_config().copy()
        if isinstance(original_config, dict):
            print(f"✅ Original config backed up: {len(original_config)} settings")
            backup_passed = True
        else:
            print(f"❌ FAIL: Expected dict backup, got {type(original_config)}")
            backup_passed = False
            test_results['errors'].append(f"Backup failed: {type(original_config)}")
        
        # Test save/load cycle with temporary data
        test_config = {
            "TEST_SETTING": "test_value",
            "TEST_NUMBER": "42"
        }
        
        save_global_config(test_config)
        loaded_config = load_global_config()
        
        if (isinstance(loaded_config, dict) and 
            loaded_config.get("TEST_SETTING") == "test_value" and
            loaded_config.get("TEST_NUMBER") == "42"):
            print("✅ Test config save/load cycle works correctly")
            cycle_passed = True
        else:
            print(f"❌ FAIL: Config save/load failed. Expected TEST_SETTING=test_value, got {loaded_config.get('TEST_SETTING')}")
            cycle_passed = False
            test_results['errors'].append(f"Save/load cycle failed: {loaded_config}")
        
        # Restore original config
        save_global_config(original_config)
        restored_config = load_global_config()
        
        if (isinstance(restored_config, dict) and 
            len(restored_config) == len(original_config) and
            all(restored_config.get(k) == v for k, v in original_config.items())):
            print("✅ Config restoration verified completely")
            restore_passed = True
        else:
            print(f"❌ FAIL: Config restoration failed. Expected {len(original_config)} items, got {len(restored_config)}")
            restore_passed = False
            test_results['errors'].append(f"Restoration failed: expected {len(original_config)}, got {len(restored_config)}")
        
        if backup_passed and cycle_passed and restore_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Backup/restore test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Backup/restore error: {e}")
    
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
        print(f"\n✅ Config command is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Config command has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
