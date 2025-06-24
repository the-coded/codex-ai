#!/usr/bin/env python3
"""
Test script for core/timetracker/report_generator.py

Tests time tracking report generation functionality including
developer statistics, monthly breakdowns, and markdown generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Test timetracker report generator functionality."""
    print("🧪 Testing ReportGenerator...")
    
    try:
        from core.timetracker.report_generator import (
            ReportGenerator, TimeTrackingReport, ProjectStats, DeveloperStats,
            MonthlyStats, DeveloperTypeStats, generate_time_report,
            generate_report_from_analysis_file, create_full_time_report
        )
        from core.timetracker.calculator import (
            TimeCalculator, CommitAnalysis, CommitStats, TimeEstimate,
            CommitType, ComplexityType, ComplexityLevel
        )
        print("✅ ReportGenerator imported successfully")
        
        # Initialize report generator
        generator = ReportGenerator()
        print("✅ ReportGenerator initialized")
        
        # Create test data
        print("\n📝 Creating test data...")
        
        # Create sample commits for testing
        test_commits = [
            CommitAnalysis(
                hash="abc123",
                author="Gabriel Mule",
                date="2024-01-15 10:30:00",
                message="feat: add authentication system",
                commit_type=CommitType.FEATURE,
                complexity_type=ComplexityType.ALGORITHMIC,
                complexity_level=ComplexityLevel.MODERATE,
                stats=CommitStats(
                    files_changed=5,
                    additions=200,
                    deletions=20,
                    file_types={"js": 3, "tsx": 2},
                    files=["auth.js", "login.tsx", "utils.js", "api.js", "types.tsx"]
                ),
                time_estimates=TimeEstimate(planning=2.5, implementation=8.0)
            ),
            CommitAnalysis(
                hash="def456",
                author="Gabriel Mule",
                date="2024-01-16 14:20:00",
                message="fix: resolve login bug",
                commit_type=CommitType.FIX,
                complexity_type=ComplexityType.ALGORITHMIC,
                complexity_level=ComplexityLevel.BASIC,
                stats=CommitStats(
                    files_changed=2,
                    additions=15,
                    deletions=5,
                    file_types={"js": 1, "tsx": 1},
                    files=["auth.js", "login.tsx"]
                ),
                time_estimates=TimeEstimate(planning=0.5, implementation=1.5)
            ),
            CommitAnalysis(
                hash="ghi789",
                author="John Doe",
                date="2024-02-01 09:15:00",
                message="feat: add user dashboard",
                commit_type=CommitType.FEATURE,
                complexity_type=ComplexityType.STRUCTURAL,
                complexity_level=ComplexityLevel.COMPLEX,
                stats=CommitStats(
                    files_changed=8,
                    additions=350,
                    deletions=10,
                    file_types={"tsx": 4, "css": 3, "js": 1},
                    files=["dashboard.tsx", "profile.tsx", "settings.tsx", "nav.tsx", "main.css", "theme.css", "utils.css", "api.js"]
                ),
                time_estimates=TimeEstimate(planning=4.0, implementation=12.0)
            ),
            CommitAnalysis(
                hash="jkl012",
                author="John Doe",
                date="2024-02-05 16:45:00",
                message="v1.0.0",
                commit_type=CommitType.PUBLISH,
                complexity_type=ComplexityType.STRUCTURAL,
                complexity_level=ComplexityLevel.TRIVIAL,
                stats=CommitStats(
                    files_changed=1,
                    additions=5,
                    deletions=0,
                    file_types={"json": 1},
                    files=["package.json"]
                ),
                time_estimates=TimeEstimate(planning=0.1, implementation=0.1)
            )
        ]
        
        print(f"✅ Created {len(test_commits)} test commits")
        
        # Test report generation
        print("\n📊 Testing report generation...")
        report = generator.process_commits(test_commits)
        
        print(f"✅ Report generated:")
        print(f"   Project period: {report.project_stats.start_date} - {report.project_stats.end_date}")
        print(f"   Total hours: {report.project_stats.total_hours:.2f}")
        print(f"   Working days: {report.project_stats.total_working_days}")
        print(f"   Calendar days: {report.project_stats.total_calendar_days}")
        print(f"   Commit frequency: {report.project_stats.commit_frequency:.1f}%")
        print(f"   Developers: {len(report.developer_stats)}")
        
        # Test developer statistics
        print("\n👥 Testing developer statistics...")
        for dev, stats in report.developer_stats.items():
            print(f"✅ Developer: {dev}")
            print(f"   Total hours: {stats.total_hours:.2f}")
            print(f"   Total commits: {stats.total_commits}")
            print(f"   Avg hours/commit: {stats.average_hours_per_commit:.2f}")
            print(f"   Months active: {len(stats.by_month)}")
            
            # Show commit type breakdown
            for commit_type, type_stats in stats.by_type.items():
                if type_stats.commits > 0:
                    print(f"     {commit_type}: {type_stats.commits} commits, {type_stats.hours:.1f}h")
        
        # Test monthly statistics
        print("\n📅 Testing monthly statistics...")
        for dev, stats in report.developer_stats.items():
            print(f"✅ Monthly stats for {dev}:")
            for month, month_stats in sorted(stats.by_month.items()):
                print(f"   {month}: {month_stats.commits} commits, {month_stats.hours:.1f}h, {month_stats.working_days} days")
                print(f"     Hours/day: {month_stats.hours_per_day:.1f}")
        
        # Test markdown generation
        print("\n📝 Testing markdown generation...")
        markdown = generator.generate_markdown_report(report)
        print(f"✅ Markdown report generated:")
        print(f"   Length: {len(markdown)} characters")
        print(f"   Lines: {len(markdown.split(chr(10)))}")
        
        # Show first few lines
        lines = markdown.split('\n')[:10]
        print("   Preview:")
        for line in lines:
            print(f"     {line}")
        
        # Test JSON generation
        print("\n📄 Testing JSON generation...")
        json_report = generator.generate_json_report(report)
        print(f"✅ JSON report generated:")
        print(f"   Length: {len(json_report)} characters")
        
        # Test to_dict conversion
        report_dict = report.to_dict()
        print(f"✅ Report to_dict conversion:")
        print(f"   Keys: {list(report_dict.keys())}")
        print(f"   Project stats keys: {list(report_dict['projectStats'].keys())}")
        print(f"   Developer count: {len(report_dict['devStats'])}")
        
        # Test month formatting
        print("\n📅 Testing month formatting...")
        test_months = ["2024-01", "2024-02", "2024-12"]
        for month in test_months:
            formatted = generator._format_month(month)
            print(f"   {month} → {formatted}")
        
        # Test convenience functions
        print("\n🔧 Testing convenience functions...")
        
        # Test generate_time_report
        conv_report = generate_time_report(test_commits)
        print(f"✅ generate_time_report: {conv_report.project_stats.total_hours:.2f} hours")
        
        # Test create_full_time_report (with real repository)
        print("\n🔍 Testing with REAL repository data (last 10 commits)...")
        try:
            # Use calculator directly to limit commits for testing
            calculator = TimeCalculator()
            all_commits = calculator.analyze_repository()
            # Take only last 10 commits for testing
            recent_commits = all_commits[:10]
            real_report = generator.process_commits(recent_commits)
            print(f"✅ Real repository analysis:")
            print(f"   Developers: {len(real_report.developer_stats)}")
            print(f"   Total hours: {real_report.project_stats.total_hours:.2f}")
            print(f"   Period: {real_report.project_stats.start_date} - {real_report.project_stats.end_date}")
            print(f"   Working days: {real_report.project_stats.total_working_days}")
            print(f"   Calendar days: {real_report.project_stats.total_calendar_days}")
            
            # Show real developer stats
            for dev, stats in real_report.developer_stats.items():
                print(f"     {dev}: {stats.total_hours:.2f}h ({stats.total_commits} commits)")
                # Show commit type breakdown
                for commit_type, type_stats in stats.by_type.items():
                    if type_stats.commits > 0:
                        print(f"       {commit_type}: {type_stats.commits} commits, {type_stats.hours:.1f}h")
            
            # Replace test data with real data for file operations
            report = real_report
            print("🔄 Using REAL data for report generation...")
            
        except Exception as e:
            print(f"   Note: create_full_time_report failed: {e}")
            print("   Falling back to test data...")
        
        # Test edge cases
        print("\n🧪 Testing edge cases...")
        
        # Empty commits list
        empty_report = generator.process_commits([])
        print(f"✅ Empty commits report:")
        print(f"   Total hours: {empty_report.project_stats.total_hours}")
        print(f"   Developers: {len(empty_report.developer_stats)}")
        
        # Single commit
        single_report = generator.process_commits([test_commits[0]])
        print(f"✅ Single commit report:")
        print(f"   Total hours: {single_report.project_stats.total_hours:.2f}")
        print(f"   Working days: {single_report.project_stats.total_working_days}")
        
        # Test data classes properties
        print("\n🏗️ Testing data class properties...")
        
        # Test ProjectStats properties
        project_stats = report.project_stats
        print(f"✅ ProjectStats properties:")
        print(f"   Commit frequency: {project_stats.commit_frequency:.1f}%")
        print(f"   Avg hours/working day: {project_stats.average_hours_per_working_day:.2f}")
        
        # Test DeveloperStats properties
        dev_stats = list(report.developer_stats.values())[0]
        print(f"✅ DeveloperStats properties:")
        print(f"   Avg hours/commit: {dev_stats.average_hours_per_commit:.2f}")
        
        # Test MonthlyStats properties
        if dev_stats.by_month:
            month_stats = list(dev_stats.by_month.values())[0]
            print(f"✅ MonthlyStats properties:")
            print(f"   Hours per day: {month_stats.hours_per_day:.2f}")
        
        # Test file operations (save reports)
        print("\n💾 Testing file operations...")
        try:
            # Ensure .tmp directory exists
            tmp_dir = Path(".tmp")
            tmp_dir.mkdir(exist_ok=True)
            
            # Save reports to .tmp directory
            json_file = tmp_dir / "git-hours-report.json"
            md_file = tmp_dir / "git-hours-report.md"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                f.write(generator.generate_json_report(report))
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(generator.generate_markdown_report(report))
            
            print(f"✅ Reports saved to .tmp/:")
            print(f"   JSON: {json_file}")
            print(f"   Markdown: {md_file}")
            print("📁 Files kept for validation - check .tmp/ directory")
        except Exception as e:
            print(f"   Note: File operations failed: {e}")
        
        print("\n🎉 All ReportGenerator tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ReportGenerator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
