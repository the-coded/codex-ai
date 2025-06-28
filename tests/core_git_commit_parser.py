#!/usr/bin/env python3
"""
Test script for core/git/commit_parser.py

Tests commit parsing functionality including conventional commits,
commit analysis, and pattern recognition.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test commit parser functionality."""
    print("🧪 Testing CommitParser...")
    
    try:
        from core.git.commit_parser import (
            CommitParser, CommitAnalyzer, ParsedCommit, CommitType,
            parse_commit, parse_commits, analyze_commit_patterns
        )
        print("✅ CommitParser imported successfully")
        
        # Initialize parser
        parser = CommitParser()
        print("✅ CommitParser initialized")
        
        # Test conventional commit parsing
        print("\n📝 Testing conventional commit parsing...")
        conventional_commit = "feat(auth): add user authentication system\n\nImplement JWT-based authentication with refresh tokens.\n\nBREAKING CHANGE: API endpoints now require authentication\nCloses #123"
        
        parsed = parser.parse(conventional_commit)
        print(f"✅ Conventional commit parsed:")
        print(f"   Type: {parsed.type.value}")
        print(f"   Scope: {parsed.scope}")
        print(f"   Description: {parsed.description}")
        print(f"   Breaking change: {parsed.breaking_change}")
        print(f"   Is conventional: {parsed.is_conventional}")
        print(f"   Issues: {parsed.issues}")
        
        # Test non-conventional commit
        print("\n📝 Testing non-conventional commit...")
        regular_commit = "Fix bug in user login functionality"
        parsed_regular = parser.parse(regular_commit)
        print(f"✅ Regular commit parsed:")
        print(f"   Type: {parsed_regular.type.value}")
        print(f"   Is conventional: {parsed_regular.is_conventional}")
        print(f"   Description: {parsed_regular.description}")
        
        # Test multiple commits
        print("\n📝 Testing multiple commits...")
        sample_commits = [
            "feat: add new feature",
            "fix: resolve authentication bug",
            "docs: update README documentation", 
            "refactor(core): improve code structure",
            "test: add unit tests for parser",
            "chore: update dependencies",
            "BREAKING CHANGE: remove deprecated API"
        ]
        
        parsed_commits = parser.parse_multiple(sample_commits)
        print(f"✅ Parsed {len(parsed_commits)} commits")
        
        # Test commit analysis
        print("\n📊 Testing commit analysis...")
        analyzer = CommitAnalyzer()
        analysis = analyzer.analyze_commits(sample_commits)
        
        print(f"✅ Commit analysis completed:")
        print(f"   Total commits: {analysis['total_commits']}")
        print(f"   Conventional commits: {analysis['conventional_commits']}")
        print(f"   Conventional percentage: {analysis['conventional_percentage']:.1f}%")
        print(f"   Features: {analysis['features']}")
        print(f"   Bugfixes: {analysis['bugfixes']}")
        print(f"   Documentation: {analysis['documentation']}")
        print(f"   Breaking changes: {analysis['breaking_changes']}")
        print(f"   Type distribution: {analysis['type_distribution']}")
        
        # Test convenience functions
        print("\n🔧 Testing convenience functions...")
        single_parsed = parse_commit("feat: test convenience function")
        print(f"✅ parse_commit: {single_parsed.type.value}")
        
        multiple_parsed = parse_commits(["feat: test1", "fix: test2"])
        print(f"✅ parse_commits: {len(multiple_parsed)} commits")
        
        pattern_analysis = analyze_commit_patterns(sample_commits)
        print(f"✅ analyze_commit_patterns: {pattern_analysis['total_commits']} commits analyzed")
        
        # Test edge cases
        print("\n🧪 Testing edge cases...")
        
        # Empty commit
        empty_parsed = parser.parse("")
        print(f"✅ Empty commit handled: {empty_parsed.description}")
        
        # Commit with co-authors
        co_author_commit = "feat: collaborative feature\n\nCo-authored-by: John Doe <john@example.com>\nCo-authored-by: Jane Smith <jane@example.com>"
        co_author_parsed = parser.parse(co_author_commit)
        print(f"✅ Co-authors parsed: {len(co_author_parsed.co_authors)} co-authors")
        
        # Commit with multiple issues
        issue_commit = "fix: resolve multiple issues\n\nFixes #123\nCloses #456\nResolves user/repo#789"
        issue_parsed = parser.parse(issue_commit)
        print(f"✅ Issues parsed: {len(issue_parsed.issues)} issues")
        
        print("\n🎉 All CommitParser tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ CommitParser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
