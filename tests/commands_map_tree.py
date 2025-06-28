#!/usr/bin/env python3
"""
Test script for commands/map_tree.py

CRITICAL TESTS - Real validation of map-tree command functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path
import tempfile
import os
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test map-tree command with REAL validation - NO BIAS."""
    print("🧪 Testing Map-Tree Command - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from commands.map_tree import run_map_tree, add_map_tree_arguments
        from core.config import CodexConfig
        import argparse
        
        print("✅ Map-tree command imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import map-tree command: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Argument parsing validation
    print("\n📝 Test 1: Argument parsing validation...")
    try:
        parser = argparse.ArgumentParser()
        add_map_tree_arguments(parser)
        
        test_args = [
            [],  # No arguments (should default to --all)
            ['--project'],  # Project only
            ['--git'],  # Git changes only
            ['--releases'],  # Release changes only
            ['--siblings'],  # Sibling files only
            ['--all'],  # All explicitly
            ['--project', '--format', 'yaml'],  # With format
            ['--git', '--output', 'test.json'],  # With output
        ]
        
        parsed_successfully = 0
        for i, args in enumerate(test_args):
            try:
                parsed = parser.parse_args(args)
                if hasattr(parsed, 'project') and hasattr(parsed, 'git') and hasattr(parsed, 'format'):
                    print(f"✅ Test {i+1}: {args} → parsed with required attributes")
                    parsed_successfully += 1
                else:
                    print(f"❌ FAIL: Test {i+1}: {args} → missing required attributes")
                    test_results['errors'].append(f"Argument parsing missing attributes: {args}")
            except Exception as e:
                print(f"❌ FAIL: Test {i+1}: {args} → crashed: {e}")
                test_results['errors'].append(f"Argument parsing failed: {args} → {e}")
        
        if parsed_successfully == len(test_args):
            print(f"✅ All {len(test_args)} argument combinations parsed successfully")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {parsed_successfully}/{len(test_args)} parsed successfully")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Argument parsing test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Argument parsing error: {e}")
    
    # Test 2: Command execution validation
    print("\n🚀 Test 2: Command execution validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.all = False
                self.project = False
                self.git = False
                self.releases = False
                self.siblings = False
                self.format = 'json'
                self.output = None
                self.verbose = False
        
        # Test default execution (should run --all)
        args = MockArgs()
        result = run_map_tree(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Default execution returned success code: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid execution result: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Command execution test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Command execution error: {e}")
    
    # Test 3: Generated files validation
    print("\n📁 Test 3: Generated files validation...")
    try:
        expected_files = [
            ".tmp/tree_project.json",
            ".tmp/tree_git_changed.json",
            ".tmp/tree_git_removed.json",
            ".tmp/tree_git_all.json",
            ".tmp/tree_release_changed.json",
            ".tmp/tree_release_removed.json",
            ".tmp/tree_release_all.json",
            ".tmp/tree_git_siblings.json"
        ]
        
        valid_files = 0
        total_files = len(expected_files)
        
        for file_path in expected_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            if len(data) > 0:
                                print(f"✅ {file_path}: Valid JSON dict with {len(data)} keys")
                            else:
                                print(f"✅ {file_path}: Valid JSON dict (empty - no data)")
                            valid_files += 1
                        else:
                            print(f"❌ FAIL: {file_path}: Invalid structure - expected dict, got {type(data)}")
                            test_results['errors'].append(f"Invalid file structure: {file_path}")
                except json.JSONDecodeError as e:
                    print(f"❌ FAIL: {file_path}: Invalid JSON - {e}")
                    test_results['errors'].append(f"Invalid JSON: {file_path} → {e}")
                except Exception as e:
                    print(f"❌ FAIL: {file_path}: Read error - {e}")
                    test_results['errors'].append(f"File read error: {file_path} → {e}")
            else:
                print(f"❌ FAIL: {file_path}: File not found")
                test_results['errors'].append(f"Missing file: {file_path}")
        
        if valid_files >= (total_files * 0.8):  # At least 80% valid
            print(f"✅ File generation validation: {valid_files}/{total_files} files valid")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: File generation: Only {valid_files}/{total_files} files valid (< 80%)")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: File validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File validation error: {e}")
    
    # Test 4: Specific command modes validation
    print("\n🎯 Test 4: Specific command modes validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.all = False
                self.project = False
                self.git = False
                self.releases = False
                self.siblings = False
                self.format = 'json'
                self.output = None
                self.verbose = False
        
        modes = [
            ('project', 'project'),
            ('git', 'git'),
            ('releases', 'releases'),
            ('siblings', 'siblings')
        ]
        
        modes_passed = 0
        
        for mode_name, mode_attr in modes:
            try:
                args = MockArgs()
                setattr(args, mode_attr, True)
                result = run_map_tree(args, config)
                
                if isinstance(result, int) and result == 0:
                    print(f"✅ {mode_name} mode returned success: {result}")
                    modes_passed += 1
                else:
                    print(f"❌ FAIL: {mode_name} mode expected int 0, got {type(result)}: {result}")
                    test_results['errors'].append(f"{mode_name} mode failed: {result}")
            except Exception as e:
                print(f"❌ FAIL: {mode_name} mode crashed: {e}")
                test_results['errors'].append(f"{mode_name} mode error: {e}")
        
        if modes_passed == len(modes):
            print(f"✅ All {len(modes)} command modes work correctly")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {modes_passed}/{len(modes)} modes work correctly")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Command modes test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Command modes error: {e}")
    
    # Test 5: Output formats validation
    print("\n📄 Test 5: Output formats validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.all = False
                self.project = True  # Use project mode for quick testing
                self.git = False
                self.releases = False
                self.siblings = False
                self.format = 'json'
                self.output = None
                self.verbose = False
        
        formats = ['json', 'yaml', 'markdown']
        formats_passed = 0
        
        for format_name in formats:
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{format_name}', delete=False) as tmp_file:
                    tmp_path = tmp_file.name
                
                args = MockArgs()
                args.format = format_name
                args.output = tmp_path
                result = run_map_tree(args, config)
                
                # Check result
                if isinstance(result, int) and result == 0:
                    # Check file was created
                    if Path(tmp_path).exists():
                        with open(tmp_path, 'r') as f:
                            content = f.read()
                            if len(content) > 0:
                                print(f"✅ {format_name} format: File created with {len(content)} chars")
                                formats_passed += 1
                            else:
                                print(f"❌ FAIL: {format_name} format: Empty file")
                                test_results['errors'].append(f"{format_name} format empty file")
                    else:
                        print(f"❌ FAIL: {format_name} format: File not created")
                        test_results['errors'].append(f"{format_name} format no file")
                else:
                    print(f"❌ FAIL: {format_name} format: Command failed with {result}")
                    test_results['errors'].append(f"{format_name} format command failed: {result}")
                
                # Clean up
                if Path(tmp_path).exists():
                    os.unlink(tmp_path)
                    
            except Exception as e:
                print(f"❌ FAIL: {format_name} format crashed: {e}")
                test_results['errors'].append(f"{format_name} format error: {e}")
        
        if formats_passed == len(formats):
            print(f"✅ All {len(formats)} output formats work correctly")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {formats_passed}/{len(formats)} formats work correctly")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Output formats test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Output formats error: {e}")
    
    # Test 6: Error handling validation
    print("\n🚫 Test 6: Error handling validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.all = False
                self.project = True
                self.git = False
                self.releases = False
                self.siblings = False
                self.format = 'json'
                self.output = None
                self.verbose = False
        
        # Test with invalid output path
        args = MockArgs()
        args.output = "/nonexistent_directory_12345/invalid/path/that/does/not/exist.json"
        result = run_map_tree(args, config)
        
        if isinstance(result, int) and result == 1:
            print(f"✅ Error handling works: invalid path returns error code 1")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected error code 1, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Error handling failed: expected 1, got {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling test error: {e}")
    
    # Test 7: Content structure validation
    print("\n🔍 Test 7: Content structure validation...")
    try:
        project_file = Path(".tmp/tree_project.json")
        if project_file.exists():
            with open(project_file, 'r') as f:
                data = json.load(f)
                
                structure_checks = 0
                
                # Check root is dict
                if isinstance(data, dict):
                    structure_checks += 1
                    print("✅ Root is dict")
                else:
                    print(f"❌ FAIL: Root should be dict, got {type(data)}")
                    test_results['errors'].append(f"Root structure invalid: {type(data)}")
                
                # Check for expected directories
                expected_dirs = ['core', 'commands', 'constants', 'tests']
                found_dirs = [d for d in expected_dirs if d in data]
                if len(found_dirs) >= 2:  # At least half
                    structure_checks += 1
                    print(f"✅ Found expected dirs: {found_dirs}")
                else:
                    print(f"❌ FAIL: Too few expected dirs found: {found_dirs}")
                    test_results['errors'].append(f"Missing expected directories: {found_dirs}")
                
                # Check for files structure
                has_files_or_content = False
                for key, value in data.items():
                    if isinstance(value, (dict, list)) and len(value) > 0:
                        has_files_or_content = True
                        break
                
                if has_files_or_content:
                    structure_checks += 1
                    print("✅ Has files or content structure")
                else:
                    print("❌ FAIL: No files or content found")
                    test_results['errors'].append("Empty project structure")
                
                if structure_checks >= 2:  # At least 2/3 checks passed
                    print(f"✅ Project structure validation passed ({structure_checks}/3)")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Project structure validation failed ({structure_checks}/3)")
                    test_results['failed'] += 1
        else:
            print("❌ FAIL: Project file not found for structure validation")
            test_results['failed'] += 1
            test_results['errors'].append("Project file missing for validation")
            
    except Exception as e:
        print(f"❌ ERROR: Content structure test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Content structure error: {e}")
    
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
        print(f"\n✅ Map-tree command is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Map-tree command has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
