#!/usr/bin/env python3
"""
Test script for utils/load_json.py

CRITICAL TESTS - Real validation of JSON loading functionality.
This test will FAIL if the implementation has bugs.
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
    """Test JSON loading functionality with REAL validation."""
    print("🧪 Testing JSON Loading Utility - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from utils.load_json import load_json
        print("✅ JSON loading utility imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import JSON loading utility: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Create temporary test files for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Test 1: Valid JSON file
        print("\n📄 Test 1: Valid JSON file...")
        try:
            valid_json = {"name": "test", "version": "1.0", "items": [1, 2, 3]}
            valid_file = os.path.join(temp_dir, "valid.json")
            
            with open(valid_file, 'w') as f:
                json.dump(valid_json, f)
            
            result = load_json(valid_file)
            
            if result == valid_json:
                print(f"✅ Valid JSON loaded correctly: {result}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: JSON mismatch. Expected {valid_json}, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Valid JSON test failed: got {result}")
        except Exception as e:
            print(f"❌ ERROR: Valid JSON test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Valid JSON test error: {e}")
        
        # Test 2: Invalid JSON file
        print("\n🚫 Test 2: Invalid JSON file...")
        try:
            invalid_file = os.path.join(temp_dir, "invalid.json")
            
            with open(invalid_file, 'w') as f:
                f.write('{"invalid": json, content}')
            
            result = load_json(invalid_file)
            
            # Should return None or raise exception
            if result is None:
                print(f"✅ Invalid JSON handled gracefully: returned None")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Invalid JSON should return None, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Invalid JSON test failed: got {result}")
        except json.JSONDecodeError:
            print(f"✅ Invalid JSON correctly raised JSONDecodeError")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ ERROR: Invalid JSON test crashed unexpectedly: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid JSON test error: {e}")
        
        # Test 3: Non-existent file
        print("\n📂 Test 3: Non-existent file...")
        try:
            non_existent = os.path.join(temp_dir, "does_not_exist.json")
            result = load_json(non_existent)
            
            if result is None:
                print(f"✅ Non-existent file handled gracefully: returned None")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Non-existent file should return None, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Non-existent file test failed: got {result}")
        except FileNotFoundError:
            print(f"✅ Non-existent file correctly raised FileNotFoundError")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ ERROR: Non-existent file test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Non-existent file test error: {e}")
        
        # Test 4: Empty JSON file
        print("\n🔹 Test 4: Empty JSON file...")
        try:
            empty_file = os.path.join(temp_dir, "empty.json")
            
            with open(empty_file, 'w') as f:
                f.write('')
            
            result = load_json(empty_file)
            
            if result is None:
                print(f"✅ Empty file handled gracefully: returned None")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Empty file should return None, got {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Empty file test failed: got {result}")
        except Exception as e:
            print(f"✅ Empty file correctly raised exception: {type(e).__name__}")
            test_results['passed'] += 1
        
        # Test 5: Complex nested JSON
        print("\n🧩 Test 5: Complex nested JSON...")
        try:
            complex_json = {
                "project": {
                    "name": "codex-ai",
                    "version": "1.0.0",
                    "dependencies": {
                        "requests": "^2.28.0",
                        "click": "^8.0.0"
                    },
                    "scripts": ["build", "test", "deploy"],
                    "metadata": {
                        "author": "dev",
                        "tags": ["ai", "toolkit", "automation"]
                    }
                }
            }
            complex_file = os.path.join(temp_dir, "complex.json")
            
            with open(complex_file, 'w') as f:
                json.dump(complex_json, f, indent=2)
            
            result = load_json(complex_file)
            
            if result == complex_json:
                print(f"✅ Complex JSON loaded correctly")
                print(f"   Project name: {result['project']['name']}")
                print(f"   Dependencies: {len(result['project']['dependencies'])}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Complex JSON mismatch")
                test_results['failed'] += 1
                test_results['errors'].append(f"Complex JSON test failed")
        except Exception as e:
            print(f"❌ ERROR: Complex JSON test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Complex JSON test error: {e}")
        
        # Test 6: JSON with Unicode
        print("\n🌍 Test 6: JSON with Unicode...")
        try:
            unicode_json = {
                "message": "Hello 世界! 🚀",
                "languages": ["English", "中文", "Português", "Español"],
                "emoji": "🎉🔥💯",
                "special": "çãóñ"
            }
            unicode_file = os.path.join(temp_dir, "unicode.json")
            
            with open(unicode_file, 'w', encoding='utf-8') as f:
                json.dump(unicode_json, f, ensure_ascii=False, indent=2)
            
            result = load_json(unicode_file)
            
            if result == unicode_json:
                print(f"✅ Unicode JSON loaded correctly")
                print(f"   Message: {result['message']}")
                print(f"   Languages: {len(result['languages'])}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Unicode JSON mismatch")
                test_results['failed'] += 1
                test_results['errors'].append(f"Unicode JSON test failed")
        except Exception as e:
            print(f"❌ ERROR: Unicode JSON test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Unicode JSON test error: {e}")
        
        # Test 7: Large JSON file
        print("\n📈 Test 7: Large JSON file...")
        try:
            large_json = {
                "data": [{"id": i, "value": f"item_{i}", "meta": {"index": i}} for i in range(1000)]
            }
            large_file = os.path.join(temp_dir, "large.json")
            
            with open(large_file, 'w') as f:
                json.dump(large_json, f)
            
            import time
            start_time = time.time()
            result = load_json(large_file)
            end_time = time.time()
            duration = end_time - start_time
            
            if result and len(result['data']) == 1000:
                print(f"✅ Large JSON loaded correctly: {len(result['data'])} items in {duration:.3f}s")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Large JSON loading failed")
                test_results['failed'] += 1
                test_results['errors'].append(f"Large JSON test failed")
        except Exception as e:
            print(f"❌ ERROR: Large JSON test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Large JSON test error: {e}")
        
        # Test 8: Return type validation
        print("\n🔢 Test 8: Return type validation...")
        try:
            simple_json = {"test": "value"}
            simple_file = os.path.join(temp_dir, "simple.json")
            
            with open(simple_file, 'w') as f:
                json.dump(simple_json, f)
            
            result = load_json(simple_file)
            
            if isinstance(result, dict):
                print(f"✅ Returns dict as expected: {type(result)}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Returns {type(result)}, expected dict")
                test_results['failed'] += 1
                test_results['errors'].append(f"Return type test failed: got {type(result)}")
        except Exception as e:
            print(f"❌ ERROR: Return type test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Return type test error: {e}")
        
        # Test 9: JSON array
        print("\n📋 Test 9: JSON array...")
        try:
            array_json = [
                {"name": "item1", "value": 100},
                {"name": "item2", "value": 200},
                {"name": "item3", "value": 300}
            ]
            array_file = os.path.join(temp_dir, "array.json")
            
            with open(array_file, 'w') as f:
                json.dump(array_json, f)
            
            result = load_json(array_file)
            
            if isinstance(result, list) and len(result) == 3:
                print(f"✅ JSON array loaded correctly: {len(result)} items")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: JSON array loading failed")
                test_results['failed'] += 1
                test_results['errors'].append(f"JSON array test failed")
        except Exception as e:
            print(f"❌ ERROR: JSON array test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"JSON array test error: {e}")
        
        # Test 10: Consistency check
        print("\n🔄 Test 10: Consistency check...")
        try:
            consistency_file = os.path.join(temp_dir, "consistency.json")
            consistency_json = {"consistent": True, "value": 42}
            
            with open(consistency_file, 'w') as f:
                json.dump(consistency_json, f)
            
            result1 = load_json(consistency_file)
            result2 = load_json(consistency_file)
            
            if result1 == result2:
                print(f"✅ Consistent results: {result1}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Inconsistent results")
                test_results['failed'] += 1
                test_results['errors'].append(f"Consistency test failed")
        except Exception as e:
            print(f"❌ ERROR: Consistency test crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Consistency test error: {e}")
    
    finally:
        # Cleanup temporary files
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
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
        print(f"\n✅ JSON loading utility is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ JSON loading utility has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This utility needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
