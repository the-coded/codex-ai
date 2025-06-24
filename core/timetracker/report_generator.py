"""
Time tracking report generator for Codex-AI.

Ports the git-hours-report.js functionality to Python.
Generates comprehensive time tracking reports from Git commit analysis.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from .calculator import CommitAnalysis, TimeCalculator


@dataclass
class DeveloperTypeStats:
    """Statistics for a specific commit type for a developer."""
    commits: int = 0
    hours: float = 0.0


@dataclass
class MonthlyStats:
    """Monthly statistics for a developer."""
    commits: int = 0
    hours: float = 0.0
    by_type: Dict[str, DeveloperTypeStats] = field(default_factory=lambda: {
        'FEATURE': DeveloperTypeStats(),
        'FIX': DeveloperTypeStats(),
        'PUBLISH': DeveloperTypeStats(),
        'MERGE': DeveloperTypeStats(),
        'DEFAULT': DeveloperTypeStats()
    })
    working_days: int = 0
    
    @property
    def hours_per_day(self) -> float:
        """Calculate hours per working day."""
        return self.hours / self.working_days if self.working_days > 0 else 0.0


@dataclass
class DeveloperStats:
    """Complete statistics for a developer."""
    total_hours: float = 0.0
    total_commits: int = 0
    by_type: Dict[str, DeveloperTypeStats] = field(default_factory=lambda: {
        'FEATURE': DeveloperTypeStats(),
        'FIX': DeveloperTypeStats(),
        'PUBLISH': DeveloperTypeStats(),
        'MERGE': DeveloperTypeStats(),
        'DEFAULT': DeveloperTypeStats()
    })
    by_month: Dict[str, MonthlyStats] = field(default_factory=dict)
    
    @property
    def average_hours_per_commit(self) -> float:
        """Calculate average hours per commit."""
        return self.total_hours / self.total_commits if self.total_commits > 0 else 0.0


@dataclass
class ProjectStats:
    """Project-wide statistics."""
    start_date: str = ""
    end_date: str = ""
    total_working_days: int = 0
    total_calendar_days: int = 0
    total_hours: float = 0.0
    
    @property
    def commit_frequency(self) -> float:
        """Calculate commit frequency as percentage of days."""
        return (self.total_working_days / self.total_calendar_days * 100) if self.total_calendar_days > 0 else 0.0
    
    @property
    def average_hours_per_working_day(self) -> float:
        """Calculate average hours per working day."""
        return self.total_hours / self.total_working_days if self.total_working_days > 0 else 0.0


@dataclass
class TimeTrackingReport:
    """Complete time tracking report."""
    project_stats: ProjectStats
    developer_stats: Dict[str, DeveloperStats]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'projectStats': {
                'start': self.project_stats.start_date,
                'end': self.project_stats.end_date,
                'totalWorkingDays': self.project_stats.total_working_days,
                'totalCalendarDays': self.project_stats.total_calendar_days,
                'totalHours': self.project_stats.total_hours
            },
            'devStats': {
                dev: {
                    'totalHours': stats.total_hours,
                    'totalCommits': stats.total_commits,
                    'byType': {
                        commit_type: {
                            'commits': type_stats.commits,
                            'hours': type_stats.hours
                        }
                        for commit_type, type_stats in stats.by_type.items()
                    },
                    'byMonth': {
                        month: {
                            'commits': month_stats.commits,
                            'hours': month_stats.hours,
                            'byType': {
                                commit_type: {
                                    'commits': type_stats.commits,
                                    'hours': type_stats.hours
                                }
                                for commit_type, type_stats in month_stats.by_type.items()
                            },
                            'workingDays': month_stats.working_days
                        }
                        for month, month_stats in stats.by_month.items()
                    }
                }
                for dev, stats in self.developer_stats.items()
            }
        }


class ReportGenerator:
    """
    Generates comprehensive time tracking reports.
    
    Processes Git commit analysis data to create detailed reports
    with developer statistics, monthly breakdowns, and project summaries.
    """
    
    # Commit type display names (from JS)
    TYPE_NAMES = {
        'FEATURE': 'Features',
        'FIX': 'Correções',
        'PUBLISH': 'Publicações',
        'MERGE': 'Merges',
        'DEFAULT': 'Outros'
    }
    
    # Month names in Portuguese (from JS)
    MONTH_NAMES = {
        1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
        5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
        9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
    }
    
    def __init__(self):
        """Initialize report generator."""
        pass
    
    def process_commits(self, commits: List[CommitAnalysis]) -> TimeTrackingReport:
        """
        Process commit analysis data into a comprehensive report (ported from JS).
        
        Args:
            commits: List of analyzed commits
            
        Returns:
            Complete time tracking report
        """
        if not commits:
            return TimeTrackingReport(
                project_stats=ProjectStats(),
                developer_stats={}
            )
        
        # Group commits by date (YYYY-MM-DD)
        commits_by_date = defaultdict(list)
        for commit in commits:
            date = commit.date.split(' ')[0]
            commits_by_date[date].append(commit)
        
        # Get unique developers (normalized to lowercase)
        developers = sorted(set(commit.author.lower() for commit in commits))
        
        # Calculate statistics for each developer
        dev_stats = {}
        for dev in developers:
            dev_commits = [c for c in commits if c.author.lower() == dev]
            dev_stats[dev] = self._calculate_developer_stats(dev_commits)
        
        # Calculate project-wide statistics
        project_stats = self._calculate_project_stats(commits, commits_by_date, dev_stats)
        
        return TimeTrackingReport(
            project_stats=project_stats,
            developer_stats=dev_stats
        )
    
    def _calculate_developer_stats(self, dev_commits: List[CommitAnalysis]) -> DeveloperStats:
        """
        Calculate statistics for a single developer (ported from JS).
        
        Args:
            dev_commits: List of commits by this developer
            
        Returns:
            Developer statistics
        """
        stats = DeveloperStats()
        
        # Process each commit
        for commit in dev_commits:
            month = commit.date[:7]  # YYYY-MM
            
            # Update type statistics
            stats.by_type[commit.commit_type].commits += 1
            stats.by_type[commit.commit_type].hours += commit.time_estimates.total
            stats.total_hours += commit.time_estimates.total
            stats.total_commits += 1
            
            # Update monthly statistics
            if month not in stats.by_month:
                stats.by_month[month] = MonthlyStats()
            
            month_stats = stats.by_month[month]
            month_stats.commits += 1
            month_stats.hours += commit.time_estimates.total
            month_stats.by_type[commit.commit_type].commits += 1
            month_stats.by_type[commit.commit_type].hours += commit.time_estimates.total
        
        # Calculate working days for each month
        for month, month_stats in stats.by_month.items():
            # Get unique working days for this month
            working_days = set()
            for commit in dev_commits:
                if commit.date.startswith(month):
                    working_days.add(commit.date.split(' ')[0])
            month_stats.working_days = len(working_days)
        
        return stats
    
    def _calculate_project_stats(self, commits: List[CommitAnalysis], 
                                commits_by_date: Dict[str, List[CommitAnalysis]],
                                dev_stats: Dict[str, DeveloperStats]) -> ProjectStats:
        """
        Calculate project-wide statistics (ported from JS).
        
        Args:
            commits: All commits
            commits_by_date: Commits grouped by date
            dev_stats: Developer statistics
            
        Returns:
            Project statistics
        """
        stats = ProjectStats()
        
        # Get date range
        stats.start_date = commits[-1].date.split(' ')[0]  # Last commit (oldest)
        stats.end_date = commits[0].date.split(' ')[0]     # First commit (newest)
        stats.total_working_days = len(commits_by_date)
        
        # Calculate calendar days
        start_date = datetime.strptime(stats.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(stats.end_date, '%Y-%m-%d')
        stats.total_calendar_days = (end_date - start_date).days + 1
        
        # Calculate total hours
        stats.total_hours = sum(dev.total_hours for dev in dev_stats.values())
        
        return stats
    
    def generate_markdown_report(self, report: TimeTrackingReport) -> str:
        """
        Generate markdown report (ported from JS).
        
        Args:
            report: Time tracking report
            
        Returns:
            Markdown report string
        """
        markdown = '# Relatório de Horas do Git\n\n'
        
        # Project Summary
        markdown += '## Resumo do Projeto\n'
        markdown += f'- **Período**: {report.project_stats.start_date} - {report.project_stats.end_date}\n'
        markdown += f'- **Dias Totais**: {report.project_stats.total_calendar_days}\n'
        markdown += f'- **Dias com Commits**: {report.project_stats.total_working_days}\n'
        markdown += f'- **Total de Horas**: {report.project_stats.total_hours:.2f}\n\n'
        
        # Developer Statistics
        markdown += '## Estatísticas por Desenvolvedor\n\n'
        
        for dev, stats in sorted(report.developer_stats.items()):
            markdown += f'### {dev}\n\n'
            
            # Summary for this developer
            markdown += f'- **Total de Horas**: {stats.total_hours:.2f}\n'
            markdown += f'- **Total de Commits**: {stats.total_commits}\n'
            markdown += f'- **Média de Horas por Commit**: {stats.average_hours_per_commit:.2f}\n\n'
            
            # Monthly table for this developer
            markdown += '| Mês | Dias Ativos | Features | Correções | Publicações | Merges | Outros | Total Horas | Horas/Dia |\n'
            markdown += '|-----|-------------|-----------|------------|-------------|---------|---------|-------------|------------|\n'
            
            for month, data in sorted(stats.by_month.items()):
                formatted_month = self._format_month(month)
                markdown += f'| {formatted_month} | {data.working_days} | '
                markdown += f'{data.by_type["FEATURE"].commits} ({data.by_type["FEATURE"].hours:.1f}h) | '
                markdown += f'{data.by_type["FIX"].commits} ({data.by_type["FIX"].hours:.1f}h) | '
                markdown += f'{data.by_type["PUBLISH"].commits} ({data.by_type["PUBLISH"].hours:.1f}h) | '
                markdown += f'{data.by_type["MERGE"].commits} ({data.by_type["MERGE"].hours:.1f}h) | '
                markdown += f'{data.by_type["DEFAULT"].commits} ({data.by_type["DEFAULT"].hours:.1f}h) | '
                markdown += f'{data.hours:.1f} | {data.hours_per_day:.1f} |\n'
            
            markdown += '\n'
            
            # Work distribution for this developer
            markdown += '#### Distribuição do Trabalho\n\n'
            for commit_type, type_data in stats.by_type.items():
                percentage = (type_data.hours / stats.total_hours * 100) if stats.total_hours > 0 else 0
                type_name = self.TYPE_NAMES[commit_type]
                markdown += f'- {type_name}: {type_data.commits} commits, {type_data.hours:.1f} horas ({percentage:.1f}% do tempo)\n'
            markdown += '\n'
        
        # Project-wide work pattern
        markdown += '## Padrão de Trabalho do Projeto\n'
        markdown += f'- Período Total: {report.project_stats.total_calendar_days} dias\n'
        markdown += f'- Dias com Commits: {report.project_stats.total_working_days} dias\n'
        markdown += f'- Frequência de Commits: {report.project_stats.commit_frequency:.1f}% dos dias\n'
        markdown += f'- Média de Horas por Dia com Commits: {report.project_stats.average_hours_per_working_day:.2f}\n\n'
        
        return markdown
    
    def _format_month(self, month_str: str) -> str:
        """
        Format month string to Portuguese (ported from JS).
        
        Args:
            month_str: Month in YYYY-MM format
            
        Returns:
            Formatted month string
        """
        year, month = month_str.split('-')
        month_num = int(month)
        month_name = self.MONTH_NAMES.get(month_num, 'unknown')
        return f'{month_name} {year}'
    
    def generate_json_report(self, report: TimeTrackingReport) -> str:
        """
        Generate JSON report.
        
        Args:
            report: Time tracking report
            
        Returns:
            JSON report string
        """
        return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
    
    def process_analysis_file(self, analysis_file: str) -> TimeTrackingReport:
        """
        Process analysis from JSON file (ported from JS).
        
        Args:
            analysis_file: Path to analysis JSON file
            
        Returns:
            Time tracking report
        """
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # Convert JSON data back to CommitAnalysis objects
        commits = []
        for commit_data in analysis_data:
            # Create CommitAnalysis from dict (simplified reconstruction)
            from .calculator import CommitStats, TimeEstimate, CommitAnalysis
            
            stats = CommitStats(
                files_changed=commit_data['stats']['filesChanged'],
                additions=commit_data['stats']['additions'],
                deletions=commit_data['stats']['deletions'],
                file_types=commit_data['stats']['fileTypes'],
                files=commit_data['stats']['files']
            )
            
            time_estimates = TimeEstimate(
                planning=commit_data['timeEstimates']['planning'],
                implementation=commit_data['timeEstimates']['implementation']
            )
            
            commit = CommitAnalysis(
                hash=commit_data['hash'],
                author=commit_data['author'],
                date=commit_data['date'],
                message=commit_data['message'],
                commit_type=commit_data['type'],
                complexity_type=commit_data['complexityType'],
                complexity_level=commit_data['complexityLevel'],
                stats=stats,
                time_estimates=time_estimates
            )
            
            commits.append(commit)
        
        return self.process_commits(commits)
    
    def save_reports(self, report: TimeTrackingReport, base_filename: str = "git-hours-report"):
        """
        Save both JSON and Markdown reports to files.
        
        Args:
            report: Time tracking report
            base_filename: Base filename for reports
        """
        # Save JSON report
        json_filename = f"{base_filename}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_json_report(report))
        
        # Save Markdown report
        md_filename = f"{base_filename}.md"
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report(report))
        
        return json_filename, md_filename


# Convenience functions
def generate_time_report(commits: List[CommitAnalysis]) -> TimeTrackingReport:
    """Generate time tracking report from commits."""
    generator = ReportGenerator()
    return generator.process_commits(commits)


def generate_report_from_analysis_file(analysis_file: str) -> TimeTrackingReport:
    """Generate report from analysis JSON file."""
    generator = ReportGenerator()
    return generator.process_analysis_file(analysis_file)


def create_full_time_report(repo_path: str = ".") -> TimeTrackingReport:
    """Create complete time report from repository analysis."""
    calculator = TimeCalculator(repo_path)
    commits = calculator.analyze_repository()
    return generate_time_report(commits)
