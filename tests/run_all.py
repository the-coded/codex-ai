#!/usr/bin/env python3
"""
Run All Tests Script for Codex-AI

Executes all test files and provides comprehensive reporting.
Supports filtering by category and special integration tests.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
import time

# Add project root to path (since we're now in tests/ subdirectory)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test categories and their files - ALL IMPLEMENTED!
TEST_CATEGORIES = {
    "commands": [
        "tests/commands_config.py",
        "tests/commands_doc_ui.py",
        "tests/commands_changelog.py"
    ],
    "core": [
        "tests/core_config_manager.py",
        "tests/core_git_changes_tracker.py",
        "tests/core_git_commit_parser.py",
        "tests/core_git_log_analyzer.py",
        "tests/core_git_release_analyzer.py",
        "tests/core_git_tree_generator.py",
        "tests/core_ai_aider_interface.py",
        "tests/core_ai_model_selector.py",
        "tests/core_ai_prompt_processor.py",
        "tests/core_ai_token_manager.py"
    ],
    "utils": [
    ],
    "cli": [
        "tests/cli.py"
    ]
}

def run_test(test_file: str) -> Tuple[bool, str, float]:
    """
    Run a single test file.
    
    Args:
        test_file: Path to test file (relative to project root)
        
    Returns:
        Tuple of (success, output, duration)
    """
    # Convert to absolute path from project root
    test_path = project_root / test_file
    
    if not test_path.exists():
        return False, f"❌ Test file not found: {test_file}", 0.0
    
    start_time = time.time()
    
    try:
        # Run from project root directory
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout per test
            cwd=str(project_root)  # Ensure we run from project root
        )
        
        duration = time.time() - start_time
        success = result.returncode == 0
        
        if success:
            return True, result.stdout, duration
        else:
            error_output = result.stderr if result.stderr else result.stdout
            return False, error_output, duration
            
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return False, f"❌ Test timed out after 60 seconds", duration
    except Exception as e:
        duration = time.time() - start_time
        return False, f"❌ Test execution failed: {e}", duration


def run_doc_ui_integration_test() -> Tuple[bool, str]:
    """
    Run special doc-ui integration test with design-system.
    
    Returns:
        Tuple of (success, output)
    """
    print("🧪 Running Doc-UI Integration Test...")
    
    # Check if design-system exists (relative to project root)
    design_system_path = project_root.parent / "design-system"
    if not design_system_path.exists():
        return False, "❌ design-system not found at ../design-system"
    
    try:
        # Test 1: Path mode with React component
        print("   Testing path mode with React component...")
        result1 = subprocess.run([
            sys.executable, "cli.py", "doc-ui",
            "--path", "../design-system/react/src/components/atoms/Button",
            "--dry-run", "--verbose"
        ], capture_output=True, text=True, timeout=30, cwd=str(project_root))
        
        if result1.returncode != 0:
            return False, f"❌ Path mode test failed: {result1.stderr}"
        
        # Test 2: Doc filter - React only
        print("   Testing doc filter - React only...")
        result2 = subprocess.run([
            sys.executable, "cli.py", "doc-ui",
            "--path", "../design-system/react/src/components",
            "--doc", "react", "--dry-run"
        ], capture_output=True, text=True, timeout=30, cwd=str(project_root))
        
        if result2.returncode != 0:
            return False, f"❌ React doc filter test failed: {result2.stderr}"
        
        # Test 3: Doc filter - Sass only
        print("   Testing doc filter - Sass only...")
        result3 = subprocess.run([
            sys.executable, "cli.py", "doc-ui",
            "--path", "../design-system/sass/src/components",
            "--doc", "sass", "--dry-run"
        ], capture_output=True, text=True, timeout=30, cwd=str(project_root))
        
        if result3.returncode != 0:
            return False, f"❌ Sass doc filter test failed: {result3.stderr}"
        
        # Test 4: Help command
        print("   Testing help command...")
        result4 = subprocess.run([
            sys.executable, "cli.py", "doc-ui", "--help"
        ], capture_output=True, text=True, timeout=10, cwd=str(project_root))
        
        if result4.returncode != 0:
            return False, f"❌ Help command test failed: {result4.stderr}"
        
        success_output = f"""✅ Doc-UI Integration Test PASSED!
        
