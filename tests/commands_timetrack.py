#!/usr/bin/env python3
"""
Test script for commands/timetrack.py

Tests the timetrack CLI command functionality including
argument parsing, filtering, and output generation.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test timetrack command functionality."""
    print("🧪 Testing TimeTrack Command...")
    
    try:
        from commands.timetrack import run_timetrack, add_timetrack_arguments
        from config import CodexConfig
        import argparse
        
        print("✅ TimeTrack command imported successfully")
        
        # Create test config
        config = CodexConfig()
        
        # Test argument parsing
        print("\n📝 Testing argument parsing...")
        parser = argparse.ArgumentParser()
        add_timetrack_arguments(parser)
        
        # Test basic arguments
        test_args = [
            [],  # No arguments
            ['--report'],  # Report flag
            ['--format', 'json'],  # Format selection
            ['--author', 'gab'],  # Author filter
            ['--since', '2024-01-01'],  # Date filter
            ['--report', '--format', 'csv', '--author', 'gabriel'],  # Combined
        ]
        
        for i, args in enumerate(test_args):
            try:
                parsed = parser.parse_args(args)
                print(f"✅ Test {i+1}: {args} → parsed successfully")
                print(f"   report: {getattr(parsed, 'report', False)}")
                print(f"   format: {getattr(parsed, 'format', 'markdown')}")
                print(f"   author: {getattr(parsed, 'author', None)}")
            except Exception as e:
                print(f"❌ Test {i+1}: {args} → failed: {e}")
        
        # Test command execution with mock args
        print("\n🚀 Testing command execution...")
        
        # Create mock args for basic execution
        class MockArgs:
            def __init__(self):
                self.report = False
                self.format = 'markdown'
                self.author = None
                self.since = None
                self.until = None
                self.output = None
                self.verbose = False
        
        # Test basic execution
        print("📊 Testing basic timetrack execution...")
        args = MockArgs()
        result = run_timetrack(args, config)
        print(f"✅ Basic execution result: {result}")
        
        # Test with report flag
        print("\n📝 Testing with report flag...")
        args = MockArgs()
        args.report = True
        result = run_timetrack(args, config)
        print(f"✅ Report execution result: {result}")
        
        # Test with author filter
        print("\n👤 Testing with author filter...")
        args = MockArgs()
        args.author = "gab"
        result = run_timetrack(args, config)
        print(f"✅ Author filter execution result: {result}")
        
        # Test with JSON format
        print("\n📄 Testing JSON format...")
        args = MockArgs()
        args.format = "json"
        args.report = True
        result = run_timetrack(args, config)
        print(f"✅ JSON format execution result: {result}")
        
        # Test with CSV format
        print("\n📊 Testing CSV format...")
        args = MockArgs()
        args.format = "csv"
        args.report = True
        result = run_timetrack(args, config)
        print(f"✅ CSV format execution result: {result}")
        
        # Test with output file
        print("\n💾 Testing output to file...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            args = MockArgs()
            args.output = tmp_path
            args.report = True
            result = run_timetrack(args, config)
            print(f"✅ File output execution result: {result}")
            
            # Check if file was created
            if Path(tmp_path).exists():
                with open(tmp_path, 'r') as f:
                    content = f.read()
                print(f"✅ Output file created with {len(content)} characters")
                print(f"   Preview: {content[:100]}...")
            else:
                print("❌ Output file was not created")
        finally:
            # Clean up
            if Path(tmp_path).exists():
                os.unlink(tmp_path)
        
        # Test HTML format
        print("\n🌐 Testing HTML format...")
        args = MockArgs()
        args.format = "html"
        args.report = True
        result = run_timetrack(args, config)
        print(f"✅ HTML format execution result: {result}")
        
        # Test date filtering
        print("\n📅 Testing date filtering...")
        args = MockArgs()
        args.since = "2025-01-01"
        result = run_timetrack(args, config)
        print(f"✅ Date filter execution result: {result}")
        
        # Test combined filters
        print("\n🔍 Testing combined filters...")
        args = MockArgs()
        args.author = "gabriel"
        args.since = "2024-01-01"
        args.report = True
        args.format = "json"
        result = run_timetrack(args, config)
        print(f"✅ Combined filters execution result: {result}")
        
        # Test error handling
        print("\n🧪 Testing error handling...")
        
        # Test with invalid author (should still work, just return no results)
        args = MockArgs()
        args.author = "nonexistent_author_12345"
        result = run_timetrack(args, config)
        print(f"✅ Invalid author handling result: {result}")
        
        # Test verbose mode
        print("\n🔍 Testing verbose mode...")
        args = MockArgs()
        args.verbose = True
        result = run_timetrack(args, config)
        print(f"✅ Verbose mode execution result: {result}")
        
        print("\n🎉 All TimeTrack command tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ TimeTrack command test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
