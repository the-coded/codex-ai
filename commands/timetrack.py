"""
Timetrack command implementation for Codex-AI.

Provides CLI interface for time tracking analysis using Git commits.
Integrates with core.timetracker module to generate comprehensive reports.
"""

import sys
import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from core.timetracker import (
    TimeCalculator, ReportGenerator, create_full_time_report,
    TIMETRACKER_AVAILABLE
)
from core.config import CodexConfig


def run_timetrack(args, config: CodexConfig) -> int:
    """
    Run timetrack analysis command.
    
    Args:
        args: Parsed command line arguments
        config: Codex configuration object
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not TIMETRACKER_AVAILABLE:
        print("❌ Error: Timetracker module not available")
        print("   Please check your installation")
        return 1
    
    try:
        print("📊 Analyzing Git commits for time tracking...")
        
        # Initialize components
        calculator = TimeCalculator()
        generator = ReportGenerator()
        
        # Get commits based on filters
        commits = _get_filtered_commits(calculator, args)
        
        if not commits:
            print("⚠️  No commits found matching the specified criteria")
            return 0
        
        print(f"✅ Found {len(commits)} commits to analyze")
        
        # Generate report
        report = generator.process_commits(commits)
        
        # Display basic stats
        _display_basic_stats(report, args)
        
        # Generate detailed report if requested
        if args.report:
            _generate_detailed_report(generator, report, args, config)
        
        # Save to file if output specified
        if args.output:
            _save_report_to_file(generator, report, args, config)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error running timetrack analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def _parse_since_parameter(since_value: str) -> Dict[str, str]:
    """
    Parse --since parameter to detect type: date, commit hash, or tag.
    
    Args:
        since_value: Value from --since parameter
        
    Returns:
        Dictionary with 'type' and 'value' keys
    """
    # Check if it looks like a commit hash (6-40 hex characters)
    if re.match(r'^[a-f0-9]{6,40}$', since_value, re.IGNORECASE):
        return {'type': 'commit', 'value': since_value}
    
    # Check if it looks like a version tag (v1.0.0, 1.0.0, etc.)
    if re.match(r'^v?\d+\.\d+(\.\d+)?', since_value):
        return {'type': 'tag', 'value': since_value}
    
    # Check if it looks like a date (YYYY-MM-DD)
    if re.match(r'^\d{4}-\d{2}-\d{2}', since_value):
        return {'type': 'date', 'value': since_value}
    
    # Default to date for backward compatibility
    return {'type': 'date', 'value': since_value}


def _filter_commits_since_hash(commits: List, target_hash: str) -> List:
    """
    Filter commits starting from a specific commit hash.
    
    Args:
        commits: List of commits (newest first)
        target_hash: Target commit hash to start from
        
    Returns:
        List of commits since the target hash (including target)
    """
    # Find the target commit index
    target_index = None
    for i, commit in enumerate(commits):
        if commit.hash.startswith(target_hash) or target_hash.startswith(commit.hash):
            target_index = i
            break
    
    if target_index is None:
        print(f"⚠️  Commit hash '{target_hash}' not found")
        return []
    
    # Return commits from target onwards (commits are newest first)
    return commits[:target_index + 1]


def _filter_commits_since_tag(commits: List, tag: str) -> List:
    """
    Filter commits since a Git tag.
    
    Args:
        commits: List of commits
        tag: Git tag name
        
    Returns:
        List of commits since the tag
    """
    try:
        # Get commit hash for the tag
        result = subprocess.run([
            'git', 'rev-list', '-n', '1', tag
        ], capture_output=True, text=True, check=True)
        
        tag_hash = result.stdout.strip()
        if tag_hash:
            return _filter_commits_since_hash(commits, tag_hash)
        
    except subprocess.CalledProcessError:
        print(f"⚠️  Tag '{tag}' not found")
    
    return []


def _filter_commits_until_hash(commits: List, target_hash: str) -> List:
    """
    Filter commits up to a specific commit hash.
    
    Args:
        commits: List of commits (newest first)
        target_hash: Target commit hash to stop at
        
    Returns:
        List of commits until the target hash (excluding target)
    """
    # Find the target commit index
    target_index = None
    for i, commit in enumerate(commits):
        if commit.hash.startswith(target_hash) or target_hash.startswith(commit.hash):
            target_index = i
            break
    
    if target_index is None:
        print(f"⚠️  Commit hash '{target_hash}' not found")
        return commits  # Return all if not found
    
    # Return commits before target (commits are newest first)
    return commits[target_index + 1:]


def _filter_commits_until_tag(commits: List, tag: str) -> List:
    """
    Filter commits until a Git tag.
    
    Args:
        commits: List of commits
        tag: Git tag name
        
    Returns:
        List of commits until the tag
    """
    try:
        # Get commit hash for the tag
        result = subprocess.run([
            'git', 'rev-list', '-n', '1', tag
        ], capture_output=True, text=True, check=True)
        
        tag_hash = result.stdout.strip()
        if tag_hash:
            return _filter_commits_until_hash(commits, tag_hash)
        
    except subprocess.CalledProcessError:
        print(f"⚠️  Tag '{tag}' not found")
    
    return commits  # Return all if tag not found


def _get_filtered_commits(calculator: TimeCalculator, args) -> List:
    """
    Get commits filtered by command line arguments.
    
    Args:
        calculator: TimeCalculator instance
        args: Command line arguments
        
    Returns:
        List of filtered commits
    """
    # Get all commits
    all_commits = calculator.analyze_repository()
    
    # Apply filters
    filtered_commits = all_commits
    
    # Filter by author
    if args.author:
        author_lower = args.author.lower()
        filtered_commits = [
            c for c in filtered_commits 
            if author_lower in c.author.lower()
        ]
    
    # Filter by since parameter (supports dates, hashes, and tags)
    if args.since:
        since_info = _parse_since_parameter(args.since)
        
        if since_info['type'] == 'commit':
            print(f"📍 Filtering commits since hash: {since_info['value']}")
            filtered_commits = _filter_commits_since_hash(filtered_commits, since_info['value'])
        
        elif since_info['type'] == 'tag':
            print(f"🏷️  Filtering commits since tag: {since_info['value']}")
            filtered_commits = _filter_commits_since_tag(filtered_commits, since_info['value'])
        
        else:  # date
            print(f"📅 Filtering commits since date: {since_info['value']}")
            filtered_commits = [
                c for c in filtered_commits 
                if c.date >= since_info['value']
            ]
    
    # Filter by until parameter (supports dates, hashes, and tags)
    if args.until:
        until_info = _parse_since_parameter(args.until)
        
        if until_info['type'] == 'commit':
            print(f"📍 Filtering commits until hash: {until_info['value']}")
            filtered_commits = _filter_commits_until_hash(filtered_commits, until_info['value'])
        
        elif until_info['type'] == 'tag':
            print(f"🏷️  Filtering commits until tag: {until_info['value']}")
            filtered_commits = _filter_commits_until_tag(filtered_commits, until_info['value'])
        
        else:  # date
            print(f"📅 Filtering commits until date: {until_info['value']}")
            filtered_commits = [
                c for c in filtered_commits 
                if c.date <= until_info['value']
            ]
    
    return filtered_commits


def _display_basic_stats(report, args):
    """
    Display basic statistics to console.
    
    Args:
        report: TimeTrackingReport object
        args: Command line arguments
    """
    print(f"\n📈 Time Tracking Summary:")
    print(f"   Period: {report.project_stats.start_date} - {report.project_stats.end_date}")
    print(f"   Total Hours: {report.project_stats.total_hours:.2f}")
    print(f"   Working Days: {report.project_stats.total_working_days}")
    print(f"   Developers: {len(report.developer_stats)}")
    
    # Show developer breakdown
    for dev, stats in report.developer_stats.items():
        print(f"     {dev}: {stats.total_hours:.2f}h ({stats.total_commits} commits)")


def _generate_detailed_report(generator: ReportGenerator, report, args, config: CodexConfig):
    """
    Generate and display detailed report.
    
    Args:
        generator: ReportGenerator instance
        report: TimeTrackingReport object
        args: Command line arguments
        config: Codex configuration
    """
    print(f"\n📝 Generating detailed report...")
    
    # Generate based on format
    if args.format == 'json':
        output = generator.generate_json_report(report)
        print(output)
    elif args.format == 'markdown':
        output = generator.generate_markdown_report(report)
        print(output)
    elif args.format == 'csv':
        output = _generate_csv_report(report)
        print(output)
    elif args.format == 'html':
        output = _generate_html_report(generator, report)
        print(output)
    else:
        # Default to markdown
        output = generator.generate_markdown_report(report)
        print(output)


def _save_report_to_file(generator: ReportGenerator, report, args, config: CodexConfig):
    """
    Save report to specified output file.
    
    Args:
        generator: ReportGenerator instance
        report: TimeTrackingReport object
        args: Command line arguments
        config: Codex configuration
    """
    output_path = Path(args.output)
    
    try:
        # Determine format from file extension if not specified
        format_type = args.format
        if not format_type:
            suffix = output_path.suffix.lower()
            if suffix == '.json':
                format_type = 'json'
            elif suffix == '.md':
                format_type = 'markdown'
            elif suffix == '.csv':
                format_type = 'csv'
            elif suffix == '.html':
                format_type = 'html'
            else:
                format_type = 'markdown'  # Default
        
        # Generate content
        if format_type == 'json':
            content = generator.generate_json_report(report)
        elif format_type == 'markdown':
            content = generator.generate_markdown_report(report)
        elif format_type == 'csv':
            content = _generate_csv_report(report)
        elif format_type == 'html':
            content = _generate_html_report(generator, report)
        else:
            content = generator.generate_markdown_report(report)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Report saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error saving report to {output_path}: {e}")


def _generate_csv_report(report) -> str:
    """
    Generate CSV format report.
    
    Args:
        report: TimeTrackingReport object
        
    Returns:
        CSV formatted string
    """
    lines = []
    
    # Header
    lines.append("Developer,Total Hours,Total Commits,Avg Hours/Commit,Features,Fixes,Publishes,Merges,Others")
    
    # Developer data
    for dev, stats in report.developer_stats.items():
        avg_hours = stats.average_hours_per_commit
        features = stats.by_type['FEATURE'].hours
        fixes = stats.by_type['FIX'].hours
        publishes = stats.by_type['PUBLISH'].hours
        merges = stats.by_type['MERGE'].hours
        others = stats.by_type['DEFAULT'].hours
        
        lines.append(f"{dev},{stats.total_hours:.2f},{stats.total_commits},{avg_hours:.2f},{features:.2f},{fixes:.2f},{publishes:.2f},{merges:.2f},{others:.2f}")
    
    return '\n'.join(lines)


def _generate_html_report(generator: ReportGenerator, report) -> str:
    """
    Generate HTML format report.
    
    Args:
        generator: ReportGenerator instance
        report: TimeTrackingReport object
        
    Returns:
        HTML formatted string
    """
    # Get markdown content
    markdown_content = generator.generate_markdown_report(report)
    
    # Simple HTML wrapper (could be enhanced with proper markdown->HTML conversion)
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Horas do Git</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .stats {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="stats">
        <h1>📊 Relatório de Horas do Git</h1>
        <p><strong>Período:</strong> {report.project_stats.start_date} - {report.project_stats.end_date}</p>
        <p><strong>Total de Horas:</strong> {report.project_stats.total_hours:.2f}</p>
        <p><strong>Dias com Commits:</strong> {report.project_stats.total_working_days}</p>
        <p><strong>Desenvolvedores:</strong> {len(report.developer_stats)}</p>
    </div>
    
    <h2>👥 Desenvolvedores</h2>
    <table>
        <tr>
            <th>Desenvolvedor</th>
            <th>Total Horas</th>
            <th>Total Commits</th>
            <th>Média Horas/Commit</th>
            <th>Features</th>
            <th>Fixes</th>
        </tr>
"""
    
    # Add developer rows
    for dev, stats in report.developer_stats.items():
        html_content += f"""        <tr>
            <td>{dev}</td>
            <td>{stats.total_hours:.2f}h</td>
            <td>{stats.total_commits}</td>
            <td>{stats.average_hours_per_commit:.2f}h</td>
            <td>{stats.by_type['FEATURE'].hours:.1f}h</td>
            <td>{stats.by_type['FIX'].hours:.1f}h</td>
        </tr>
"""
    
    html_content += """    </table>
    
    <h2>📋 Detalhes Completos</h2>
    <pre style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; overflow-x: auto;">""" + markdown_content.replace('<', '&lt;').replace('>', '&gt;') + """</pre>
</body>
</html>"""
    
    return html_content


