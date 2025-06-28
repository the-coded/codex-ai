#!/usr/bin/env python3
"""
Quick test script for GitLogAnalyzer.
"""

from core.git import GitLogAnalyzer, CommitInfo

def test_git_analyzer():
    """Test basic functionality of GitLogAnalyzer."""
    print("🧪 Testing GitLogAnalyzer...")
    
    try:
        # Initialize analyzer
        analyzer = GitLogAnalyzer()
        print(f"✅ GitLogAnalyzer initialized")
        print(f"   Output directory: {analyzer.output_dir}")
        
        # Test getting last commit hash
        last_commit = analyzer.get_last_commit_hash()
        print(f"✅ Last commit hash: {last_commit[:8]}...")
        
        # Test merge commit detection
        is_merge = analyzer.is_merge_commit(last_commit)
        print(f"✅ Is merge commit: {is_merge}")
        
        # Test commit analysis - SIMPLE mode
        print("\n📝 Testing SIMPLE mode...")
        commit_info_simple = analyzer.analyze_last_commit('simple')
        print(f"✅ Simple commit analyzed:")
        print(f"   Author: {commit_info_simple.author}")
        print(f"   Message: {commit_info_simple.message}")
        print(f"   Files changed: {len(commit_info_simple.files_changed)}")
        
        # Test saving simple output
        simple_output_file = analyzer.save_simple_output()
        print(f"✅ Simple output saved to: {simple_output_file}")
        
        # Test commit analysis - DETAILED mode
        print("\n📋 Testing DETAILED mode...")
        commit_info_detailed = analyzer.analyze_last_commit('detailed')
        print(f"✅ Detailed commit analyzed:")
        print(f"   Author: {commit_info_detailed.author}")
        print(f"   Message: {commit_info_detailed.message}")
        print(f"   Has patch: {bool(commit_info_detailed.patch)}")
        
        # Test saving detailed output
        detailed_output_file = analyzer.save_detailed_output()
        print(f"✅ Detailed output saved to: {detailed_output_file}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_git_analyzer()
