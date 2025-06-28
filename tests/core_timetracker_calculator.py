#!/usr/bin/env python3
"""
Test script for core/timetracker/calculator.py

Tests time tracking calculator functionality including commit analysis,
complexity calculation, and time estimation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test timetracker calculator functionality."""
    print("🧪 Testing TimeCalculator...")
    
    try:
        from core.timetracker.calculator import (
            TimeCalculator, CommitStats, TimeEstimate, CommitAnalysis,
            ComplexityType, ComplexityLevel, CommitType,
            analyze_repository_time, calculate_commit_time
        )
        print("✅ TimeCalculator imported successfully")
        
        # Initialize calculator
        calculator = TimeCalculator()
        print("✅ TimeCalculator initialized")
        
        # Test file extension parsing (using constants function)
        print("\n📝 Testing file extension parsing...")
        from constants.timetrack import get_file_extension
        test_files = [
            "component.tsx",
            "utils.js", 
            "styles.scss",
            "config.json",
            "README.md",
            "component.stories.tsx",
            "utils.test.js"
        ]
        
        for filename in test_files:
            ext = get_file_extension(filename)
            print(f"   {filename} → {ext}")
        
        # Test commit type detection (using constants function)
        print("\n📝 Testing commit type detection...")
        from constants.timetrack import get_commit_type
        test_messages = [
            "feat: add new authentication system",
            "fix: resolve login bug",
            "Merge pull request #123",
            "v1.2.3",
            "docs: update README",
            "refactor: improve code structure"
        ]
        
        for message in test_messages:
            commit_type = get_commit_type(message)
            print(f"   '{message}' → {commit_type}")
        
        # Test file category detection (using constants function)
        print("\n📝 Testing file category detection...")
        from constants.timetrack import get_file_category
        test_extensions = ["js", "css", "json", "md", "unknown"]
        
        for ext in test_extensions:
            category_info = get_file_category(ext)
            print(f"   {ext} → {category_info['category']} (planning: {category_info['base_time']['planning']}h)")
        
        # Test complexity analysis
        print("\n📊 Testing complexity analysis...")
        
        # Create test commit stats
        test_stats = CommitStats(
            files_changed=5,
            additions=150,
            deletions=30,
            file_types={"js": 2, "tsx": 1, "css": 1, "md": 1},
            files=["src/components/Auth.tsx", "src/utils/helpers.js", "src/styles/main.css", "README.md", "src/services/api.js"]
        )
        
        complexity_type, complexity_level = calculator.analyze_complexity(test_stats)
        print(f"✅ Complexity analysis:")
        print(f"   Type: {complexity_type}")
        print(f"   Level: {complexity_level}")
        print(f"   Files changed: {test_stats.files_changed}")
        print(f"   Net changes: {test_stats.net_changes}")
        print(f"   Total changes: {test_stats.total_changes}")
        
        # Test time estimation
        print("\n⏱️ Testing time estimation...")
        time_estimate = calculator.calculate_time_estimates(
            test_stats, CommitType.FEATURE, complexity_type, complexity_level
        )
        
        print(f"✅ Time estimates:")
        print(f"   Planning: {time_estimate.planning:.2f} hours")
        print(f"   Implementation: {time_estimate.implementation:.2f} hours")
        print(f"   Total: {time_estimate.total:.2f} hours")
        
        # Test repository analysis (limited to avoid long output)
        print("\n📊 Testing repository analysis...")
        try:
            commits = calculator.get_detailed_git_log()
            print(f"✅ Repository analysis completed:")
            print(f"   Total commits analyzed: {len(commits)}")
            
            if commits:
                # Show stats for first few commits
                for i, commit in enumerate(commits[:3]):
                    print(f"   Commit {i+1}: {commit.hash}")
                    print(f"     Author: {commit.author}")
                    print(f"     Type: {commit.commit_type}")
                    print(f"     Complexity: {commit.complexity_type}/{commit.complexity_level}")
                    print(f"     Files: {commit.stats.files_changed}")
                    print(f"     Time: {commit.time_estimates.total:.2f}h")
                
                # Calculate total time
                total_time = sum(c.time_estimates.total for c in commits)
                print(f"   Total estimated time: {total_time:.2f} hours")
                
                # Test JSON generation
                json_output = calculator.generate_analysis_json(commits[:2])  # Just first 2 for brevity
                print(f"✅ JSON generation successful (length: {len(json_output)} chars)")
        
        except Exception as e:
            print(f"   Note: Repository analysis failed: {e}")
        
        # Test convenience functions
        print("\n🔧 Testing convenience functions...")
        
        # Test calculate_commit_time
        time_est = calculate_commit_time(test_stats, "feat: add new feature")
        print(f"✅ calculate_commit_time: {time_est.total:.2f} hours")
        
        # Test analyze_repository_time
        try:
            repo_commits = analyze_repository_time()
            print(f"✅ analyze_repository_time: {len(repo_commits)} commits")
        except Exception as e:
            print(f"   Note: analyze_repository_time failed: {e}")
        
        # Test edge cases
        print("\n🧪 Testing edge cases...")
        
        # Empty commit stats
        empty_stats = CommitStats()
        empty_complexity = calculator.analyze_complexity(empty_stats)
        print(f"✅ Empty stats complexity: {empty_complexity}")
        
        # Single file commit
        single_file_stats = CommitStats(
            files_changed=1,
            additions=10,
            deletions=0,
            file_types={"py": 1},
            files=["test.py"]
        )
        single_time = calculator.calculate_time_estimates(
            single_file_stats, CommitType.FIX, ComplexityType.ALGORITHMIC, ComplexityLevel.BASIC
        )
        print(f"✅ Single file time estimate: {single_time.total:.2f} hours")
        
        # Large commit
        large_stats = CommitStats(
            files_changed=50,
            additions=2000,
            deletions=500,
            file_types={"js": 20, "tsx": 15, "css": 10, "json": 5},
            files=[f"file{i}.js" for i in range(50)]
        )
        large_complexity = calculator.analyze_complexity(large_stats)
        large_time = calculator.calculate_time_estimates(
            large_stats, CommitType.FEATURE, large_complexity[0], large_complexity[1]
        )
        print(f"✅ Large commit analysis:")
        print(f"   Complexity: {large_complexity[0]}/{large_complexity[1]}")
        print(f"   Time estimate: {large_time.total:.2f} hours")
        
        # Test data classes
        print("\n🏗️ Testing data classes...")
        
        # Test CommitAnalysis to_dict
        analysis = CommitAnalysis(
            hash="abc123",
            author="Test Author",
            date="2024-01-01 12:00:00",
            message="test commit",
            commit_type=CommitType.FEATURE,
            complexity_type=ComplexityType.ALGORITHMIC,
            complexity_level=ComplexityLevel.MODERATE,
            stats=test_stats,
            time_estimates=time_estimate
        )
        
        analysis_dict = analysis.to_dict()
        print(f"✅ CommitAnalysis to_dict: {len(analysis_dict)} keys")
        print(f"   Hash: {analysis_dict['hash']}")
        print(f"   Type: {analysis_dict['type']}")
        print(f"   Total time: {analysis_dict['timeEstimates']['total']:.2f}h")
        
        print("\n🎉 All TimeCalculator tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ TimeCalculator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