def add_timetrack_arguments(parser):
    """
    Add timetrack-specific arguments to argument parser.
    
    Args:
        parser: ArgumentParser instance
    """
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate detailed time tracking report'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'csv', 'html'],
        default='markdown',
        help='Output format for reports (default: markdown)'
    )
    
    parser.add_argument(
        '--author',
        type=str,
        help='Filter commits by author name (partial match)'
    )
    
    parser.add_argument(
        '--since',
        type=str,
        help='Filter commits since date (YYYY-MM-DD), tag (v1.0.0), or commit hash (abc123)'
    )
    
    parser.add_argument(
        '--until',
        type=str,
        help='Filter commits until date (YYYY-MM-DD), tag (v1.0.0), or commit hash (abc123)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Save report to file (format auto-detected from extension)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output for debugging'
    )


# CLI integration helper
def get_timetrack_help() -> str:
    """Get help text for timetrack command."""
    return """
Analyze development time from Git commits.

Examples:
  codex-ai timetrack                           # Basic analysis
  codex-ai timetrack --report                 # Detailed report
  codex-ai timetrack --author "John"          # Filter by author
  codex-ai timetrack --since "2024-01-01"     # Filter by date
  codex-ai timetrack --since "abc123"         # Filter since commit hash
  codex-ai timetrack --since "v1.0.0"         # Filter since tag
  codex-ai timetrack --until "def456"         # Filter until commit hash
  codex-ai timetrack --until "v2.0.0"         # Filter until tag
  codex-ai timetrack --since "v1.0.0" --until "v2.0.0"  # Between versions
  codex-ai timetrack --format json            # JSON output
  codex-ai timetrack --output report.html     # Save to file
  codex-ai timetrack --report --format csv -o stats.csv  # CSV report to file

The timetrack command analyzes Git commits to estimate development time
based on file types, complexity, and commit patterns. It provides insights
into developer productivity, project timelines, and work distribution.

Both --since and --until parameters accept:
  • Dates: "2024-01-01" (YYYY-MM-DD format)
  • Commit hashes: "abc123" or "abc123def456" (7-40 hex characters)
  • Tags: "v1.0.0" or "1.2.3" (version tags)
"""
