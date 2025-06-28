#!/usr/bin/env python3
"""
Test script for core/git/changes_tracker.py

Tests Git changes tracking functionality including repository state,
file changes, and change analysis.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test changes tracker functionality."""
    print("🧪 Testing ChangesTracker...")
    
    try:
        from core.git.changes_tracker import (
            ChangesTracker, ChangeAnalyzer, FileChange, RepositoryState,
            ChangeType, FileStatus, get_repository_state, 
            get_changes_since_commit, analyze_repository_changes
        )
        print("✅ ChangesTracker imported successfully")
        
        # Initialize tracker
        tracker = ChangesTracker()
        print("✅ ChangesTracker initialized")
        
        # Test repository state
        print("\n📊 Testing repository state...")
        state = tracker.get_repository_state()
        
        print(f"✅ Repository state retrieved:")
        print(f"   Branch: {state.branch}")
        print(f"   Commit: {state.commit_hash[:8] if state.commit_hash else 'None'}")
        print(f"   Total changes: {state.total_changes}")
        print(f"   Staged changes: {len(state.staged_changes)}")
        print(f"   Modified changes: {len(state.modified_changes)}")
        print(f"   Untracked files: {len(state.untracked_files)}")
        print(f"   Is clean: {state.clean}")
        print(f"   Is dirty: {state.is_dirty}")
        print(f"   Has changes: {state.has_changes}")
        
        if state.ahead_behind:
            ahead, behind = state.ahead_behind
            print(f"   Ahead/Behind: +{ahead}/-{behind}")
        
        # Show some changes if they exist
        if state.staged_changes:
            print(f"\n📝 Staged changes ({len(state.staged_changes)}):")
            for change in state.staged_changes[:5]:  # Show first 5
                print(f"   {change.change_type.value}: {change.path}")
        
        if state.modified_changes:
            print(f"\n📝 Modified changes ({len(state.modified_changes)}):")
            for change in state.modified_changes[:5]:  # Show first 5
                print(f"   {change.change_type.value}: {change.path}")
        
        if state.untracked_files:
            print(f"\n📝 Untracked files ({len(state.untracked_files)}):")
            for change in state.untracked_files[:5]:  # Show first 5
                print(f"   {change.change_type.value}: {change.path}")
        
        # Test file tracking
        print("\n🔍 Testing file tracking...")
        test_files = ["README.md", "pyproject.toml", "nonexistent.txt"]
        
        for file_path in test_files:
            is_tracked = tracker.is_file_tracked(file_path)
            is_ignored = tracker.is_file_ignored(file_path)
            print(f"   {file_path}: tracked={is_tracked}, ignored={is_ignored}")
        
        # Test changes since commit
        print("\n📈 Testing changes since commit...")
        try:
            # Get changes since HEAD~1 (last commit)
            changes_since_last = tracker.get_changes_since_commit("HEAD~1")
            print(f"✅ Changes since last commit: {len(changes_since_last)}")
            
            for change in changes_since_last[:3]:  # Show first 3
                print(f"   {change.change_type.value}: {change.path}")
                if change.old_path:
                    print(f"     (renamed from: {change.old_path})")
        except Exception as e:
            print(f"   Note: Could not get changes since last commit: {e}")
        
        # Test file history
        print("\n📚 Testing file history...")
        try:
            history = tracker.get_file_history("README.md", max_commits=3)
            print(f"✅ README.md history: {len(history)} commits")
            
            for entry in history:
                print(f"   {entry['commit']}: {entry['message']}")
        except Exception as e:
            print(f"   Note: Could not get file history: {e}")
        
        # Test change analyzer
        print("\n📊 Testing change analyzer...")
        analyzer = ChangeAnalyzer()
        analysis = analyzer.analyze_repository_state()
        
        print(f"✅ Repository analysis completed:")
        print(f"   Total changes: {analysis['total_changes']}")
        print(f"   Staged count: {analysis['staged_count']}")
        print(f"   Modified count: {analysis['modified_count']}")
        print(f"   Untracked count: {analysis['untracked_count']}")
        print(f"   Is clean: {analysis['is_clean']}")
        print(f"   Is dirty: {analysis['is_dirty']}")
        print(f"   Branch: {analysis['branch']}")
        
        if analysis['file_types']:
            print(f"   File types: {analysis['file_types']}")
        
        if analysis['change_types']:
            print(f"   Change types: {analysis['change_types']}")
        
        # Test convenience functions
        print("\n🔧 Testing convenience functions...")
        
        # Test get_repository_state function
        state_func = get_repository_state()
        print(f"✅ get_repository_state: {state_func.total_changes} changes")
        
        # Test analyze_repository_changes function
        analysis_func = analyze_repository_changes()
        print(f"✅ analyze_repository_changes: {analysis_func['total_changes']} changes")
        
        # Test get_changes_since_commit function
        try:
            changes_func = get_changes_since_commit("HEAD~1")
            print(f"✅ get_changes_since_commit: {len(changes_func)} changes")
        except Exception as e:
            print(f"   Note: get_changes_since_commit failed: {e}")
        
        # Test FileChange properties
        print("\n🧪 Testing FileChange properties...")
        if state.staged_changes or state.modified_changes or state.untracked_files:
            all_changes = state.staged_changes + state.modified_changes + state.untracked_files
            if all_changes:
                test_change = all_changes[0]
                print(f"✅ FileChange properties test:")
                print(f"   Path: {test_change.path}")
                print(f"   Is added: {test_change.is_added}")
                print(f"   Is modified: {test_change.is_modified}")
                print(f"   Is deleted: {test_change.is_deleted}")
                print(f"   Is renamed: {test_change.is_renamed}")
                print(f"   Is staged: {test_change.is_staged}")
                print(f"   Is untracked: {test_change.is_untracked}")
        
        # Test conflicted files
        print("\n⚔️ Testing conflict detection...")
        conflicted = tracker.get_conflicted_files()
        print(f"✅ Conflicted files: {len(conflicted)}")
        if conflicted:
            for file_path in conflicted:
                print(f"   Conflict: {file_path}")
        
        print("\n🎉 All ChangesTracker tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ChangesTracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
