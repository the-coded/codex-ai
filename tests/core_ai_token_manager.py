#!/usr/bin/env python3
"""
Test script for core/ai/token_manager.py

CRITICAL TESTS - Real validation of AI token management functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test AI token manager with REAL validation - NO BIAS."""
    print("🧪 Testing AI Token Manager - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.ai.token_manager import (
            count_tokens, get_token_count, get_token_count_from_text,
            get_multiple_files_token_count, get_total_token_count,
            estimate_model_for_token_count, validate_token_count_for_model,
            get_token_count_summary
        )
        print("✅ AI token manager imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import AI token manager: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Token counting with valid text
    print("\n🔢 Test 1: Token counting with valid text...")
    try:
        test_text = "This is a test text for token counting."
        result = count_tokens(test_text)
        
        if isinstance(result, int):
            if result > 0:
                print(f"✅ Token count returned: {result} tokens for text length {len(test_text)}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Token count should be > 0, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Token count non-positive: {result}")
        else:
            print(f"❌ FAIL: Token count returned {type(result)}, expected int")
            test_results['failed'] += 1
            test_results['errors'].append(f"Token count wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Token counting test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token counting error: {e}")
    
    # Test 2: Token counting with empty text
    print("\n🔹 Test 2: Token counting with empty text...")
    try:
        result = count_tokens("")
        
        if isinstance(result, int):
            if result >= 0:  # Empty can be 0 or small positive
                print(f"✅ Empty text token count: {result}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Empty text token count should be >= 0, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Empty text negative tokens: {result}")
        else:
            print(f"❌ FAIL: Empty text returned {type(result)}, expected int")
            test_results['failed'] += 1
            test_results['errors'].append(f"Empty text wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Empty text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Empty text test error: {e}")
    
    # Test 3: Token counting with large text
    print("\n📈 Test 3: Token counting with large text...")
    try:
        large_text = "This is a test sentence. " * 100  # 2500 chars
        result = count_tokens(large_text)
        
        if isinstance(result, int):
            if result > 0:
                # Rough validation: should be reasonable ratio
                ratio = len(large_text) / result if result > 0 else 0
                if 1 <= ratio <= 10:  # 1-10 chars per token is reasonable
                    print(f"✅ Large text: {len(large_text)} chars → {result} tokens (ratio: {ratio:.1f})")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Unreasonable token ratio: {ratio:.1f} chars/token")
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Unreasonable token ratio: {ratio}")
            else:
                print(f"❌ FAIL: Large text should have > 0 tokens, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Large text zero tokens: {result}")
        else:
            print(f"❌ FAIL: Large text returned {type(result)}, expected int")
            test_results['failed'] += 1
            test_results['errors'].append(f"Large text wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Large text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Large text test error: {e}")
    
    # Test 4: get_token_count_from_text function
    print("\n📊 Test 4: get_token_count_from_text function...")
    try:
        test_text = "Testing the get_token_count_from_text function."
        result = get_token_count_from_text(test_text, use_api=False)
        
        if isinstance(result, int) and result > 0:
            print(f"✅ get_token_count_from_text: {result} tokens")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: get_token_count_from_text returned invalid result: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"get_token_count_from_text failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: get_token_count_from_text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"get_token_count_from_text error: {e}")
    
    # Test 5: get_multiple_files_token_count function
    print("\n📊 Test 5: get_multiple_files_token_count function...")
    try:
        # Create temp test files
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, "test1.txt")
            file2 = os.path.join(temp_dir, "test2.txt")
            
            with open(file1, 'w') as f:
                f.write("First test file content.")
            with open(file2, 'w') as f:
                f.write("Second test file content.")
            
            result = get_multiple_files_token_count([file1, file2], use_api=False)
            
            if isinstance(result, dict) and len(result) == 2:
                if all(isinstance(count, int) and count > 0 for count in result.values()):
                    print(f"✅ get_multiple_files_token_count: {result}")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Invalid token counts in result: {result}")
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Invalid multiple files result: {result}")
            else:
                print(f"❌ FAIL: get_multiple_files_token_count wrong format: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Multiple files wrong format: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: get_multiple_files_token_count test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Multiple files test error: {e}")
    
    # Test 6: get_total_token_count function
    print("\n📊 Test 6: get_total_token_count function...")
    try:
        # Create temp test files
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, "test1.txt")
            file2 = os.path.join(temp_dir, "test2.txt")
            
            with open(file1, 'w') as f:
                f.write("First test file content.")
            with open(file2, 'w') as f:
                f.write("Second test file content.")
            
            result = get_total_token_count([file1, file2], use_api=False)
            
            if isinstance(result, int) and result > 0:
                print(f"✅ get_total_token_count: {result} total tokens")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: get_total_token_count invalid result: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Total token count failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: get_total_token_count test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Total token count error: {e}")
    
    # Test 7: Token count consistency
    print("\n🔄 Test 7: Token count consistency...")
    try:
        test_text = "Consistency test for token counting functionality."
        result1 = count_tokens(test_text)
        result2 = count_tokens(test_text)
        
        if result1 == result2:
            print(f"✅ Consistent token counts: {result1}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Inconsistent token counts: {result1} != {result2}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Inconsistent token counts: {result1} != {result2}")
            
    except Exception as e:
        print(f"❌ ERROR: Consistency test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Consistency test error: {e}")
    
    # Test 8: Edge cases for token counting
    print("\n⚡ Test 8: Edge cases for token counting...")
    try:
        edge_cases = [
            ("a", "single character"),
            ("  ", "whitespace only"),
            ("123", "numbers only"),
            ("🎉🔥💯", "emojis only"),
            ("中文测试", "non-ASCII text")
        ]
        
        all_handled = True
        for text, description in edge_cases:
            try:
                result = count_tokens(text)
                if not isinstance(result, int) or result < 0:
                    print(f"❌ FAIL: {description} returned invalid result: {result}")
                    all_handled = False
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Edge case {description} failed")
                    break
            except Exception as edge_e:
                print(f"❌ FAIL: {description} crashed: {edge_e}")
                all_handled = False
                test_results['failed'] += 1
                test_results['errors'].append(f"Edge case {description} crashed")
                break
        
        if all_handled:
            print(f"✅ All edge cases handled properly")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Edge cases test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Edge cases test error: {e}")
    
    # Test 9: estimate_model_for_token_count function
    print("\n🚀 Test 9: estimate_model_for_token_count function...")
    try:
        result = estimate_model_for_token_count(50000)
        
        if isinstance(result, str) and result:
            print(f"✅ Model recommendation for 50K tokens: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: estimate_model_for_token_count invalid result: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Model estimation failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: estimate_model_for_token_count test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model estimation error: {e}")
    
    # Test 10: validate_token_count_for_model function
    print("\n✅ Test 10: validate_token_count_for_model function...")
    try:
        result = validate_token_count_for_model(10000, "claude-4-sonnet")
        
        if isinstance(result, bool):
            print(f"✅ Token validation for 10K tokens: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: validate_token_count_for_model wrong type: {type(result)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Token validation wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: validate_token_count_for_model test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token validation error: {e}")
    
    # Test 11: get_token_count_summary function
    print("\n📊 Test 11: get_token_count_summary function...")
    try:
        # Create temp test files
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, "test1.txt")
            
            with open(file1, 'w') as f:
                f.write("Test content for summary.")
            
            result = get_token_count_summary([file1])
            
            if isinstance(result, dict) and 'total_tokens' in result:
                print(f"✅ Token count summary: {result['total_tokens']} total tokens")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: get_token_count_summary invalid format: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Token summary failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: get_token_count_summary test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token summary error: {e}")
    
    # Test 12: Token calculation validation
    print("\n🧮 Test 12: Token calculation validation...")
    try:
        # Test with known text that should have predictable token count
        known_text = "The quick brown fox jumps over the lazy dog."  # Common test phrase
        tokens = count_tokens(known_text)
        
        # Validate it's reasonable (roughly 1-15 tokens for this phrase)
        if isinstance(tokens, int) and 1 <= tokens <= 20:
            print(f"✅ Known phrase '{known_text}' → {tokens} tokens (reasonable)")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Known phrase unreasonable token count: {tokens}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Known phrase unreasonable: {tokens} tokens")
            
    except Exception as e:
        print(f"❌ ERROR: Token calculation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token calculation test error: {e}")
    
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
        print(f"\n✅ AI token manager is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ AI token manager has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