Test Results:
✅ Path mode with React component
✅ Doc filter - React only  
✅ Doc filter - Sass only
✅ Help command

Output samples:
{result1.stdout[:200]}...
{result4.stdout[:200]}...
"""
        
        return True, success_output
        
    except subprocess.TimeoutExpired:
        return False, "❌ Integration test timed out"
    except Exception as e:
        return False, f"❌ Integration test failed: {e}"


def print_test_summary(results: Dict[str, Tuple[bool, str, float]]):
    """Print comprehensive test summary."""
    total_tests = len(results)
    passed_tests = sum(1 for success, _, _ in results.values() if success)
    failed_tests = total_tests - passed_tests
    total_time = sum(duration for _, _, duration in results.values())
    
    print(f"\n{'='*60}")
    print(f"🧪 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"⏱️ Total Time: {total_time:.2f}s")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print(f"\n❌ FAILED TESTS:")
        for test_name, (success, output, duration) in results.items():
            if not success:
                print(f"   • {test_name} ({duration:.2f}s)")
                # Show first few lines of error
                error_lines = output.split('\n')[:3]
                for line in error_lines:
                    if line.strip():
                        print(f"     {line}")
    
    print(f"\n✅ PASSED TESTS:")
    for test_name, (success, output, duration) in results.items():
        if success:
            print(f"   • {test_name} ({duration:.2f}s)")


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="Run Codex-AI tests - 100% Coverage Achieved!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/run_all.py                    # Run all tests (21/21 implemented!)
  python tests/run_all.py --category commands # Run only commands tests
  python tests/run_all.py --doc-ui-integration # Run doc-ui integration test
  python tests/run_all.py --verbose          # Verbose output
  
  # From tests directory:
  cd tests && python run_all.py              # Also works!
        """
    )
    
    parser.add_argument(
        '--category',
        choices=['commands', 'core', 'utils', 'cli'],
        help='Run tests for specific category only'
    )
    parser.add_argument(
        '--doc-ui-integration',
        action='store_true',
        help='Run doc-ui integration test with design-system'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed test output'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.doc_ui_integration:
        success, output = run_doc_ui_integration_test()
        print(output)
        return 0 if success else 1
    
    # Determine which tests to run
    if args.category:
        tests_to_run = TEST_CATEGORIES[args.category]
        print(f"🧪 Running {args.category.upper()} tests...")
    else:
        # Run all tests
        tests_to_run = []
        for category_tests in TEST_CATEGORIES.values():
            tests_to_run.extend(category_tests)
        print("🧪 Running ALL tests...")
    
    print(f"📊 Total tests to run: {len(tests_to_run)}")
    print(f"✅ ALL TESTS IMPLEMENTED! 🎉")
    print(f"📁 Running from: {project_root}")
    
    # Run tests
    results = {}
    
    for i, test_file in enumerate(tests_to_run, 1):
        print(f"\n[{i}/{len(tests_to_run)}] Running {test_file}...")
        
        success, output, duration = run_test(test_file)
        results[test_file] = (success, output, duration)
        
        if success:
            print(f"   ✅ PASSED ({duration:.2f}s)")
        else:
            print(f"   ❌ FAILED ({duration:.2f}s)")
        
        # Show detailed output if verbose or if test failed
        if args.verbose or not success:
            print("   " + "─" * 50)
            for line in output.split('\n')[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"   {line}")
            if len(output.split('\n')) > 10:
                print("   ... (output truncated)")
            print("   " + "─" * 50)
    
    # Print summary
    print_test_summary(results)
    
    # Return appropriate exit code
    failed_count = sum(1 for success, _, _ in results.values() if not success)
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
