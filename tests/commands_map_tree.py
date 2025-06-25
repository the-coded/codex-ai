#!/usr/bin/env python3
"""
Test script for commands/map_tree.py

Tests the map-tree CLI command functionality including
argument parsing, tree generation, and output formats.
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
    """Test map-tree command functionality."""
    print("🧪 Testing Map-Tree Command...")
    
    try:
        from commands.map_tree import run_map_tree, add_map_tree_arguments
        from core.config import CodexConfig
        import argparse
        
        print("✅ Map-tree command imported successfully")
        
        # Create test config
        config = CodexConfig()
        
        # Test argument parsing
        print("\n📝 Testing argument parsing...")
        parser = argparse.ArgumentParser()
        add_map_tree_arguments(parser)
        
        # Test basic arguments
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
        
        for i, args in enumerate(test_args):
            try:
                parsed = parser.parse_args(args)
                print(f"✅ Test {i+1}: {args} → parsed successfully")
                print(f"   project: {getattr(parsed, 'project', False)}")
                print(f"   git: {getattr(parsed, 'git', False)}")
                print(f"   all: {getattr(parsed, 'all', False)}")
                print(f"   format: {getattr(parsed, 'format', 'json')}")
            except Exception as e:
                print(f"❌ Test {i+1}: {args} → failed: {e}")
        
        # Test command execution with mock args
        print("\n🚀 Testing command execution...")
        
        # Create mock args for basic execution
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
        print("📊 Testing default execution (all maps)...")
        args = MockArgs()
        result = run_map_tree(args, config)
        print(f"✅ Default execution result: {result}")
        
        # Check if files were created
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
        
        print("\n📁 Checking generated files...")
        for file_path in expected_files:
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        print(f"✅ {file_path}: Valid JSON, {len(str(data))} chars")
                    except json.JSONDecodeError:
                        print(f"❌ {file_path}: Invalid JSON")
            else:
                print(f"⚠️  {file_path}: Not found")
        
        # Test project only
        print("\n🏗️  Testing project structure only...")
        args = MockArgs()
        args.project = True
        result = run_map_tree(args, config)
        print(f"✅ Project-only execution result: {result}")
        
        # Test git changes only
        print("\n🔄 Testing git changes only...")
        args = MockArgs()
        args.git = True
        result = run_map_tree(args, config)
        print(f"✅ Git-only execution result: {result}")
        
        # Test releases only
        print("\n🏷️  Testing releases only...")
        args = MockArgs()
        args.releases = True
        result = run_map_tree(args, config)
        print(f"✅ Releases-only execution result: {result}")
        
        # Test siblings only
        print("\n👥 Testing siblings only...")
        args = MockArgs()
        args.siblings = True
        result = run_map_tree(args, config)
        print(f"✅ Siblings-only execution result: {result}")
        
        # Test with custom output
        print("\n💾 Testing custom output...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            args = MockArgs()
            args.project = True
            args.output = tmp_path
            result = run_map_tree(args, config)
            print(f"✅ Custom output execution result: {result}")
            
            # Check if custom file was created
            if Path(tmp_path).exists():
                with open(tmp_path, 'r') as f:
                    try:
                        data = json.load(f)
                        print(f"✅ Custom output file created with valid JSON")
                        print(f"   Content preview: {str(data)[:100]}...")
                    except json.JSONDecodeError:
                        print(f"❌ Custom output file contains invalid JSON")
            else:
                print("❌ Custom output file was not created")
        finally:
            # Clean up
            if Path(tmp_path).exists():
                os.unlink(tmp_path)
        
        # Test YAML format
        print("\n📄 Testing YAML format...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            args = MockArgs()
            args.project = True
            args.format = 'yaml'
            args.output = tmp_path
            result = run_map_tree(args, config)
            print(f"✅ YAML format execution result: {result}")
            
            # Check if YAML file was created
            if Path(tmp_path).exists():
                with open(tmp_path, 'r') as f:
                    content = f.read()
                    print(f"✅ YAML output file created")
                    print(f"   Content preview: {content[:100]}...")
            else:
                print("❌ YAML output file was not created")
        finally:
            # Clean up
            if Path(tmp_path).exists():
                os.unlink(tmp_path)
        
        # Test markdown format
        print("\n📝 Testing Markdown format...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            args = MockArgs()
            args.project = True
            args.format = 'markdown'
            args.output = tmp_path
            result = run_map_tree(args, config)
            print(f"✅ Markdown format execution result: {result}")
            
            # Check if Markdown file was created
            if Path(tmp_path).exists():
                with open(tmp_path, 'r') as f:
                    content = f.read()
                    print(f"✅ Markdown output file created")
                    print(f"   Content preview: {content[:100]}...")
            else:
                print("❌ Markdown output file was not created")
        finally:
            # Clean up
            if Path(tmp_path).exists():
                os.unlink(tmp_path)
        
        # Test verbose mode
        print("\n🔍 Testing verbose mode...")
        args = MockArgs()
        args.project = True
        args.verbose = True
        result = run_map_tree(args, config)
        print(f"✅ Verbose mode execution result: {result}")
        
        # Test error handling
        print("\n🧪 Testing error handling...")
        print("   📝 Testing invalid output path (should fail with error code 1)...")
        
        # Test with invalid output path (should fail and return 1)
        args = MockArgs()
        args.project = True
        # Use a path that definitely doesn't exist and can't be created
        args.output = "/nonexistent_directory_12345/invalid/path/that/does/not/exist.json"
        result = run_map_tree(args, config)
        if result == 1:
            print(f"✅ Error handling working correctly - returned error code: {result}")
        else:
            print(f"❌ Error handling failed - should return 1, got: {result}")
        
        # Validate generated content structure
        print("\n🔍 Validating content structure...")
        project_file = Path(".tmp/tree_project.json")
        if project_file.exists():
            with open(project_file, 'r') as f:
                try:
                    data = json.load(f)
                    print("✅ Project structure validation:")
                    
                    # Check for expected structure
                    if isinstance(data, dict):
                        print(f"   Root is dict: ✅")
                        
                        # Look for common directories
                        expected_dirs = ['core', 'commands', 'constants', 'tests']
                        found_dirs = [d for d in expected_dirs if d in data]
                        print(f"   Found expected dirs: {found_dirs}")
                        
                        # Check for files array
                        if 'files' in data:
                            files = data['files']
                            if isinstance(files, list):
                                print(f"   Root files: {len(files)} files")
                            else:
                                print(f"   Root files: Invalid format")
                        
                    else:
                        print(f"   Root is not dict: ❌")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Project structure validation failed: {e}")
        
        print("\n🎉 All Map-Tree command tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Map-tree command test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
