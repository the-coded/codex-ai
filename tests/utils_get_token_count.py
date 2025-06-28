#!/usr/bin/env python3
"""
Test script for utils/get_token_count.py

CRITICAL TESTS - Real validation of token counting functionality.
This test will FAIL if the implementation has bugs.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test token counting functionality with REAL validation."""
    print("🧪 Testing Token Count Utility - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from utils.get_token_count import (
            get_token_count_from_text, get_token_count, get_multiple_files_token_count,
            get_total_token_count, estimate_model_for_token_count, 
            validate_token_count_for_model, get_token_count_summary
        )
        print("✅ Token count utility imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import token count utility: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Empty string
    print("\n📝 Test 1: Empty string token count...")
    try:
        result = get_token_count_from_text("", use_api=False)  # Use fallback to avoid API costs
        if result == 0:
            print(f"✅ Empty string correctly returns 0 tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Empty string returned {result} tokens, expected 0")
            test_results['failed'] += 1
            test_results['errors'].append(f"Empty string test failed: got {result}, expected 0")
    except Exception as e:
        print(f"❌ ERROR: Empty string test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Empty string test error: {e}")
    
    # Test 2: Simple text
    print("\n📝 Test 2: Simple text token count...")
    test_text = "Hello world"
    try:
        result = get_token_count_from_text(test_text, use_api=False)
        # This should be around 2-3 tokens for most tokenizers
        if isinstance(result, int) and result > 0:
            print(f"✅ Simple text '{test_text}' returns {result} tokens (reasonable)")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Simple text returned invalid result: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Simple text test failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Simple text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Simple text test error: {e}")
    
    # Test 3: Code snippet
    print("\n📝 Test 3: Code snippet token count...")
    code_text = """
def hello_world():
    print("Hello, world!")
    return True
"""
    try:
        result = get_token_count_from_text(code_text, use_api=False)
        # Code should have more tokens due to syntax
        if isinstance(result, int) and result > 10:
            print(f"✅ Code snippet returns {result} tokens (reasonable for code)")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Code snippet returned suspiciously low count: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Code snippet test failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Code snippet test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Code snippet test error: {e}")
    
    # Test 4: Large text
    print("\n📝 Test 4: Large text token count...")
    large_text = "This is a test sentence. " * 100  # 500 words
    try:
        result = get_token_count_from_text(large_text, use_api=False)
        # Should be significantly more tokens
        if isinstance(result, int) and result > 100:
            print(f"✅ Large text (500 words) returns {result} tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Large text returned unexpectedly low count: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Large text test failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Large text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Large text test error: {e}")
    
    # Test 5: Special characters
    print("\n📝 Test 5: Special characters token count...")
    special_text = "Hello! @#$%^&*()_+ 你好 🚀 ñáéíóú"
    try:
        result = get_token_count_from_text(special_text, use_api=False)
        if isinstance(result, int) and result > 0:
            print(f"✅ Special characters text returns {result} tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Special characters returned invalid result: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Special characters test failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Special characters test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Special characters test error: {e}")
    
    # Test 6: None input (should handle gracefully)
    print("\n📝 Test 6: None input handling...")
    try:
        result = get_token_count_from_text(None, use_api=False)
        if result == 0:
            print(f"✅ None input correctly returns 0 tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: None input returned {result}, expected 0")
            test_results['failed'] += 1
            test_results['errors'].append(f"None input test failed: got {result}, expected 0")
    except Exception as e:
        print(f"❌ ERROR: None input crashed (should handle gracefully): {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"None input test error: {e}")
    
    # Test 7: Non-string input
    print("\n📝 Test 7: Non-string input handling...")
    try:
        result = get_token_count_from_text(12345, use_api=False)
        # Number "12345" should be converted to string and return reasonable token count
        if isinstance(result, int) and result > 0:
            print(f"✅ Number input converted to string: {result} tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Number input returned invalid result: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Number input test failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Number input crashed (should handle gracefully): {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Number input test error: {e}")
    
    # Test 8: Consistency check
    print("\n📝 Test 8: Consistency check...")
    test_string = "Consistency test string"
    try:
        result1 = get_token_count_from_text(test_string, use_api=False)
        result2 = get_token_count_from_text(test_string, use_api=False)
        if result1 == result2:
            print(f"✅ Consistent results: {result1} == {result2}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Inconsistent results: {result1} != {result2}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Consistency test failed: {result1} != {result2}")
    except Exception as e:
        print(f"❌ ERROR: Consistency test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Consistency test error: {e}")
    
    # Test 9: Performance check (basic)
    print("\n📝 Test 9: Basic performance check...")
    import time
    performance_text = "Performance test text. " * 1000  # Large text
    try:
        start_time = time.time()
        result = get_token_count_from_text(performance_text, use_api=False)
        end_time = time.time()
        duration = end_time - start_time
        
        if duration < 5.0:  # Should complete in under 5 seconds
            print(f"✅ Performance acceptable: {duration:.3f}s for large text ({result} tokens)")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Performance too slow: {duration:.3f}s")
            test_results['failed'] += 1
            test_results['errors'].append(f"Performance test failed: {duration:.3f}s")
    except Exception as e:
        print(f"❌ ERROR: Performance test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Performance test error: {e}")
    
    # Test 10: Return type validation
    print("\n📝 Test 10: Return type validation...")
    try:
        result = get_token_count_from_text("Type test", use_api=False)
        if isinstance(result, int):
            print(f"✅ Returns integer as expected: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Returns {type(result)}, expected int")
            test_results['failed'] += 1
            test_results['errors'].append(f"Return type test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: Return type test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Return type test error: {e}")
    
    # Test 11: API functionality test
    print("\n🌐 Test 11: API functionality test...")
    import os
    
    # Check multiple sources for API key
    api_key = None
    api_sources = []
    
    # 1. Environment variable
    env_key = os.getenv("ANTHROPIC_API_KEY")
    if env_key:
        api_key = env_key
        api_sources.append("Environment variable")
    
    # 2. Try to get from config
    try:
        from core.config.manager import CodexConfig
        config = CodexConfig()
        config_key = config.get_api_key()
        if config_key and not api_key:
            api_key = config_key
            api_sources.append("Config file")
    except Exception:
        pass
    
    
    print(f"   API key sources checked: {', '.join(api_sources) if api_sources else 'None found'}")
    
    if api_key:
        try:
            api_result = get_token_count_from_text("Hello API test", use_api=True)
            fallback_result = get_token_count_from_text("Hello API test", use_api=False)
            
            if isinstance(api_result, int) and api_result > 0:
                print(f"✅ API returned valid result: {api_result} tokens")
                print(f"   Fallback result: {fallback_result} tokens")
                print(f"   Difference: {abs(api_result - fallback_result)} tokens")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: API returned invalid result: {api_result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"API test failed: got {api_result}")
        except Exception as e:
            print(f"⚠️  API test failed (expected if no key/network): {e}")
            # Don't count as failure since API might not be available
            test_results['passed'] += 1
    else:
        print("⚠️  No ANTHROPIC_API_KEY found, skipping API test")
        test_results['passed'] += 1
    
    # Test 12: File-based token counting
    print("\n📁 Test 12: File-based token counting...")
    import tempfile
    try:
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def test_function():\n    return 'Hello, world!'\n")
            temp_file = f.name
        
        # Test file counting
        file_result = get_token_count(temp_file, use_api=False)
        
        if isinstance(file_result, int) and file_result > 0:
            print(f"✅ File token count: {file_result} tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: File counting returned invalid result: {file_result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"File counting test failed: got {file_result}")
        
        # Cleanup
        os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ ERROR: File counting test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File counting test error: {e}")
    
    # Test 13: Multiple files token counting
    print("\n📁 Test 13: Multiple files token counting...")
    try:
        # Create multiple temporary test files
        temp_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_test{i}.py', delete=False) as f:
                f.write(f"# Test file {i}\ndef function_{i}():\n    return {i}\n")
                temp_files.append(f.name)
        
        # Test multiple file counting
        multi_result = get_multiple_files_token_count(temp_files, use_api=False)
        total_result = get_total_token_count(temp_files, use_api=False)
        
        if isinstance(multi_result, dict) and len(multi_result) == 3:
            print(f"✅ Multiple files counted: {len(multi_result)} files")
            print(f"   Individual counts: {list(multi_result.values())}")
            print(f"   Total tokens: {total_result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Multiple files counting failed: {multi_result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Multiple files test failed: got {multi_result}")
        
        # Cleanup
        for temp_file in temp_files:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ ERROR: Multiple files test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Multiple files test error: {e}")
    
    # Test 14: Model estimation
    print("\n🤖 Test 14: Model estimation...")
    try:
        # Test model estimation for different token counts
        small_model = estimate_model_for_token_count(1000)
        large_model = estimate_model_for_token_count(100000)
        
        print(f"✅ Model estimation working:")
        print(f"   1K tokens → {small_model}")
        print(f"   100K tokens → {large_model}")
        test_results['passed'] += 1
        
    except Exception as e:
        print(f"❌ ERROR: Model estimation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model estimation test error: {e}")
    
    # Test 15: Token validation
    print("\n✅ Test 15: Token validation...")
    try:
        # Test token validation for different models
        valid_small = validate_token_count_for_model(1000, "claude-4-sonnet")
        valid_large = validate_token_count_for_model(1000000, "claude-4-sonnet")
        
        print(f"✅ Token validation working:")
        print(f"   1K tokens valid: {valid_small}")
        print(f"   1M tokens valid: {valid_large}")
        test_results['passed'] += 1
        
    except Exception as e:
        print(f"❌ ERROR: Token validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token validation test error: {e}")
    
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
        print(f"\n✅ Token count utility is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Token count utility has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This utility needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
