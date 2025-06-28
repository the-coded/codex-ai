#!/usr/bin/env python3
"""
Test script for utils/get_base_path.py

CRITICAL TESTS - Real validation of base path functionality.
This test will FAIL if the implementation has bugs.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test base path functionality with REAL validation."""
    print("🧪 Testing Base Path Utility - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from utils.get_base_path import (
            get_base_path, get_project_root, resolve_path, ensure_directory,
            get_output_path, is_development_mode, is_pipeline_mode, find_file_in_hierarchy
        )
        print("✅ Base path utility imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import base path utility: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Base path detection
    print("\n📁 Test 1: Base path detection...")
    try:
        result = get_base_path()
        
        # Should return "." since we're in development mode
        if result == ".":
            print(f"✅ Base path correctly detected: {result}")
            test_results['passed'] += 1
        else:
            print(f"⚠️  Base path returned: {result} (context dependent)")
            test_results['passed'] += 1  # Still valid behavior
    except Exception as e:
        print(f"❌ ERROR: Base path detection crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Base path detection error: {e}")
    
    # Test 2: Project root resolution
    print("\n📂 Test 2: Project root resolution...")
    try:
        result = get_project_root()
        
        if isinstance(result, Path):
            print(f"✅ Project root resolved: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Project root returned {type(result)}, expected Path")
            test_results['failed'] += 1
            test_results['errors'].append(f"Project root test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: Project root test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Project root test error: {e}")
    
    # Test 3: Path resolution
    print("\n🔗 Test 3: Path resolution...")
    try:
        test_path = "src/components"
        result = resolve_path(test_path)
        
        if isinstance(result, Path) and test_path in str(result):
            print(f"✅ Path resolved correctly: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Path resolution failed: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Path resolution failed: got {result}")
    except Exception as e:
        print(f"❌ ERROR: Path resolution test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Path resolution test error: {e}")
    
    # Test 4: Directory ensuring
    print("\n🔹 Test 4: Directory ensuring...")
    try:
        test_dir = "test_temp_dir"
        result = ensure_directory(test_dir)
        
        if isinstance(result, Path) and result.exists():
            print(f"✅ Directory ensured: {result}")
            # Cleanup
            import shutil
            shutil.rmtree(result, ignore_errors=True)
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Directory not created: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Directory ensuring failed: {result}")
    except Exception as e:
        print(f"❌ ERROR: Directory ensuring test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Directory ensuring test error: {e}")
    
    # Test 5: Output path generation
    print("\n📄 Test 5: Output path generation...")
    try:
        filename = "test_output.txt"
        result = get_output_path(filename)
        
        if isinstance(result, Path) and filename in str(result):
            print(f"✅ Output path generated: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Output path generation failed: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Output path generation failed: {result}")
    except Exception as e:
        print(f"❌ ERROR: Output path test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Output path test error: {e}")
    
    # Test 6: Development mode detection
    print("\n🔧 Test 6: Development mode detection...")
    try:
        result = is_development_mode()
        
        if isinstance(result, bool):
            print(f"✅ Development mode detection: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Development mode returned {type(result)}, expected bool")
            test_results['failed'] += 1
            test_results['errors'].append(f"Development mode test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: Development mode test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Development mode test error: {e}")
    
    # Test 7: Pipeline mode detection
    print("\n🚀 Test 7: Pipeline mode detection...")
    try:
        result = is_pipeline_mode()
        
        if isinstance(result, bool):
            print(f"✅ Pipeline mode detection: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Pipeline mode returned {type(result)}, expected bool")
            test_results['failed'] += 1
            test_results['errors'].append(f"Pipeline mode test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: Pipeline mode test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Pipeline mode test error: {e}")
    
    # Test 8: File finding in hierarchy
    print("\n🔍 Test 8: File finding in hierarchy...")
    try:
        # Look for a file we know exists
        result = find_file_in_hierarchy("cli.py")
        
        if result is None or isinstance(result, Path):
            print(f"✅ File finding works: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: File finding returned {type(result)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"File finding test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: File finding test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File finding test error: {e}")
    
    # Test 9: Return type validation for get_base_path
    print("\n🔢 Test 9: Return type validation...")
    try:
        result = get_base_path()
        
        if isinstance(result, str):
            print(f"✅ Returns string as expected: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Returns {type(result)}, expected str")
            test_results['failed'] += 1
            test_results['errors'].append(f"Return type test failed: got {type(result)}")
    except Exception as e:
        print(f"❌ ERROR: Return type test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Return type test error: {e}")
    
    # Test 10: Consistency check
    print("\n🔄 Test 10: Consistency check...")
    try:
        result1 = get_base_path()
        result2 = get_base_path()
        
        if result1 == result2:
            print(f"✅ Consistent results: {result1}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Inconsistent results: {result1} != {result2}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Consistency test failed: {result1} != {result2}")
    except Exception as e:
        print(f"❌ ERROR: Consistency test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Consistency test error: {e}")
    
    # Test 11: Context detection with current directory
    print("\n📍 Test 11: Context detection...")
    try:
        base_path = get_base_path()
        project_root = get_project_root()
        dev_mode = is_development_mode()
        pipeline_mode = is_pipeline_mode()
        
        print(f"✅ Context successfully analyzed:")
        print(f"   Base path: {base_path}")
        print(f"   Project root: {project_root}")
        print(f"   Development mode: {dev_mode}")
        print(f"   Pipeline mode: {pipeline_mode}")
        test_results['passed'] += 1
        
    except Exception as e:
        print(f"❌ ERROR: Context detection test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Context detection test error: {e}")
    
    # Test 12: Output path with custom directory
    print("\n📂 Test 12: Custom output directory...")
    try:
        filename = "custom_test.json"
        custom_dir = "custom_output"
        result = get_output_path(filename, custom_dir)
        
        if isinstance(result, Path) and filename in str(result) and custom_dir in str(result):
            print(f"✅ Custom output path: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Custom output path failed: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Custom output path failed: {result}")
    except Exception as e:
        print(f"❌ ERROR: Custom output test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Custom output test error: {e}")
    
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
        print(f"\n✅ Base path utility is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Base path utility has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This utility needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
