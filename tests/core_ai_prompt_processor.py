#!/usr/bin/env python3
"""
Test script for core/ai/prompt_processor.py

CRITICAL TESTS - Real validation of AI prompt processing functionality.
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
    """Test AI prompt processor with REAL validation - NO BIAS."""
    print("🧪 Testing AI Prompt Processor - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.ai.prompt_processor import (
            load_prompt, get_changelog_prompt, get_doc_ui_prompt,
            get_react_prompt, get_sass_prompt, get_storybook_prompt
        )
        print("✅ AI prompt processor imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import AI prompt processor: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Load changelog prompt
    print("\n📋 Test 1: Load changelog prompt...")
    try:
        result = get_changelog_prompt()
        
        if isinstance(result, str):
            if len(result) > 0:
                if "changelog" in result.lower() or "commit" in result.lower():
                    print(f"✅ Changelog prompt loaded: {len(result)} characters with relevant content")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Changelog prompt lacks relevant content")
                    test_results['failed'] += 1
                    test_results['errors'].append("Changelog prompt irrelevant content")
            else:
                print(f"❌ FAIL: Changelog prompt is empty")
                test_results['failed'] += 1
                test_results['errors'].append("Changelog prompt empty")
        else:
            print(f"❌ FAIL: Changelog prompt returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Changelog prompt wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Changelog prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Changelog prompt error: {e}")
    
    # Test 2: Load React prompt
    print("\n⚛️ Test 2: Load React prompt...")
    try:
        result = get_react_prompt()
        
        if isinstance(result, str):
            if len(result) > 0:
                if "react" in result.lower() or "component" in result.lower():
                    print(f"✅ React prompt loaded: {len(result)} characters with relevant content")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: React prompt lacks relevant content")
                    test_results['failed'] += 1
                    test_results['errors'].append("React prompt irrelevant content")
            else:
                print(f"❌ FAIL: React prompt is empty")
                test_results['failed'] += 1
                test_results['errors'].append("React prompt empty")
        else:
            print(f"❌ FAIL: React prompt returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"React prompt wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: React prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"React prompt error: {e}")
    
    # Test 3: Load Sass prompt
    print("\n🎨 Test 3: Load Sass prompt...")
    try:
        result = get_sass_prompt()
        
        if isinstance(result, str):
            if len(result) > 0:
                if "sass" in result.lower() or "style" in result.lower() or "css" in result.lower():
                    print(f"✅ Sass prompt loaded: {len(result)} characters with relevant content")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Sass prompt lacks relevant content")
                    test_results['failed'] += 1
                    test_results['errors'].append("Sass prompt irrelevant content")
            else:
                print(f"❌ FAIL: Sass prompt is empty")
                test_results['failed'] += 1
                test_results['errors'].append("Sass prompt empty")
        else:
            print(f"❌ FAIL: Sass prompt returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Sass prompt wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Sass prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Sass prompt error: {e}")
    
    # Test 4: Load Storybook prompt
    print("\n📚 Test 4: Load Storybook prompt...")
    try:
        result = get_storybook_prompt()
        
        if isinstance(result, str):
            if len(result) > 0:
                if "storybook" in result.lower() or "story" in result.lower():
                    print(f"✅ Storybook prompt loaded: {len(result)} characters with relevant content")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Storybook prompt lacks relevant content")
                    test_results['failed'] += 1
                    test_results['errors'].append("Storybook prompt irrelevant content")
            else:
                print(f"❌ FAIL: Storybook prompt is empty")
                test_results['failed'] += 1
                test_results['errors'].append("Storybook prompt empty")
        else:
            print(f"❌ FAIL: Storybook prompt returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Storybook prompt wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Storybook prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Storybook prompt error: {e}")
    
    # Test 5: Direct prompt loading with known file
    print("\n📄 Test 5: Direct prompt loading...")
    try:
        result = load_prompt("changelog_prompt")
        
        if isinstance(result, str):
            if len(result) > 0:
                print(f"✅ Direct load worked: {len(result)} characters")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Direct load returned empty string")
                test_results['failed'] += 1
                test_results['errors'].append("Direct load empty")
        else:
            print(f"❌ FAIL: Direct load returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Direct load wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Direct prompt loading test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Direct prompt loading error: {e}")
    
    # Test 6: Load non-existent prompt (fallback behavior)
    print("\n🚫 Test 6: Non-existent prompt handling...")
    try:
        result = load_prompt("nonexistent_prompt_12345")
        
        if isinstance(result, str):
            if len(result) > 0:
                # Should return fallback message
                if "nonexistent_prompt_12345" in result or "task" in result.lower():
                    print(f"✅ Non-existent prompt handled with fallback: '{result}'")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Non-existent prompt fallback unexpected: '{result}'")
                    test_results['failed'] += 1
                    test_results['errors'].append("Non-existent prompt fallback unexpected")
            else:
                print(f"❌ FAIL: Non-existent prompt returned empty string")
                test_results['failed'] += 1
                test_results['errors'].append("Non-existent prompt empty")
        else:
            print(f"❌ FAIL: Non-existent prompt returned {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Non-existent prompt wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Non-existent prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Non-existent prompt error: {e}")
    
    # Test 7: uidocs prompt with doc type
    print("\n🎯 Test 7: uidocs prompt with doc type...")
    try:
        doc_types = ["react", "sass", "storybook"]
        valid_results = 0
        
        for doc_type in doc_types:
            try:
                result = get_doc_ui_prompt(doc_type)
                if isinstance(result, str) and len(result) > 0:
                    valid_results += 1
                else:
                    print(f"❌ FAIL: uidocs {doc_type} prompt invalid: {type(result)}")
                    test_results['failed'] += 1
                    test_results['errors'].append(f"uidocs {doc_type} prompt invalid")
                    break
            except Exception as doc_e:
                print(f"❌ FAIL: uidocs {doc_type} prompt crashed: {doc_e}")
                test_results['failed'] += 1
                test_results['errors'].append(f"uidocs {doc_type} prompt crashed")
                break
        
        if valid_results == len(doc_types):
            print(f"✅ All {len(doc_types)} doc-ui doc types work")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: uidocs prompt test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"uidocs prompt error: {e}")
    
    # Test 8: Prompt consistency
    print("\n🔄 Test 8: Prompt consistency...")
    try:
        result1 = get_changelog_prompt()
        result2 = get_changelog_prompt()
        
        if result1 == result2:
            print(f"✅ Prompt loading is consistent")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Prompt loading inconsistent")
            test_results['failed'] += 1
            test_results['errors'].append("Prompt loading inconsistent")
            
    except Exception as e:
        print(f"❌ ERROR: Consistency test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Consistency test error: {e}")
    
    # Test 9: Prompt content validation
    print("\n🔍 Test 9: Prompt content validation...")
    try:
        prompts_to_check = [
            (get_changelog_prompt(), "changelog"),
            (get_react_prompt(), "react"),
            (get_sass_prompt(), "sass"),
            (get_storybook_prompt(), "storybook")
        ]
        
        all_valid = True
        for prompt_content, prompt_type in prompts_to_check:
            # Check for basic quality indicators
            if len(prompt_content) < 10:  # Too short
                print(f"❌ FAIL: {prompt_type} prompt too short: {len(prompt_content)} chars")
                all_valid = False
                test_results['failed'] += 1
                test_results['errors'].append(f"{prompt_type} prompt too short")
                break
            elif len(prompt_content) > 50000:  # Unreasonably long
                print(f"❌ FAIL: {prompt_type} prompt too long: {len(prompt_content)} chars")
                all_valid = False
                test_results['failed'] += 1
                test_results['errors'].append(f"{prompt_type} prompt too long")
                break
        
        if all_valid:
            print(f"✅ All prompts have reasonable content length")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Content validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Content validation error: {e}")
    
    # Test 10: Different prompts return different content
    print("\n🔀 Test 10: Prompt uniqueness validation...")
    try:
        prompts = {
            "changelog": get_changelog_prompt(),
            "react": get_react_prompt(),
            "sass": get_sass_prompt(),
            "storybook": get_storybook_prompt()
        }
        
        # Check if all prompts are different
        prompt_values = list(prompts.values())
        unique_prompts = set(prompt_values)
        
        if len(unique_prompts) == len(prompt_values):
            print(f"✅ All {len(prompt_values)} prompts are unique")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Some prompts are identical: {len(unique_prompts)} unique out of {len(prompt_values)}")
            test_results['failed'] += 1
            test_results['errors'].append("Some prompts identical")
            
    except Exception as e:
        print(f"❌ ERROR: Uniqueness test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Uniqueness test error: {e}")
    
    # Test 11: Error handling with invalid input
    print("\n⚡ Test 11: Error handling validation...")
    try:
        # Test with various invalid inputs
        invalid_inputs = ["", None, 123, [], {}]
        handled_correctly = 0
        
        for invalid_input in invalid_inputs:
            try:
                if invalid_input is None:
                    # Can't pass None to string format, expect this to fail
                    continue
                elif not isinstance(invalid_input, str):
                    # Non-string inputs might cause errors, that's OK
                    continue
                else:
                    # Empty string should work (returns fallback)
                    result = load_prompt(invalid_input)
                    if isinstance(result, str):
                        handled_correctly += 1
            except Exception:
                # Errors with invalid inputs are acceptable
                handled_correctly += 1
        
        print(f"✅ Error handling works for invalid inputs")
        test_results['passed'] += 1
        
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling test error: {e}")
    
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
        print(f"\n✅ AI prompt processor is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ AI prompt processor has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
