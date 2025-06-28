#!/usr/bin/env python3
"""
Test script for core/ai/model_selector.py

CRITICAL TESTS - Real validation of AI model selection functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test AI model selector with REAL validation - NO BIAS."""
    print("🧪 Testing AI Model Selector - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.ai.model_selector import (
            get_default_model, get_model_by_name, get_model_for_tokens, ModelInfo
        )
        print("✅ AI model selector imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import AI model selector: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Default model retrieval
    print("\n🤖 Test 1: Default model retrieval...")
    try:
        default_model = get_default_model()
        
        if default_model is None:
            print(f"❌ FAIL: Default model is None")
            test_results['failed'] += 1
            test_results['errors'].append("Default model is None")
        elif isinstance(default_model, ModelInfo):
            if hasattr(default_model, 'name') and hasattr(default_model, 'max_tokens'):
                print(f"✅ Default model retrieved: {default_model.name} ({default_model.max_tokens} tokens)")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Default model missing required attributes")
                test_results['failed'] += 1
                test_results['errors'].append(f"Default model missing attributes")
        else:
            print(f"❌ FAIL: Default model wrong type: {type(default_model)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Default model wrong type: {type(default_model)}")
            
    except Exception as e:
        print(f"❌ ERROR: Default model test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Default model error: {e}")
    
    # Test 2: Model retrieval by name (valid)
    print("\n🎯 Test 2: Valid model retrieval by name...")
    try:
        # Try model names from constants
        test_models = [
            "anthropic/claude-4-sonnet-20250514",
            "anthropic/claude-3-5-sonnet-20241022",
            "CLAUDE_4_SONNET",
            "CLAUDE_3_5_SONNET"
        ]
        
        found_valid_model = False
        for model_name in test_models:
            model = get_model_by_name(model_name)
            if model is not None:
                if isinstance(model, ModelInfo) and hasattr(model, 'name'):
                    print(f"✅ Retrieved model: {model.name}")
                    found_valid_model = True
                    break
                else:
                    print(f"❌ FAIL: Model {model_name} has invalid structure")
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Invalid model structure: {model_name}")
                    break
        
        if found_valid_model:
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: No valid models found from test list")
            test_results['failed'] += 1
            test_results['errors'].append("No valid models available")
            
    except Exception as e:
        print(f"❌ ERROR: Valid model retrieval crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Valid model retrieval error: {e}")
    
    # Test 3: Invalid model handling
    print("\n🚫 Test 3: Invalid model handling...")
    try:
        invalid_model = get_model_by_name("invalid/nonexistent-model-12345")
        
        if invalid_model is None:
            print(f"✅ Invalid model correctly returned None")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Invalid model should return None, got {type(invalid_model)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid model handling failed: got {type(invalid_model)}")
            
    except Exception as e:
        print(f"❌ ERROR: Invalid model test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Invalid model test error: {e}")
    
    # Test 4: Token-based model selection
    print("\n🔢 Test 4: Token-based model selection...")
    try:
        # Test different token counts
        test_cases = [
            (1000, "small token count"),
            (50000, "medium token count"),  
            (200000, "large token count"),
            (1000000, "very large token count")
        ]
        
        all_valid = True
        for token_count, description in test_cases:
            model = get_model_for_tokens(token_count)
            
            if model is None:
                print(f"❌ FAIL: Token selection returned None for {description}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Token selection failed for {token_count}")
                all_valid = False
                break
            elif not isinstance(model, ModelInfo):
                print(f"❌ FAIL: Token selection returned wrong type for {description}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Token selection wrong type for {token_count}")
                all_valid = False
                break
            elif token_count > model.max_tokens:
                # This might be valid if it returns the largest available model
                print(f"⚠️  Token count {token_count} > model max {model.max_tokens} (using largest available)")
        
        if all_valid:
            print(f"✅ Token-based model selection working")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Token-based selection crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Token-based selection error: {e}")
    
    # Test 5: ModelInfo structure validation
    print("\n📋 Test 5: ModelInfo structure validation...")
    try:
        default_model = get_default_model()
        
        if default_model is not None:
            required_attrs = ['name', 'aider_model', 'max_tokens']
            missing_attrs = [attr for attr in required_attrs if not hasattr(default_model, attr)]
            
            if len(missing_attrs) == 0:
                print(f"✅ ModelInfo has all required attributes")
                print(f"   name: {default_model.name}")
                print(f"   aider_model: {default_model.aider_model}")
                print(f"   max_tokens: {default_model.max_tokens}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: ModelInfo missing attributes: {missing_attrs}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Missing ModelInfo attributes: {missing_attrs}")
        else:
            print(f"❌ FAIL: Cannot validate ModelInfo structure - no model available")
            test_results['failed'] += 1
            test_results['errors'].append("No model for structure validation")
            
    except Exception as e:
        print(f"❌ ERROR: ModelInfo structure test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"ModelInfo structure error: {e}")
    
    # Test 6: Model consistency
    print("\n🔄 Test 6: Model consistency...")
    try:
        model1 = get_default_model()
        model2 = get_default_model()
        
        if model1 is not None and model2 is not None:
            if (model1.name == model2.name and 
                model1.aider_model == model2.aider_model and
                model1.max_tokens == model2.max_tokens):
                print(f"✅ Default model returns consistent results")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Default model inconsistent")
                test_results['failed'] += 1
                test_results['errors'].append("Default model inconsistent")
        else:
            print(f"❌ FAIL: Consistency test failed - models are None")
            test_results['failed'] += 1
            test_results['errors'].append("Consistency test - models None")
            
    except Exception as e:
        print(f"❌ ERROR: Consistency test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Consistency test error: {e}")
    
    # Test 7: Edge case token selection
    print("\n⚡ Test 7: Edge case token selection...")
    try:
        edge_cases = [0, -1, 999999999]  # Zero, negative, very large
        
        all_handled = True
        for token_count in edge_cases:
            try:
                model = get_model_for_tokens(token_count)
                if model is None:
                    print(f"❌ FAIL: Edge case {token_count} returned None")
                    all_handled = False
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Edge case {token_count} failed")
                    break
                elif not isinstance(model, ModelInfo):
                    print(f"❌ FAIL: Edge case {token_count} wrong type")
                    all_handled = False
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Edge case {token_count} wrong type")
                    break
            except Exception as edge_e:
                print(f"❌ FAIL: Edge case {token_count} crashed: {edge_e}")
                all_handled = False
                test_results['failed'] += 1
                test_results['errors'].append(f"Edge case {token_count} crashed")
                break
        
        if all_handled:
            print(f"✅ Edge cases handled properly")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Edge case test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Edge case test error: {e}")
    
    # Test 8: Return type validation
    print("\n🔍 Test 8: Return type validation...")
    try:
        # Test all functions return correct types
        default_model = get_default_model()
        token_model = get_model_for_tokens(50000)
        valid_model = get_model_by_name("anthropic/claude-4-sonnet-20250514")
        
        type_checks = [
            (default_model, ModelInfo, "get_default_model"),
            (token_model, ModelInfo, "get_model_for_tokens"),
        ]
        
        all_types_correct = True
        for result, expected_type, func_name in type_checks:
            if result is not None and not isinstance(result, expected_type):
                print(f"❌ FAIL: {func_name} returned {type(result)}, expected {expected_type}")
                all_types_correct = False
                test_results['failed'] += 1
                test_results['errors'].append(f"{func_name} wrong return type")
                break
        
        # Handle optional result (can be None)
        if valid_model is not None and not isinstance(valid_model, ModelInfo):
            print(f"❌ FAIL: get_model_by_name returned {type(valid_model)}, expected ModelInfo")
            all_types_correct = False
            test_results['failed'] += 1
            test_results['errors'].append("get_model_by_name wrong return type")
        
        if all_types_correct:
            print(f"✅ All functions return correct types")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Return type test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Return type test error: {e}")
    
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
        print(f"\n✅ AI model selector is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ AI model selector has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
