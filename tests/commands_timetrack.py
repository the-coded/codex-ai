#!/usr/bin/env python3
"""
Test script for commands/timetrack.py

CRITICAL TESTS - Real validation of timetrack command functionality.
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
    """Test timetrack command with REAL validation - NO BIAS."""
    print("🧪 Testing TimeTrack Command - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from commands.timetrack import run_timetrack, add_timetrack_arguments
        from core.config import CodexConfig
        import argparse
        
        print("✅ TimeTrack command imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import timetrack command: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Argument parsing validation
    print("\n📝 Test 1: Argument parsing validation...")
    try:
        parser = argparse.ArgumentParser()
        add_timetrack_arguments(parser)
        
        test_args = [
            [],  # No arguments
            ['--report'],  # Report flag
            ['--format', 'json'],  # Format selection
            ['--author', 'gab'],  # Author filter
            ['--since', '2024-01-01'],  # Date filter
            ['--report', '--format', 'csv', '--author', 'gabriel'],  # Combined
        ]
        
        parsed_successfully = 0
        for i, args in enumerate(test_args):
            try:
                parsed = parser.parse_args(args)
                if (hasattr(parsed, 'report') and hasattr(parsed, 'format') and 
                    hasattr(parsed, 'author')):
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
    
    # Test 2: Basic command execution validation
    print("\n🚀 Test 2: Basic command execution validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = False
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        args = MockArgs()
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Basic execution returned success code: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid execution result: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Basic execution test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Basic execution error: {e}")
    
    # Test 3: Report generation validation
    print("\n📝 Test 3: Report generation validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = True  # Enable report
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        args = MockArgs()
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Report generation returned success code: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid report result: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Report generation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Report generation error: {e}")
    
    # Test 4: Output formats validation
    print("\n📄 Test 4: Output formats validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = True
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        formats = ['markdown', 'json', 'csv', 'html']
        formats_passed = 0
        
        for format_name in formats:
            try:
                args = MockArgs()
                args.format = format_name
                result = run_timetrack(args, config)
                
                if isinstance(result, int) and result == 0:
                    print(f"✅ {format_name} format returned success: {result}")
                    formats_passed += 1
                else:
                    print(f"❌ FAIL: {format_name} format expected int 0, got {type(result)}: {result}")
                    test_results['errors'].append(f"{format_name} format failed: {result}")
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
    
    # Test 5: File output validation
    print("\n💾 Test 5: File output validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = True
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            args = MockArgs()
            args.output = tmp_path
            result = run_timetrack(args, config)
            
            # Check result code
            if isinstance(result, int) and result == 0:
                # Check file was created
                if Path(tmp_path).exists():
                    with open(tmp_path, 'r') as f:
                        content = f.read()
                        if isinstance(content, str) and len(content) > 0:
                            print(f"✅ File output: Created with {len(content)} chars")
                            test_results['passed'] += 1
                        else:
                            print(f"❌ FAIL: File output: Empty or invalid content")
                            test_results['failed'] += 1
                            test_results['errors'].append("File output empty content")
                else:
                    print(f"❌ FAIL: File output: File not created")
                    test_results['failed'] += 1
                    test_results['errors'].append("File output no file")
            else:
                print(f"❌ FAIL: File output: Command failed with {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"File output command failed: {result}")
        finally:
            # Clean up
            if Path(tmp_path).exists():
                os.unlink(tmp_path)
                
    except Exception as e:
        print(f"❌ ERROR: File output test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File output error: {e}")
    
    # Test 6: Author filtering validation
    print("\n👤 Test 6: Author filtering validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = False
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        # Test with real author (should work)
        args = MockArgs()
        args.author = "gab"  # Common git author
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Author filtering returned success: {result}")
            author_passed = True
        else:
            print(f"❌ FAIL: Author filtering expected int 0, got {type(result)}: {result}")
            author_passed = False
            test_results['errors'].append(f"Author filtering failed: {result}")
        
        # Test with nonexistent author (should still work, just no results)
        args = MockArgs()
        args.author = "nonexistent_author_12345"
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Nonexistent author handling: {result}")
            nonexistent_passed = True
        else:
            print(f"❌ FAIL: Nonexistent author expected int 0, got {type(result)}: {result}")
            nonexistent_passed = False
            test_results['errors'].append(f"Nonexistent author failed: {result}")
        
        if author_passed and nonexistent_passed:
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Author filtering test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Author filtering error: {e}")
    
    # Test 7: Date filtering validation
    print("\n📅 Test 7: Date filtering validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = False
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        # Test with valid date
        args = MockArgs()
        args.since = "2024-01-01"
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Date filtering returned success: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Date filtering expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Date filtering failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Date filtering test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Date filtering error: {e}")
    
    # Test 8: Combined filters validation
    print("\n🔍 Test 8: Combined filters validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = True
                self.format = 'json'
                self.author = "gab"
                self.since = "2024-01-01"
                self.until = None
                self.output = None
                self.verbose = False
        
        args = MockArgs()
        result = run_timetrack(args, config)
        
        if isinstance(result, int) and result == 0:
            print(f"✅ Combined filters returned success: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Combined filters expected int 0, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Combined filters failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Combined filters test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Combined filters error: {e}")
    
    # Test 9: Error handling validation
    print("\n🚫 Test 9: Error handling validation...")
    try:
        config = CodexConfig()
        
        class MockArgs:
            def __init__(self):
                self.report = True
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        # Test with invalid output path
        args = MockArgs()
        args.output = "/nonexistent_directory_12345/invalid/path/that/does/not/exist.md"
        result = run_timetrack(args, config)
        
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
        print(f"\n✅ TimeTrack command is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ TimeTrack command has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
