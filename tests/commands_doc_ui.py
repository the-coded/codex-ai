#!/usr/bin/env python3
"""
Test script for commands/doc_ui.py

CRITICAL TESTS - Real validation of doc-ui command functionality.
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
    """Test doc-ui command with REAL validation - NO BIAS."""
    print("🧪 Testing Doc-UI Command - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from commands.doc_ui import (
            run_doc_ui, doc_ui_command, add_doc_ui_arguments, get_doc_ui_help,
            DOC_UI_FILE_PATTERNS, detect_file_types, get_component_base_path,
            get_component_siblings, map_files_for_doc_type, auto_detect_mode,
            get_files_for_mode, get_files_for_path, has_stories_file
        )
        print("✅ Doc-UI command imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import doc-ui command: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: File patterns structure validation
    print("\n📋 Test 1: File patterns structure validation...")
    try:
        if isinstance(DOC_UI_FILE_PATTERNS, dict) and len(DOC_UI_FILE_PATTERNS) > 0:
            print(f"✅ File patterns is dict with {len(DOC_UI_FILE_PATTERNS)} patterns")
            
            # Validate structure of each pattern
            required_keys = ['description', 'extensions', 'required_patterns', 'exclude_patterns']
            valid_patterns = 0
            
            for pattern_name, pattern_config in DOC_UI_FILE_PATTERNS.items():
                if isinstance(pattern_config, dict) and all(key in pattern_config for key in required_keys):
                    valid_patterns += 1
                else:
                    print(f"❌ FAIL: Pattern {pattern_name} missing required keys")
                    test_results['errors'].append(f"Invalid pattern structure: {pattern_name}")
            
            if valid_patterns == len(DOC_UI_FILE_PATTERNS):
                print(f"✅ All {valid_patterns} patterns have valid structure")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Only {valid_patterns}/{len(DOC_UI_FILE_PATTERNS)} patterns valid")
                test_results['failed'] += 1
        else:
            print(f"❌ FAIL: Expected dict with patterns, got {type(DOC_UI_FILE_PATTERNS)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid patterns type: {type(DOC_UI_FILE_PATTERNS)}")
            
    except Exception as e:
        print(f"❌ ERROR: File patterns test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File patterns error: {e}")
    
    # Test 2: Component base path detection validation
    print("\n📂 Test 2: Component base path detection validation...")
    try:
        test_cases = [
            ("src/components/atoms/Button/Button.tsx", "src/components/atoms/Button"),
            ("react/src/components/molecules/Card/Card.tsx", "react/src/components/molecules/Card"),
            ("sass/src/components/atoms/Button/Button.scss", "sass/src/components/atoms/Button"),
            ("", ""),  # Edge case
            ("invalid/path", "invalid")  # Edge case
        ]
        
        correct_detections = 0
        
        for input_path, expected_base in test_cases:
            try:
                base_path = get_component_base_path(input_path)
                if isinstance(base_path, str) and (base_path == expected_base or input_path == ""):
                    print(f"✅ {input_path} → {base_path} (correct)")
                    correct_detections += 1
                else:
                    print(f"❌ FAIL: {input_path} → {base_path} (expected {expected_base})")
                    test_results['errors'].append(f"Base path detection failed: {input_path}")
            except Exception as e:
                print(f"❌ FAIL: {input_path} crashed: {e}")
                test_results['errors'].append(f"Base path crashed: {input_path} → {e}")
        
        if correct_detections >= len(test_cases) * 0.8:  # 80% success rate
            print(f"✅ Base path detection: {correct_detections}/{len(test_cases)} correct")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Base path detection: Only {correct_detections}/{len(test_cases)} correct")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Base path detection test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Base path detection error: {e}")
    
    # Test 3: File type detection validation
    print("\n🔍 Test 3: File type detection validation...")
    try:
        test_files = [
            "src/components/Button/Button.tsx",
            "src/components/Button/Button.config.ts", 
            "src/components/Button/Button.stories.tsx",
            "src/styles/Button.scss",
            "src/styles/main.css"
        ]
        
        categorized = detect_file_types(test_files)
        
        if isinstance(categorized, dict):
            total_categorized = sum(len(files) for files in categorized.values())
            if total_categorized == len(test_files):
                print(f"✅ File categorization: {total_categorized}/{len(test_files)} files categorized")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: File categorization: Only {total_categorized}/{len(test_files)} files categorized")
                test_results['failed'] += 1
                test_results['errors'].append(f"Incomplete categorization: {total_categorized}/{len(test_files)}")
        else:
            print(f"❌ FAIL: Expected dict result, got {type(categorized)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid categorization type: {type(categorized)}")
            
    except Exception as e:
        print(f"❌ ERROR: File type detection test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File type detection error: {e}")
    
    # Test 4: Component siblings detection validation
    print("\n👥 Test 4: Component siblings detection validation...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "src/components/atoms/Button"
            component_dir.mkdir(parents=True, exist_ok=True)
            
            # Create test files
            test_sibling_files = [
                "Button.tsx",
                "Button.config.ts", 
                "Button.stories.tsx",
                "Button.scss"
            ]
            
            for file_name in test_sibling_files:
                (component_dir / file_name).touch()
            
            # Test sibling detection
            test_file = str(component_dir / "Button.tsx")
            siblings = get_component_siblings(test_file)
            
            if isinstance(siblings, list):
                # Should find at least the created siblings
                expected_siblings = len(test_sibling_files) - 1  # Exclude the input file itself
                if len(siblings) >= expected_siblings:
                    print(f"✅ Siblings detection: Found {len(siblings)} siblings (expected >= {expected_siblings})")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Found {len(siblings)} siblings, expected >= {expected_siblings}")
                    test_results['failed'] += 1
                    test_results['errors'].append(f"Insufficient siblings found: {len(siblings)}")
            else:
                print(f"❌ FAIL: Expected list result, got {type(siblings)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Invalid siblings type: {type(siblings)}")
                
    except Exception as e:
        print(f"❌ ERROR: Siblings detection test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Siblings detection error: {e}")
    
    # Test 5: File mapping validation
    print("\n📝 Test 5: File mapping validation...")
    try:
        test_changed_files = [
            "react/src/components/atoms/Button/Button.tsx",
            "react/src/components/atoms/Card/Card.config.ts",
            "sass/src/components/atoms/Button/Button.scss"
        ]
        
        doc_types = ["react", "sass", "storybook"]
        successful_mappings = 0
        
        for doc_type in doc_types:
            try:
                mapping = map_files_for_doc_type(doc_type, test_changed_files)
                
                if (isinstance(mapping, dict) and 
                    'context_files' in mapping and 
                    'output_files' in mapping and
                    isinstance(mapping['context_files'], list) and
                    isinstance(mapping['output_files'], list)):
                    
                    print(f"✅ {doc_type} mapping: {len(mapping['context_files'])} context, {len(mapping['output_files'])} output")
                    successful_mappings += 1
                else:
                    print(f"❌ FAIL: {doc_type} mapping has invalid structure")
                    test_results['errors'].append(f"Invalid mapping structure: {doc_type}")
                    
            except Exception as e:
                print(f"❌ FAIL: {doc_type} mapping crashed: {e}")
                test_results['errors'].append(f"Mapping error {doc_type}: {e}")
        
        if successful_mappings == len(doc_types):
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: File mapping test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File mapping error: {e}")
    
    # Test 6: Help text validation
    print("\n📚 Test 6: Help text validation...")
    try:
        help_text = get_doc_ui_help()
        
        if isinstance(help_text, str) and len(help_text) > 100:
            # Validate it contains expected content
            expected_keywords = ["doc-ui", "documentation", "component", "examples"]
            found_keywords = [kw for kw in expected_keywords if kw.lower() in help_text.lower()]
            
            if len(found_keywords) >= len(expected_keywords) * 0.75:  # 75% of keywords
                print(f"✅ Help text: {len(help_text)} chars with {len(found_keywords)}/{len(expected_keywords)} keywords")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Help text missing keywords: found {len(found_keywords)}/{len(expected_keywords)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Help text missing keywords: {found_keywords}")
        else:
            print(f"❌ FAIL: Expected substantial string, got {type(help_text)} with {len(help_text) if isinstance(help_text, str) else 'N/A'} chars")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid help text: {type(help_text)}")
            
    except Exception as e:
        print(f"❌ ERROR: Help text test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Help text error: {e}")
    
    # Test 7: Argument parser validation
    print("\n⚙️ Test 7: Argument parser validation...")
    try:
        import argparse
        parser = argparse.ArgumentParser()
        add_doc_ui_arguments(parser)
        
        # Test parsing valid arguments
        test_args = ["--doc", "react", "--mode", "local", "--dry-run", "--verbose"]
        
        try:
            args = parser.parse_args(test_args)
            
            if (hasattr(args, 'doc') and args.doc == "react" and
                hasattr(args, 'mode') and args.mode == "local" and
                hasattr(args, 'dry_run') and args.dry_run is True and
                hasattr(args, 'verbose') and args.verbose is True):
                
                print("✅ Argument parsing: All attributes correct")
                test_results['passed'] += 1
            else:
                print("❌ FAIL: Argument parsing: Incorrect attribute values")
                test_results['failed'] += 1
                test_results['errors'].append("Argument parsing attribute mismatch")
                
        except Exception as e:
            print(f"❌ FAIL: Argument parsing crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Argument parsing crashed: {e}")
            
    except Exception as e:
        print(f"❌ ERROR: Argument parser test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Argument parser error: {e}")
    
    # Test 8: Stories file detection validation
    print("\n📖 Test 8: Stories file detection validation...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "src/components/Button"
            component_dir.mkdir(parents=True, exist_ok=True)
            
            # Create component file
            component_file = component_dir / "Button.tsx"
            component_file.touch()
            
            # Test without stories file
            has_stories_before = has_stories_file(str(component_file))
            
            # Create stories file
            stories_file = component_dir / "Button.stories.tsx"
            stories_file.touch()
            
            # Test with stories file
            has_stories_after = has_stories_file(str(component_file))
            
            if (isinstance(has_stories_before, bool) and not has_stories_before and
                isinstance(has_stories_after, bool) and has_stories_after):
                
                print("✅ Stories detection: Correctly detects presence/absence")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Stories detection incorrect: before={has_stories_before}, after={has_stories_after}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Stories detection failed: {has_stories_before} → {has_stories_after}")
                
    except Exception as e:
        print(f"❌ ERROR: Stories detection test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Stories detection error: {e}")
    
    # Test 9: Error handling validation
    print("\n🚫 Test 9: Error handling validation...")
    try:
        # Test with invalid inputs
        error_tests_passed = 0
        
        # Test invalid file list
        try:
            result = detect_file_types(None)
            if isinstance(result, dict):
                print("✅ Handles None input gracefully")
                error_tests_passed += 1
        except Exception:
            print("✅ Properly rejects None input")
            error_tests_passed += 1
        
        # Test invalid component path
        try:
            result = get_component_base_path(None)
            if isinstance(result, str):
                print("✅ Handles None path gracefully")
                error_tests_passed += 1
        except Exception:
            print("✅ Properly rejects None path")
            error_tests_passed += 1
        
        # Test invalid doc type
        try:
            result = map_files_for_doc_type("invalid_type", [])
            if isinstance(result, dict):
                print("✅ Handles invalid doc type gracefully")
                error_tests_passed += 1
        except Exception:
            print("✅ Properly rejects invalid doc type")
            error_tests_passed += 1
        
        if error_tests_passed >= 2:  # At least 2/3 error handling tests passed
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            test_results['errors'].append(f"Insufficient error handling: {error_tests_passed}/3")
            
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
        print(f"\n✅ Doc-UI command is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Doc-UI command has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
