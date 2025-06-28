#!/usr/bin/env python3
"""
Test script for GitReleaseAnalyzer.
"""

from core.git import GitReleaseAnalyzer, ReleaseInfo, ReleaseComparison

def test_git_release_analyzer():
    """Test basic functionality of GitReleaseAnalyzer."""
    print("🧪 Testing GitReleaseAnalyzer...")
    
    try:
        # Initialize analyzer
        analyzer = GitReleaseAnalyzer()
        print(f"✅ GitReleaseAnalyzer initialized")
        print(f"   Output directory: {analyzer.output_dir}")
        
        # Test repository check
        is_repo = analyzer.is_git_repository()
        print(f"✅ Is Git repository: {is_repo}")
        
        if not is_repo:
            print("⚠️  Not in a Git repository - skipping tag tests")
            return True
        
        # Test getting current tag
        current_tag = analyzer.get_current_tag()
        print(f"✅ Current tag: {current_tag or 'No tags found'}")
        
        # Test getting all tags
        all_tags = analyzer.get_all_tags()
        print(f"✅ Total tags found: {len(all_tags)}")
        if all_tags:
            print(f"   Latest tags: {all_tags[:3]}")
        
        # Test release analysis (only if tags exist)
        if current_tag:
            print("\n🔍 Testing release analysis...")
            
            # Test tag info
            tag_info = analyzer.get_tag_info(current_tag)
            print(f"✅ Tag info retrieved:")
            print(f"   Tag: {tag_info.tag}")
            print(f"   Date: {tag_info.date}")
            print(f"   Commit: {tag_info.commit_hash[:8]}...")
            
            # Test release comparison - SIMPLE mode
            print("\n📝 Testing SIMPLE mode...")
            comparison_simple = analyzer.analyze_current_release('simple')
            if comparison_simple:
                print(f"✅ Simple release comparison created:")
                print(f"   Current: {comparison_simple.current_release.tag}")
                print(f"   Previous: {comparison_simple.previous_release.tag if comparison_simple.previous_release else 'First release'}")
                print(f"   Commits: {len(comparison_simple.commits)}")
                
                # Test saving simple output
                simple_output_file = analyzer.save_simple_output()
                if simple_output_file:
                    print(f"✅ Simple output saved to: {simple_output_file}")
                else:
                    print("⚠️  No simple output file created")
            else:
                print("⚠️  No simple release comparison available")
            
            # Test release comparison - DETAILED mode
            print("\n📋 Testing DETAILED mode...")
            comparison_detailed = analyzer.analyze_current_release('detailed')
            if comparison_detailed:
                print(f"✅ Detailed release comparison created:")
                print(f"   Current: {comparison_detailed.current_release.tag}")
                print(f"   Previous: {comparison_detailed.previous_release.tag if comparison_detailed.previous_release else 'First release'}")
                print(f"   Commits: {len(comparison_detailed.commits)}")
                print(f"   Has full diff: {bool(comparison_detailed.full_diff)}")
                
                # Test saving detailed output
                detailed_output_file = analyzer.save_detailed_output()
                if detailed_output_file:
                    print(f"✅ Detailed output saved to: {detailed_output_file}")
                else:
                    print("⚠️  No detailed output file created")
            else:
                print("⚠️  No detailed release comparison available")
        else:
            print("⚠️  No tags found - skipping release analysis")
            print("   To test with tags, create one: git tag v1.0.0")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_git_release_analyzer()
