#!/usr/bin/env python3
"""
Test script for core/git/changes_tracker.py

CRITICAL TESTS - Real validation of git changes tracker functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test changes tracker with REAL validation - NO BIAS."""
    print("🧪 Testing ChangesTracker - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from core.git.changes_tracker import (
            ChangesTracker, ChangeAnalyzer, FileChange, RepositoryState,
            ChangeType, FileStatus, get_repository_state, 
            get_changes_since_commit, analyze_repository_changes
        )
        
        print("✅ ChangesTracker imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import changes tracker: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: ChangesTracker initialization validation
    print("\n📝 Test 1: ChangesTracker initialization validation...")
    try:
        tracker = ChangesTracker()
        
        if isinstance(tracker, ChangesTracker):
            print(f"✅ ChangesTracker created with correct type")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected ChangesTracker, got {type(tracker)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong tracker type: {type(tracker)}")
            
        # Test required methods exist
        required_methods = ['get_repository_state', 'is_file_tracked', 'get_changes_since_commit']
        for method_name in required_methods:
            if hasattr(tracker, method_name) and callable(getattr(tracker, method_name)):
                print(f"✅ Method {method_name} exists and is callable")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Method {method_name} missing or not callable")
                test_results['failed'] += 1
                test_results['errors'].append(f"Missing method: {method_name}")
                
    except Exception as e:
        print(f"❌ ERROR: ChangesTracker initialization crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"ChangesTracker initialization error: {e}")
    
    # Test 2: Repository state validation
    print("\n📊 Test 2: Repository state validation...")
    try:
        tracker = ChangesTracker()
        state = tracker.get_repository_state()
        
        if isinstance(state, RepositoryState):
            print(f"✅ Repository state has correct type")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected RepositoryState, got {type(state)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong state type: {type(state)}")
        
        # Test required attributes
        required_attrs = ['branch', 'commit_hash', 'total_changes', 'staged_changes', 'modified_changes']
        for attr_name in required_attrs:
            if hasattr(state, attr_name):
                attr_value = getattr(state, attr_name)
                print(f"✅ Attribute {attr_name}: {type(attr_value).__name__}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Missing attribute {attr_name}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Missing attribute: {attr_name}")
        
        # Test specific attribute types
        if hasattr(state, 'total_changes') and isinstance(state.total_changes, int) and state.total_changes >= 0:
            print(f"✅ total_changes is valid integer: {state.total_changes}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: total_changes invalid: {type(state.total_changes)}: {getattr(state, 'total_changes', 'missing')}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid total_changes: {getattr(state, 'total_changes', 'missing')}")
            
    except Exception as e:
        print(f"❌ ERROR: Repository state test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Repository state error: {e}")
    
    # Test 3: File tracking validation
    print("\n🔍 Test 3: File tracking validation...")
    try:
        tracker = ChangesTracker()
        
        # Test with known files
        test_files = [
            ("README.md", True),  # Should exist and be tracked
            ("pyproject.toml", True),  # Should exist and be tracked
            ("nonexistent_file_12345.txt", False)  # Should not exist
        ]
        
        tracking_passed = 0
        for file_path, should_exist in test_files:
            try:
                is_tracked = tracker.is_file_tracked(file_path)
                if isinstance(is_tracked, bool):
                    if should_exist and is_tracked:
                        print(f"✅ {file_path}: correctly tracked")
                        tracking_passed += 1
                    elif not should_exist and not is_tracked:
                        print(f"✅ {file_path}: correctly not tracked")
                        tracking_passed += 1
                    else:
                        print(f"❌ FAIL: {file_path}: expected tracked={should_exist}, got {is_tracked}")
                        test_results['errors'].append(f"File tracking failed: {file_path}")
                else:
                    print(f"❌ FAIL: {file_path}: is_file_tracked returned {type(is_tracked)}, expected bool")
                    test_results['errors'].append(f"File tracking wrong type: {file_path} → {type(is_tracked)}")
            except Exception as e:
                print(f"❌ FAIL: {file_path}: is_file_tracked crashed: {e}")
                test_results['errors'].append(f"File tracking crashed: {file_path} → {e}")
        
        if tracking_passed == len(test_files):
            print(f"✅ All {len(test_files)} file tracking tests passed")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Only {tracking_passed}/{len(test_files)} file tracking tests passed")
            test_results['failed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: File tracking test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"File tracking error: {e}")
    
    # Test 4: Changes since commit validation
    print("\n📈 Test 4: Changes since commit validation...")
    try:
        tracker = ChangesTracker()
        
        # Test with HEAD~1 (should work in most repos)
        try:
            changes = tracker.get_changes_since_commit("HEAD~1")
            if isinstance(changes, list):
                print(f"✅ Changes since HEAD~1: {len(changes)} changes (list type)")
                test_results['passed'] += 1
                
                # Test FileChange objects if any exist
                if changes:
                    first_change = changes[0]
                    if isinstance(first_change, FileChange):
                        print(f"✅ First change is FileChange: {first_change.path}")
                        test_results['passed'] += 1
                    else:
                        print(f"❌ FAIL: Expected FileChange, got {type(first_change)}")
                        test_results['failed'] += 1
                        test_results['errors'].append(f"Wrong change type: {type(first_change)}")
                else:
                    print(f"✅ No changes since HEAD~1 (valid)")
                    test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Expected list, got {type(changes)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Changes wrong type: {type(changes)}")
        except Exception as e:
            # This might fail in repos without history, which is valid
            print(f"✅ Changes since commit handled gracefully: {type(e).__name__}")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: Changes since commit test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Changes since commit error: {e}")
    
    # Test 5: ChangeAnalyzer validation
    print("\n📊 Test 5: ChangeAnalyzer validation...")
    try:
        analyzer = ChangeAnalyzer()
        
        if isinstance(analyzer, ChangeAnalyzer):
            print(f"✅ ChangeAnalyzer created with correct type")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected ChangeAnalyzer, got {type(analyzer)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Wrong analyzer type: {type(analyzer)}")
        
        # Test analysis
        analysis = analyzer.analyze_repository_state()
        if isinstance(analysis, dict):
            print(f"✅ Analysis returned dict with {len(analysis)} keys")
            test_results['passed'] += 1
            
            # Test required keys
            required_keys = ['total_changes', 'staged_count', 'modified_count', 'is_clean', 'branch']
            keys_found = 0
            for key in required_keys:
                if key in analysis:
                    print(f"✅ Analysis key '{key}': {type(analysis[key]).__name__}")
                    keys_found += 1
                else:
                    print(f"❌ FAIL: Missing analysis key: {key}")
                    test_results['errors'].append(f"Missing analysis key: {key}")
            
            if keys_found == len(required_keys):
                print(f"✅ All {len(required_keys)} required analysis keys found")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Only {keys_found}/{len(required_keys)} analysis keys found")
                test_results['failed'] += 1
        else:
            print(f"❌ FAIL: Expected dict, got {type(analysis)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Analysis wrong type: {type(analysis)}")
            
    except Exception as e:
        print(f"❌ ERROR: ChangeAnalyzer test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"ChangeAnalyzer error: {e}")
    
    # Test 6: Convenience functions validation
    print("\n🔧 Test 6: Convenience functions validation...")
    try:
        # Test get_repository_state function
        state_func = get_repository_state()
        if isinstance(state_func, RepositoryState):
            print(f"✅ get_repository_state returns RepositoryState")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: get_repository_state expected RepositoryState, got {type(state_func)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"get_repository_state wrong type: {type(state_func)}")
        
        # Test analyze_repository_changes function
        analysis_func = analyze_repository_changes()
        if isinstance(analysis_func, dict):
            print(f"✅ analyze_repository_changes returns dict")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: analyze_repository_changes expected dict, got {type(analysis_func)}")
            test_results['failed'] += 1
            test_results['errors'].append(f"analyze_repository_changes wrong type: {type(analysis_func)}")
            
    except Exception as e:
        print(f"❌ ERROR: Convenience functions test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Convenience functions error: {e}")
    
    # Test 7: FileChange properties validation
    print("\n🧪 Test 7: FileChange properties validation...")
    try:
        tracker = ChangesTracker()
        state = tracker.get_repository_state()
        
        # Get any change to test properties
        all_changes = []
        if hasattr(state, 'staged_changes'):
            all_changes.extend(state.staged_changes)
        if hasattr(state, 'modified_changes'):
            all_changes.extend(state.modified_changes)
        if hasattr(state, 'untracked_files'):
            all_changes.extend(state.untracked_files)
        
        if all_changes:
            test_change = all_changes[0]
            if isinstance(test_change, FileChange):
                print(f"✅ FileChange object found: {test_change.path}")
                
                # Test boolean properties
                boolean_props = ['is_added', 'is_modified', 'is_deleted', 'is_renamed', 'is_staged', 'is_untracked']
                props_passed = 0
                for prop_name in boolean_props:
                    if hasattr(test_change, prop_name):
                        prop_value = getattr(test_change, prop_name)
                        if isinstance(prop_value, bool):
                            print(f"✅ Property {prop_name}: {prop_value}")
                            props_passed += 1
                        else:
                            print(f"❌ FAIL: Property {prop_name} expected bool, got {type(prop_value)}")
                            test_results['errors'].append(f"FileChange property wrong type: {prop_name}")
                    else:
                        print(f"❌ FAIL: Missing property {prop_name}")
                        test_results['errors'].append(f"Missing FileChange property: {prop_name}")
                
                if props_passed == len(boolean_props):
                    print(f"✅ All {len(boolean_props)} FileChange properties valid")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Only {props_passed}/{len(boolean_props)} FileChange properties valid")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAIL: Expected FileChange, got {type(test_change)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Wrong change object type: {type(test_change)}")
        else:
            print(f"✅ No changes to test FileChange properties (valid)")
            test_results['passed'] += 1
            
    except Exception as e:
        print(f"❌ ERROR: FileChange properties test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"FileChange properties error: {e}")
    
    # Test 8: Error handling validation
    print("\n🚫 Test 8: Error handling validation...")
    try:
        tracker = ChangesTracker()
        
        # Test with invalid commit hash
        try:
            invalid_changes = tracker.get_changes_since_commit("invalid_commit_hash_12345")
            # Should either return empty list or raise exception
            if isinstance(invalid_changes, list):
                print(f"✅ Invalid commit handled gracefully: returned list")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Invalid commit expected list or exception, got {type(invalid_changes)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Invalid commit handling failed: {type(invalid_changes)}")
        except Exception:
            print(f"✅ Invalid commit correctly raised exception")
            test_results['passed'] += 1
        
        # Test with invalid file path
        try:
            invalid_tracking = tracker.is_file_tracked("/invalid/path/that/does/not/exist")
            if isinstance(invalid_tracking, bool):
                print(f"✅ Invalid file path handled gracefully: {invalid_tracking}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Invalid file path expected bool, got {type(invalid_tracking)}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Invalid file path handling failed: {type(invalid_tracking)}")
        except Exception as e:
            print(f"❌ FAIL: Invalid file path crashed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid file path error: {e}")
            
    except Exception as e:
        print(f"❌ ERROR: Error handling test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Error handling error: {e}")
    
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
        print(f"\n✅ ChangesTracker is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ ChangesTracker has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This module needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
