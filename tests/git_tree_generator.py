#!/usr/bin/env python3
"""
Quick test script for GitTreeGenerator.
"""

from core.git import GitTreeGenerator, TreeGenerationResult

def test_tree_generator():
    """Test basic functionality of GitTreeGenerator."""
    print("🧪 Testing GitTreeGenerator...")
    
    try:
        # Initialize generator
        generator = GitTreeGenerator()
        print(f"✅ GitTreeGenerator initialized")
        print(f"   Output directory: {generator.output_dir}")
        
        # Test project tree generation
        print("\n📁 Testing project tree generation...")
        project_result = generator.generate_project_tree()
        print(f"✅ Project tree generated:")
        print(f"   Success: {project_result.success}")
        print(f"   File count: {project_result.file_count}")
        if project_result.success:
            print(f"   Output file: {project_result.output_file}")
        else:
            print(f"   Error: {project_result.error_message}")
        
        # Test Git changes trees
        print("\n🔄 Testing Git changes trees...")
        git_results = generator.generate_git_changes_trees()
        print(f"✅ Git changes trees generated:")
        print(f"   Total results: {len(git_results)}")
        for result in git_results:
            print(f"   - {result.tree_type}: {result.success} ({result.file_count} files)")
            if result.error_message:
                print(f"     Error: {result.error_message}")
        
        # Test release changes trees
        print("\n🏷️ Testing release changes trees...")
        release_results = generator.generate_release_changes_trees()
        print(f"✅ Release changes trees generated:")
        print(f"   Total results: {len(release_results)}")
        for result in release_results:
            print(f"   - {result.tree_type}: {result.success} ({result.file_count} files)")
            if result.error_message:
                print(f"     Error: {result.error_message}")
        
        # Test siblings tree (if prerequisites exist)
        print("\n👥 Testing siblings tree...")
        siblings_result = generator.generate_siblings_tree()
        print(f"✅ Siblings tree generated:")
        print(f"   Success: {siblings_result.success}")
        print(f"   File count: {siblings_result.file_count}")
        if siblings_result.success:
            print(f"   Output file: {siblings_result.output_file}")
        else:
            print(f"   Error: {siblings_result.error_message}")
        
        # Test generate all trees
        print("\n🌳 Testing generate all trees...")
        all_results = generator.generate_all_trees()
        print(f"✅ All trees generated:")
        print(f"   Total results: {len(all_results)}")
        
        # Generate summary
        summary = generator.get_generation_summary(all_results)
        print(f"\n📊 Generation Summary:")
        print(f"   Total trees: {summary['total_trees']}")
        print(f"   Successful: {summary['successful']}")
        print(f"   Failed: {summary['failed']}")
        print(f"   Total files: {summary['total_files']}")
        print(f"   Output directory: {summary['output_directory']}")
        
        if summary['generated_files']:
            print(f"   Generated files:")
            for tree_type, filepath in summary['generated_files'].items():
                print(f"     - {tree_type}: {filepath}")
        
        if summary['errors']:
            print(f"   Errors:")
            for tree_type, error in summary['errors'].items():
                print(f"     - {tree_type}: {error}")
        
        print("\n🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_tree_generator()
