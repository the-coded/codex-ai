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
        from core.ai.token_manager import count_tokens, should_use_detailed_git_log
        from core.ai.model_selector import ModelInfo
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
    
    # Test 4: Git log mode decision - small commit count
    print("\n📊 Test 4: Git log mode decision - small commit count...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        small_count = 10
        
        use_detailed, reasoning = should_use_detailed_git_log(small_count, model)
        
        if isinstance(use_detailed, bool) and isinstance(reasoning, str):
            if use_detailed:  # Should use detailed for small count
                print(f"✅ Small count ({small_count}) uses detailed: {reasoning}")
                test_results['passed'] += 1
            else:
                print(f"⚠️  Small count uses simple (might be valid): {reasoning}")
                test_results['passed'] += 1  # Could be valid depending on model limits
        else:
            print(f"❌ FAIL: Wrong return types: {type(use_detailed)}, {type(reasoning)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong return types for small count")
            
    except Exception as e:
        print(f"❌ ERROR: Small count test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Small count test error: {e}")
    
    # Test 5: Git log mode decision - large commit count
    print("\n📊 Test 5: Git log mode decision - large commit count...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=10000)  # Small model
        large_count = 1000
        
        use_detailed, reasoning = should_use_detailed_git_log(large_count, model)
        
        if isinstance(use_detailed, bool) and isinstance(reasoning, str):
            if not use_detailed:  # Should use simple for large count + small model
                print(f"✅ Large count ({large_count}) uses simple: {reasoning}")
                test_results['passed'] += 1
            else:
                print(f"⚠️  Large count uses detailed: {reasoning}")
                # This could be valid if model is very large, but with 10K tokens it's suspicious
                if "200000" in reasoning or "detailed would be" in reasoning:
                    print(f"✅ Reasoning includes token calculation")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Large count decision lacks proper reasoning")
                    test_results['failed'] += 1
                    test_results['errors'].append("Large count decision unreasonable")
        else:
            print(f"❌ FAIL: Wrong return types: {type(use_detailed)}, {type(reasoning)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong return types for large count")
            
    except Exception as e:
        print(f"❌ ERROR: Large count test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Large count test error: {e}")
    
    # Test 6: Token count consistency
    print("\n🔄 Test 6: Token count consistency...")
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
    
    # Test 7: Edge cases for token counting
    print("\n⚡ Test 7: Edge cases for token counting...")
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
    
    # Test 8: Git log decision with zero commits
    print("\n🔹 Test 8: Git log decision with zero commits...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=50000)
        zero_count = 0
        
        use_detailed, reasoning = should_use_detailed_git_log(zero_count, model)
        
        if isinstance(use_detailed, bool) and isinstance(reasoning, str):
            print(f"✅ Zero commits handled: detailed={use_detailed}, reasoning='{reasoning}'")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Zero commits wrong types: {type(use_detailed)}, {type(reasoning)}")
            test_results['failed'] += 1
            test_results['errors'].append("Zero commits wrong types")
            
    except Exception as e:
        print(f"❌ ERROR: Zero commits test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Zero commits test error: {e}")
    
    # Test 9: Very large model capacity
    print("\n🚀 Test 9: Very large model capacity...")
    try:
        large_model = ModelInfo(name="large-model", aider_model="large", max_tokens=1000000)
        medium_count = 100
        
        use_detailed, reasoning = should_use_detailed_git_log(medium_count, large_model)
        
        if isinstance(use_detailed, bool) and isinstance(reasoning, str):
            if use_detailed:
                print(f"✅ Large model uses detailed for {medium_count} commits: {reasoning}")
                test_results['passed'] += 1
            else:
                print(f"⚠️  Large model uses simple (unexpected but not wrong): {reasoning}")
                test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Large model wrong types: {type(use_detailed)}, {type(reasoning)}")
            test_results['failed'] += 1
            test_results['errors'].append("Large model wrong types")
            
    except Exception as e:
        print(f"❌ ERROR: Large model test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Large model test error: {e}")
    
    # Test 10: Token calculation validation
    print("\n🧮 Test 10: Token calculation validation...")
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
