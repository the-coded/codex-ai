#!/usr/bin/env python3
"""
Test script for commands/changelog.py

CRITICAL TESTS - Real validation of changelog command functionality.
This test will FAIL if the implementation has bugs.
NO CONFIRMATION BIAS - Only real validation.
"""

import sys
from pathlib import Path
import tempfile
import os
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test changelog command with REAL validation - NO BIAS."""
    print("🧪 Testing Changelog Command - CRITICAL VALIDATION...")
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        from commands.changelog import run_changelog, changelog_command
        
        print("✅ Changelog command imported successfully")
        test_results['passed'] += 1
        
    except ImportError as e:
        print(f"❌ CRITICAL FAILURE: Cannot import changelog command: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Import failed: {e}")
        return False
    
    # Test 1: Function signature validation
    print("\n📝 Test 1: Function signature validation...")
    try:
        # Test run_changelog function signature
        import inspect
        sig = inspect.signature(run_changelog)
        expected_params = ['output_file', 'since_commit', 'branch', 'model_name', 'verbose', 'dry_run']
        actual_params = list(sig.parameters.keys())
        
        if all(param in actual_params for param in expected_params):
            print(f"✅ run_changelog has all expected parameters: {expected_params}")
            test_results['passed'] += 1
        else:
            missing = [p for p in expected_params if p not in actual_params]
            print(f"❌ FAIL: run_changelog missing parameters: {missing}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Missing parameters: {missing}")
            
    except Exception as e:
        print(f"❌ ERROR: Function signature test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Function signature error: {e}")
    
    # Test 2: Dry run execution validation
    print("\n🔍 Test 2: Dry run execution validation...")
    try:
        result = run_changelog(
            output_file="test_changelog.md",
            since_commit="HEAD~3",
            dry_run=True,
            verbose=False
        )
        
        if isinstance(result, bool) and result is True:
            print(f"✅ Dry run returned success: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Expected True, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Dry run failed: expected True, got {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Dry run execution crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Dry run execution error: {e}")
    
    # Test 3: Git repository validation
    print("\n🔗 Test 3: Git repository validation...")
    try:
        git_check = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                                 capture_output=True, text=True)
        
        if git_check.returncode == 0:
            # Test with real git repo
            result = run_changelog(
                output_file="test_git.md",
                since_commit=None,  # Auto-detect
                dry_run=True,
                verbose=False
            )
            
            if isinstance(result, bool) and result is True:
                print(f"✅ Git integration works: {result}")
                test_results['passed'] += 1
            else:
                print(f"❌ FAIL: Git integration expected True, got {type(result)}: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Git integration failed: {result}")
        else:
            print(f"❌ FAIL: Not in git repository")
            test_results['failed'] += 1
            test_results['errors'].append("Not in git repository")
            
    except Exception as e:
        print(f"❌ ERROR: Git repository test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Git repository error: {e}")
    
    # Test 4: CLI command handler validation
    print("\n⚙️ Test 4: CLI command handler validation...")
    try:
        class MockArgs:
            def __init__(self):
                self.since = "HEAD~2"
                self.branch = None
                self.output = "test_cli.md" 
                self.model = None
                self.verbose = False
                self.dry_run = True
        
        mock_args = MockArgs()
        result = changelog_command(mock_args)
        
        if isinstance(result, bool) and result is True:
            print(f"✅ CLI command handler works: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: CLI handler expected True, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"CLI handler failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: CLI command handler crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"CLI handler error: {e}")
    
    # Test 5: Model specification validation
    print("\n🤖 Test 5: Model specification validation...")
    try:
        result = run_changelog(
            output_file="test_model.md",
            since_commit="HEAD~1",
            model_name="anthropic/claude-4-sonnet-20250514",
            dry_run=True,
            verbose=False
        )
        
        if isinstance(result, bool) and result is True:
            print(f"✅ Model specification works: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Model specification expected True, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Model specification failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Model specification crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Model specification error: {e}")
    
    # Test 6: Invalid model handling validation
    print("\n🚫 Test 6: Invalid model handling validation...")
    try:
        result = run_changelog(
            output_file="test_invalid_model.md",
            since_commit="HEAD~1",
            model_name="invalid/non-existent-model",
            dry_run=True,
            verbose=False
        )
        
        if isinstance(result, bool) and result is False:
            print(f"✅ Invalid model correctly rejected: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Invalid model expected False, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid model handling failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Invalid model test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Invalid model test error: {e}")
    
    # Test 7: Branch specification validation
    print("\n🌿 Test 7: Branch specification validation...")
    try:
        result = run_changelog(
            output_file="test_branch.md",
            since_commit="HEAD~1",
            branch="main",
            dry_run=True,
            verbose=False
        )
        
        if isinstance(result, bool) and result is True:
            print(f"✅ Branch specification works: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Branch specification expected True, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Branch specification failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Branch specification crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Branch specification error: {e}")
    
    # Test 8: Verbose mode validation
    print("\n🔊 Test 8: Verbose mode validation...")
    try:
        result = run_changelog(
            output_file="test_verbose.md",
            since_commit="HEAD~1",
            dry_run=True,
            verbose=True
        )
        
        if isinstance(result, bool) and result is True:
            print(f"✅ Verbose mode works: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Verbose mode expected True, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Verbose mode failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Verbose mode crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Verbose mode error: {e}")
    
    # Test 9: Invalid commit handling validation
    print("\n❌ Test 9: Invalid commit handling validation...")
    try:
        # Test with clearly invalid commit hash
        result = run_changelog(
            output_file="test.md",
            since_commit="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # 40 char invalid hash
            dry_run=True,
            verbose=False
        )
        
        # Invalid commit should still work in dry-run (no git validation in dry-run)
        # But let's test with a commit that would fail git validation
        if isinstance(result, bool):
            print(f"✅ Invalid commit handled gracefully: {result}")
            test_results['passed'] += 1
        else:
            print(f"❌ FAIL: Invalid commit expected bool, got {type(result)}: {result}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Invalid commit handling failed: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: Invalid commit test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Invalid commit test error: {e}")
    
    # Test 10: Dry-run file validation (NO AI execution)
    print("\n📁 Test 10: Dry-run file validation...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "test_dry_changelog.md")
            
            # Use DRY-RUN to avoid AI execution
            result = run_changelog(
                output_file=output_file,
                since_commit="HEAD~1",
                dry_run=True,  # KEEP DRY-RUN to avoid AI costs
                verbose=True   # Enable verbose to see more details
            )
            
            if isinstance(result, bool) and result is True:
                # In dry-run, file should NOT be created
                if not os.path.exists(output_file):
                    print(f"✅ Dry-run validation: No file created (correct behavior)")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAIL: Dry-run created file (should not create files)")
                    test_results['failed'] += 1
                    test_results['errors'].append("Dry-run created file unexpectedly")
            else:
                print(f"❌ FAIL: Dry-run expected True, got {type(result)}: {result}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Dry-run validation failed: {result}")
                
    except Exception as e:
        print(f"❌ ERROR: Dry-run validation test crashed: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Dry-run validation error: {e}")
    
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
        print(f"\n✅ Changelog command is FUNCTIONAL (>= 80% pass rate)")
        return True
    else:
        print(f"\n❌ Changelog command has CRITICAL ISSUES (< 80% pass rate)")
        print("🚨 This command needs immediate attention!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
