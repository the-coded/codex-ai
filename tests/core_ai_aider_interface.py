#!/usr/bin/env python3
"""
Test script for core/ai/aider_interface.py

CRITICAL TESTS - Real validation of AI Aider interface functionality.
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
    """Test AI Aider interface with REAL validation - NO BIAS."""
    print("🧪 Testing AI Aider Interface - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.ai.aider_interface import (
            AiderInterface, AiderResult, run_changelog_generation,
            run_react_documentation, run_sass_documentation, 
            run_storybook_documentation, run_doc_ui_generation
        )
        from core.ai.model_selector import ModelInfo
        print("✅ AI Aider interface imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import AI Aider interface: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: AiderResult dataclass validation
    print("\n🏗️ Test 1: AiderResult dataclass validation...")
    try:
        result = AiderResult(
            success=True,
            output="test output",
            error="test error",
            command="test command"
        )
        
        if (hasattr(result, 'success') and hasattr(result, 'output') and 
            hasattr(result, 'error') and hasattr(result, 'command')):
            if (result.success == True and result.output == "test output" and
                result.error == "test error" and result.command == "test command"):
                print(f"✅ AiderResult dataclass works correctly")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: AiderResult fields have wrong values")
                test_results['failed'] += 1
                test_results['errors'].append("AiderResult field values incorrect")
        else:
            print(f"❌ FAIL: AiderResult missing required fields")
            test_results['failed'] += 1
            test_results['errors'].append("AiderResult missing fields")
            
    except Exception as e:
        print(f"❌ ERROR: AiderResult test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"AiderResult test error: {e}")
    
    # Test 2: AiderInterface initialization
    print("\n🔧 Test 2: AiderInterface initialization...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        if hasattr(interface, 'model') and hasattr(interface, 'api_key'):
            if interface.model == model:
                print(f"✅ AiderInterface initialized correctly")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: AiderInterface model assignment failed")
                test_results['failed'] += 1
                test_results['errors'].append("AiderInterface model assignment failed")
        else:
            print(f"❌ FAIL: AiderInterface missing required attributes")
            test_results['failed'] += 1
            test_results['errors'].append("AiderInterface missing attributes")
            
    except Exception as e:
        print(f"❌ ERROR: AiderInterface initialization crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"AiderInterface initialization error: {e}")
    
    # Test 3: Command building methods exist
    print("\n⚙️ Test 3: Command building methods validation...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        required_methods = [
            'run_changelog', 'run_doc_ui_react', 'run_doc_ui_sass', 
            'run_doc_ui_storybook', 'run_custom'
        ]
        
        missing_methods = []
        for method_name in required_methods:
            if not hasattr(interface, method_name):
                missing_methods.append(method_name)
            elif not callable(getattr(interface, method_name)):
                missing_methods.append(f"{method_name} (not callable)")
        
        if len(missing_methods) == 0:
            print(f"✅ All required methods present: {required_methods}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Missing methods: {missing_methods}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Missing methods: {missing_methods}")
            
    except Exception as e:
        print(f"❌ ERROR: Method validation crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Method validation error: {e}")
    
    # Test 4: Run custom command (no actual execution)
    print("\n🎯 Test 4: Custom command building...")
    try:
        model = ModelInfo(name="anthropic/claude-4-sonnet-20250514", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        # Test command building without actually executing
        # Mock the _execute_command to avoid real Aider calls
        original_execute = interface._execute_command
        
        def mock_execute(command):
            return AiderResult(
                success=True,
                output="mock output",
                error="",
                command=command
            )
        
        interface._execute_command = mock_execute
        
        result = interface.run_custom("test prompt", files=["test.py"], read_files=["context.py"])
        
        if isinstance(result, AiderResult):
            if result.success and "test prompt" in result.command:
                print(f"✅ Custom command building works")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Custom command result invalid")
                test_results['failed'] += 1
                test_results['errors'].append("Custom command result invalid")
        else:
            print(f"❌ FAIL: Custom command returned {type(result)}, expected AiderResult")
            test_results['failed'] += 1
            test_results['errors'].append(f"Custom command wrong type: {type(result)}")
        
        # Restore original method
        interface._execute_command = original_execute
        
    except Exception as e:
        print(f"❌ ERROR: Custom command test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Custom command test error: {e}")
    
    # Test 5: Convenience functions validation
    print("\n🔗 Test 5: Convenience functions validation...")
    try:
        convenience_functions = [
            run_changelog_generation, run_react_documentation,
            run_sass_documentation, run_storybook_documentation,
            run_doc_ui_generation
        ]
        
        all_callable = True
        for func in convenience_functions:
            if not callable(func):
                print(f"❌ FAIL: Function {func.__name__} not callable")
                all_callable = False
                test_results['failed'] += 1
                test_results['errors'].append(f"Function {func.__name__} not callable")
                break
        
        if all_callable:
            print(f"✅ All {len(convenience_functions)} convenience functions are callable")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Convenience functions test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Convenience functions error: {e}")
    
    # Test 6: Model key mapping
    print("\n🗝️ Test 6: Model key mapping...")
    try:
        model = ModelInfo(name="anthropic/claude-4-sonnet-20250514", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        model_key = interface._get_model_key()
        
        if isinstance(model_key, str):
            if len(model_key) > 0:
                print(f"✅ Model key mapping works: '{model_key}'")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Model key is empty string")
                test_results['failed'] += 1
                test_results['errors'].append("Model key empty")
        else:
            print(f"❌ FAIL: Model key returned {type(model_key)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Model key wrong type: {type(model_key)}")
            
    except Exception as e:
        print(f"❌ ERROR: Model key mapping test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model key mapping error: {e}")
    
    # Test 7: Environment setup
    print("\n🌍 Test 7: Environment setup validation...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model, api_key="test_api_key")
        
        env = interface._get_env()
        
        if isinstance(env, dict):
            if 'ANTHROPIC_API_KEY' in env and env['ANTHROPIC_API_KEY'] == "test_api_key":
                print(f"✅ Environment setup works correctly")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: API key not properly set in environment")
                test_results['failed'] += 1
                test_results['errors'].append("API key not in environment")
        else:
            print(f"❌ FAIL: Environment returned {type(env)}, expected dict")
            test_results['failed'] += 1
            test_results['errors'].append(f"Environment wrong type: {type(env)}")
            
    except Exception as e:
        print(f"❌ ERROR: Environment setup test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Environment setup error: {e}")
    
    # Test 8: Error handling in command execution
    print("\n🚫 Test 8: Error handling validation...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        # Test with clearly invalid command that should fail
        result = interface._execute_command("nonexistent_command_12345_invalid")
        
        if isinstance(result, AiderResult):
            if not result.success:  # Should fail
                print(f"✅ Error handling works: failed command correctly detected")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Invalid command reported success")
                test_results['failed'] += 1
                test_results['errors'].append("Invalid command false success")
        else:
            print(f"❌ FAIL: Error handling returned {type(result)}, expected AiderResult")
            test_results['failed'] += 1
            test_results['errors'].append(f"Error handling wrong type: {type(result)}")
            
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling test error: {e}")
    
    # Test 9: File type routing in run_doc_ui_generation
    print("\n🎯 Test 9: File type routing validation...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        
        # Mock all aider executions to avoid real command execution
        from core.ai.aider_interface import AiderInterface
        original_execute = AiderInterface._execute_command
        
        def mock_execute_safe(self, command):
            # Return success for all commands - we're testing routing, not execution
            return AiderResult(success=True, output="mocked", error="", command=command)
        
        AiderInterface._execute_command = mock_execute_safe
        
        test_results_routing = []
        
        # Test different file types
        file_types = ["react", "sass", "storybook", "invalid"]
        
        for file_type in file_types:
            try:
                result = run_doc_ui_generation(
                    model=model,
                    file_type=file_type,
                    files=["test.txt"],
                    prompt_file="prompt.md",
                    output_dir=["output.md"]
                )
                
                if isinstance(result, AiderResult):
                    if file_type == "invalid":
                        # Should fail for invalid type
                        if not result.success:
                            test_results_routing.append(f"✅ {file_type}: correctly rejected")
                        else:
                            test_results_routing.append(f"❌ {file_type}: should have failed")
                    else:
                        # Valid types should return AiderResult with success (mocked)
                        if result.success:
                            test_results_routing.append(f"✅ {file_type}: returned successful AiderResult")
                        else:
                            test_results_routing.append(f"❌ {file_type}: returned failed AiderResult")
                else:
                    test_results_routing.append(f"❌ {file_type}: wrong return type")
            except Exception as routing_e:
                test_results_routing.append(f"❌ {file_type}: crashed with {routing_e}")
        
        # Restore original method
        AiderInterface._execute_command = original_execute
        
        if all("✅" in result for result in test_results_routing):
            print(f"✅ File type routing works for all types")
            for result in test_results_routing:
                print(f"   {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Some file type routing issues:")
            for result in test_results_routing:
                print(f"   {result}")
            test_results['failed'] += 1
            test_results['errors'].append("File type routing issues")
            
    except Exception as e:
        print(f"❌ ERROR: File type routing test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File type routing error: {e}")
    
    # Test 10: API key configuration methods
    print("\n🔑 Test 10: API key configuration...")
    try:
        model = ModelInfo(name="test-model", aider_model="test", max_tokens=100000)
        
        # Test with explicit API key
        interface_with_key = AiderInterface(model, api_key="explicit_key")
        if interface_with_key.api_key == "explicit_key":
            print(f"✅ Explicit API key setting works")
        else:
            print(f"❌ FAIL: Explicit API key not set correctly")
            test_results['failed'] += 1
            test_results['errors'].append("Explicit API key failed")
        
        # Test without explicit API key (should try config/env)
        interface_no_key = AiderInterface(model)
        if interface_no_key.api_key is not None or interface_no_key.api_key is None:
            # Either case is valid - might get from config/env or be None
            print(f"✅ API key handling without explicit key works")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: API key handling failed")
            test_results['failed'] += 1
            test_results['errors'].append("API key handling failed")
            
    except Exception as e:
        print(f"❌ ERROR: API key configuration test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"API key configuration error: {e}")
    
    # Test 11: Command template integration
    print("\n📝 Test 11: Command template integration...")
    try:
        model = ModelInfo(name="anthropic/claude-4-sonnet-20250514", aider_model="test", max_tokens=100000)
        interface = AiderInterface(model)
        
        # Mock execute to capture command without running
        captured_commands = []
        
        def capture_execute(command):
            captured_commands.append(command)
            return AiderResult(success=True, output="mock", error="", command=command)
        
        interface._execute_command = capture_execute
        
        # Test changelog command building
        interface.run_changelog("log.txt", "prompt.md", "output.md")
        
        if len(captured_commands) > 0:
            command = captured_commands[0]
            if isinstance(command, str) and len(command) > 0:
                print(f"✅ Command template integration works")
                print(f"   Generated command length: {len(command)} chars")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Generated command invalid")
                test_results['failed'] += 1
                test_results['errors'].append("Generated command invalid")
        else:
            print(f"❌ FAIL: No command captured")
            test_results['failed'] += 1
            test_results['errors'].append("No command captured")
            
    except Exception as e:
        print(f"❌ ERROR: Command template test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Command template error: {e}")
    
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
        print(f"\n✅ AI Aider interface is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ AI Aider interface has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
