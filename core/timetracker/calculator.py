"""
Time tracking calculator for Codex-AI.

Ports the JavaScript timetracker functionality to Python.
Analyzes Git commits to estimate development time and complexity.
"""

import subprocess
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from pathlib import Path

from constants.timetrack import (
    FILE_TYPE_MULTIPLIERS, COMMIT_TYPE_MULTIPLIERS, COMPLEXITY_THRESHOLDS,
    STRUCTURAL_PATTERNS, ALGORITHMIC_PATTERNS
)


@dataclass
class CommitStats:
    """Statistics for a single commit."""
    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
    file_types: Dict[str, int] = field(default_factory=dict)
    files: List[str] = field(default_factory=list)
    
    @property
    def net_changes(self) -> int:
        """Get net changes (additions - deletions)."""
        return self.additions - self.deletions
    
    @property
    def total_changes(self) -> int:
        """Get total changes (additions + deletions)."""
        return self.additions + self.deletions


@dataclass
class TimeEstimate:
    """Time estimates for a commit."""
    planning: float = 0.0
    implementation: float = 0.0
    
    @property
    def total(self) -> float:
        """Get total time estimate."""
        return self.planning + self.implementation


@dataclass
class CommitAnalysis:
    """Complete analysis of a single commit."""
    hash: str
    author: str
    date: str
    message: str
    commit_type: str
    complexity_type: str
    complexity_level: str
    stats: CommitStats
    time_estimates: TimeEstimate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'hash': self.hash,
            'author': self.author,
            'date': self.date,
            'message': self.message,
            'type': self.commit_type,
            'complexityType': self.complexity_type,
            'complexityLevel': self.complexity_level,
            'stats': {
                'filesChanged': self.stats.files_changed,
                'additions': self.stats.additions,
                'deletions': self.stats.deletions,
                'fileTypes': self.stats.file_types,
                'files': self.stats.files
            },
            'timeEstimates': {
                'planning': self.time_estimates.planning,
                'implementation': self.time_estimates.implementation,
                'total': self.time_estimates.total
            }
        }


class ComplexityType:
    """Complexity type constants."""
    STRUCTURAL = "STRUCTURAL"
    ALGORITHMIC = "ALGORITHMIC"


class ComplexityLevel:
    """Complexity level constants."""
    TRIVIAL = "TRIVIAL"
    BASIC = "BASIC"
    MODERATE = "MODERATE"
    COMPLEX = "COMPLEX"
    VERY_COMPLEX = "VERY_COMPLEX"


class CommitType:
    """Commit type constants."""
    FEATURE = "FEATURE"
    FIX = "FIX"
    PUBLISH = "PUBLISH"
    MERGE = "MERGE"
    DEFAULT = "DEFAULT"


class TimeCalculator:
    """
    Main time tracking calculator.
    
    Analyzes Git commits to estimate development time based on:
    - File types and complexity
    - Commit patterns
    - Code changes (additions/deletions)
    - Structural vs algorithmic complexity
    """
    
    # File type categories (from JS)
    FILE_CATEGORIES = {
        'LOGIC': {
            'extensions': ['js', 'ts', 'jsx', 'tsx'],
            'base_time': {
                'planning': 1.0,      # 1h
                'implementation': 0.04  # ~2.4min per line
            }
        },
        'CONFIG': {
            'extensions': ['json', 'yml', 'yaml', 'lock', 'gitignore', 'npmrc', 'env'],
            'base_time': {
                'planning': 0.25,     # 15min
                'implementation': 0.01  # ~0.6min per line
            }
        },
        'STYLE': {
            'extensions': ['css', 'scss', 'sass', 'less', 'stylus'],
            'base_time': {
                'planning': 0.5,      # 30min
                'implementation': 0.02  # ~1.2min per line
            }
        },
        'DOCS': {
            'extensions': ['md', 'mdx', 'txt', 'doc', 'docx', 'html'],
            'base_time': {
                'planning': 0.3,      # 18min
                'implementation': 0.015  # ~0.9min per line
            }
        }
    }
    
    # Complexity levels (from JS)
    COMPLEXITY_LEVELS = {
        ComplexityType.STRUCTURAL: {
            ComplexityLevel.TRIVIAL: 0.5,
            ComplexityLevel.BASIC: 0.8,
            ComplexityLevel.MODERATE: 1.2,
            ComplexityLevel.COMPLEX: 1.6,
            ComplexityLevel.VERY_COMPLEX: 2.0
        },
        ComplexityType.ALGORITHMIC: {
            ComplexityLevel.TRIVIAL: 0.5,
            ComplexityLevel.BASIC: 1.0,
            ComplexityLevel.MODERATE: 1.5,
            ComplexityLevel.COMPLEX: 2.0,
            ComplexityLevel.VERY_COMPLEX: 2.5
        }
    }
    
    # Commit type multipliers (from JS)
    COMMIT_MULTIPLIERS = {
        CommitType.FEATURE: 1.0,
        CommitType.FIX: 0.5,
        CommitType.PUBLISH: 0.1,
        CommitType.MERGE: 0.0,
        CommitType.DEFAULT: 0.8
    }
    
    # Time calculation constants (from JS)
    PLANNING_BASE = 0.3
    PLANNING_NET_WEIGHT = 0.7
    PLANNING_DELETION_FACTOR = 0.2
    DELETION_TIME_FACTOR = 0.1
    
    # File patterns (from JS)
    STRUCTURAL_FILE_TYPES = ['css', 'scss', 'less', 'html', 'jsx', 'tsx', 'svg']
    ALGORITHMIC_FILE_TYPES = ['js', 'ts', 'jsx', 'tsx']
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize time calculator.
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = Path(repo_path)
    
    def get_file_extension(self, filename: str) -> str:
        """
        Get file extension using regex (ported from JS).
        
        Args:
            filename: File name to analyze
            
        Returns:
            File extension without dot
        """
        # Get main extension (.ts, .tsx, etc)
        base_match = re.search(r'\.([a-zA-Z0-9]+)(?:\})?$', filename)
        if not base_match:
            return 'unknown'
        
        # Check for .stories or .test before extension
        special_match = re.search(r'\.(stories|test|spec)\.([a-zA-Z0-9]+)(?:\})?$', filename)
        if special_match:
            return special_match.group(2)  # Return real extension (ts/tsx)
        
        return base_match.group(1)
    
    def get_commit_type(self, message: str) -> str:
        """
        Determine commit type from message (ported from JS).
        
        Args:
            message: Commit message
            
        Returns:
            Commit type constant
        """
        # Merge commits
        if message.startswith('Merge'):
            return CommitType.MERGE
        
        # Feature commits
        if message.startswith('feat:'):
            return CommitType.FEATURE
        if re.match(r'^v?\d+\.\d+\.\d+.*\s+-\s+.*feature', message, re.IGNORECASE):
            return CommitType.FEATURE
        if re.match(r'^.*first commit.*mvp', message, re.IGNORECASE):
            return CommitType.FEATURE
        
        # Fix commits
        if message.startswith('fix:'):
            return CommitType.FIX
        if re.match(r'^v?\d+\.\d+\.\d+.*\s+-\s+.*fix', message, re.IGNORECASE):
            return CommitType.FIX
        
        # Release commits
        if re.match(r'^release\/v\d+', message, re.IGNORECASE):
            return CommitType.PUBLISH
        if re.match(r'^v?\d+\.\d+\.\d+\s*$', message):
            return CommitType.PUBLISH
        if re.match(r'^Publish\s+v?\d+\.\d+\.\d+$', message):
            return CommitType.PUBLISH
        if re.match(r'^New Release:', message, re.IGNORECASE):
            return CommitType.PUBLISH
        
        # Version with fix/feature
        if re.match(r'^v?\d+\.\d+\.\d+.*fix', message, re.IGNORECASE):
            return CommitType.FIX
        if re.match(r'^v?\d+\.\d+\.\d+.*feat', message, re.IGNORECASE):
            return CommitType.FEATURE
        
        return CommitType.DEFAULT
    
    def get_file_category(self, file_type: str) -> Dict[str, Any]:
        """
        Get file category and base time (ported from JS).
        
        Args:
            file_type: File extension
            
        Returns:
            Dictionary with category and base_time
        """
        for category, info in self.FILE_CATEGORIES.items():
            if file_type in info['extensions']:
                return {
                    'category': category,
                    'base_time': info['base_time']
                }
        
        # Default to LOGIC if unknown
        return {
            'category': 'LOGIC',
            'base_time': self.FILE_CATEGORIES['LOGIC']['base_time']
        }
    
    def calculate_structural_score(self, stats: CommitStats) -> float:
        """
        Calculate structural complexity score (ported from JS).
        
        Args:
            stats: Commit statistics
            
        Returns:
            Structural complexity score
        """
        score = 0.0
        
        # Check file patterns
        for file_path in stats.files:
            if any(pattern in file_path for pattern in STRUCTURAL_PATTERNS):
                score += 10
        
        # Check file types
        for file_type, count in stats.file_types.items():
            if file_type in self.STRUCTURAL_FILE_TYPES:
                score += count * 5
        
        # File count impact
        score += stats.files_changed * 2
        
        # Style files have high structural impact
        style_files = sum(1 for f in stats.files 
                         if f.endswith(('.css', '.scss', '.less')))
        score += style_files * 8
        
        return score
    
    def calculate_algorithmic_score(self, stats: CommitStats) -> float:
        """
        Calculate algorithmic complexity score (ported from JS).
        
        Args:
            stats: Commit statistics
            
        Returns:
            Algorithmic complexity score
        """
        score = 0.0
        
        # Check file patterns
        for file_path in stats.files:
            if any(pattern in file_path for pattern in ALGORITHMIC_PATTERNS):
                score += 15
        
        # Check file types
        for file_type, count in stats.file_types.items():
            if file_type in self.ALGORITHMIC_FILE_TYPES:
                score += count * 8
        
        # Lines per file (more lines = more algorithmic complexity)
        # Consider additions with higher weight than deletions
        avg_lines_per_file = (stats.additions + stats.deletions * 0.10) / stats.files_changed if stats.files_changed > 0 else 0
        score += min(avg_lines_per_file / 10, 20)
        
        # Deletion ratio (reduced and limited)
        deletion_ratio = stats.deletions / (stats.additions or 1)
        score += min(deletion_ratio, 1.5) * 5  # Max 1.5x and reduced from 15 to 5
        
        return score
    
    def get_complexity_level(self, score: float) -> str:
        """
        Determine complexity level from score (ported from JS).
        
        Args:
            score: Complexity score
            
        Returns:
            Complexity level constant
        """
        if score <= 10:
            return ComplexityLevel.TRIVIAL
        elif score <= 30:
            return ComplexityLevel.BASIC
        elif score <= 60:
            return ComplexityLevel.MODERATE
        elif score <= 100:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.VERY_COMPLEX
    
    def analyze_complexity(self, stats: CommitStats) -> Tuple[str, str]:
        """
        Analyze complexity type and level (ported from JS).
        
        Args:
            stats: Commit statistics
            
        Returns:
            Tuple of (complexity_type, complexity_level)
        """
        # Calculate scores
        structural_score = self.calculate_structural_score(stats)
        algorithmic_score = self.calculate_algorithmic_score(stats)
        
        # Determine dominant type
        complexity_type = (ComplexityType.STRUCTURAL 
                          if structural_score > algorithmic_score 
                          else ComplexityType.ALGORITHMIC)
        
        # Calculate final score based on type
        final_score = structural_score if complexity_type == ComplexityType.STRUCTURAL else algorithmic_score
        
        # Determine level
        complexity_level = self.get_complexity_level(final_score)
        
        return complexity_type, complexity_level
    
    def calculate_time_estimates(self, stats: CommitStats, commit_type: str, 
                               complexity_type: str, complexity_level: str) -> TimeEstimate:
        """
        Calculate time estimates for a commit (ported from JS).
        
        Args:
            stats: Commit statistics
            commit_type: Type of commit
            complexity_type: Complexity type
            complexity_level: Complexity level
            
        Returns:
            TimeEstimate object
        """
        total_planning_hours = 0.0
        total_implementation_hours = 0.0
        
        # Process each file type
        for file_type, count in stats.file_types.items():
            file_info = self.get_file_category(file_type)
            base_time = file_info['base_time']
            type_ratio = count / stats.files_changed if stats.files_changed > 0 else 0
            
            # Separate additions and deletions
            added_lines = stats.additions * type_ratio
            deleted_lines = stats.deletions * type_ratio
            total_lines = added_lines + deleted_lines
            
            # Get complexity multiplier
            complexity_multiplier = self.COMPLEXITY_LEVELS[complexity_type][complexity_level]
            
            # Calculate net ratio for planning
            net_ratio = (max(0, stats.additions - stats.deletions) / total_lines 
                        if total_lines > 0 else 0)
            
            # Planning multiplier base + net ratio weight
            planning_multiplier = self.PLANNING_BASE + (net_ratio * self.PLANNING_NET_WEIGHT)
            
            # Reduce if more deletions than additions
            if stats.deletions > stats.additions:
                planning_multiplier *= self.PLANNING_DELETION_FACTOR
            
            # Get commit type multiplier
            type_multiplier = self.COMMIT_MULTIPLIERS[commit_type]
            
            # Calculate hours for this file type
            total_planning_hours += (base_time['planning'] * 
                                   complexity_multiplier *
                                   type_ratio *
                                   planning_multiplier *
                                   type_multiplier)
            
            # Additions have full weight, deletions have reduced weight
            total_implementation_hours += (
                (added_lines * base_time['implementation'] * complexity_multiplier * type_multiplier) +
                (deleted_lines * base_time['implementation'] * complexity_multiplier * 
                 self.DELETION_TIME_FACTOR * type_multiplier)
            )
        
        return TimeEstimate(
            planning=total_planning_hours,
            implementation=total_implementation_hours
        )
    
    def get_detailed_git_log(self) -> List[CommitAnalysis]:
        """
        Get detailed git log with patches (ported from JS).
        
        Returns:
            List of CommitAnalysis objects
        """
        try:
            # Get detailed git log with stats
            result = subprocess.run([
                'git', 'log', 
                '--pretty=format:%h|%an|%ad|%s',
                '--date=format:%Y-%m-%d %H:%M:%S',
                '--numstat'
            ], cwd=self.repo_path, capture_output=True, text=True, check=True)
            
            log_output = result.stdout
            commits = []
            current_commit = None
            
            for line in log_output.split('\n'):
                if '|' in line:
                    # This is a commit header
                    if current_commit:
                        commits.append(self._finalize_commit(current_commit))
                    
                    parts = line.split('|')
                    if len(parts) >= 4:
                        hash_val, author, date, message = parts[0], parts[1], parts[2], '|'.join(parts[3:])
                        
                        # Ignore CI commits
                        if author != 'github-ci':
                            current_commit = {
                                'hash': hash_val,
                                'author': author,
                                'date': date,
                                'message': message,
                                'stats': CommitStats()
                            }
                        else:
                            current_commit = None
                
                elif line.strip() and current_commit:
                    # This is a file stat line
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        additions_str, deletions_str, file_path = parts[0], parts[1], parts[2]
                        
                        if file_path:
                            file_type = self.get_file_extension(file_path)
                            current_commit['stats'].file_types[file_type] = (
                                current_commit['stats'].file_types.get(file_type, 0) + 1
                            )
                            current_commit['stats'].files_changed += 1
                            current_commit['stats'].files.append(file_path)
                            current_commit['stats'].additions += int(additions_str) if additions_str.isdigit() else 0
                            current_commit['stats'].deletions += int(deletions_str) if deletions_str.isdigit() else 0
            
            # Don't forget the last commit
            if current_commit:
                commits.append(self._finalize_commit(current_commit))
            
            return commits
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e}")
    
    def _finalize_commit(self, commit_data: Dict[str, Any]) -> CommitAnalysis:
        """
        Finalize commit analysis with time estimates.
        
        Args:
            commit_data: Raw commit data
            
        Returns:
            Complete CommitAnalysis object
        """
        stats = commit_data['stats']
        commit_type = self.get_commit_type(commit_data['message'])
        complexity_type, complexity_level = self.analyze_complexity(stats)
        time_estimates = self.calculate_time_estimates(stats, commit_type, complexity_type, complexity_level)
        
        return CommitAnalysis(
            hash=commit_data['hash'],
            author=commit_data['author'],
            date=commit_data['date'],
            message=commit_data['message'],
            commit_type=commit_type,
            complexity_type=complexity_type,
            complexity_level=complexity_level,
            stats=stats,
            time_estimates=time_estimates
        )
    
    def analyze_repository(self) -> List[CommitAnalysis]:
        """
        Analyze entire repository for time tracking.
        
        Returns:
            List of analyzed commits
        """
        return self.get_detailed_git_log()
    
    def generate_analysis_json(self, commits: List[CommitAnalysis]) -> str:
        """
        Generate JSON analysis report.
        
        Args:
            commits: List of analyzed commits
            
        Returns:
            JSON string
        """
        return json.dumps([commit.to_dict() for commit in commits], indent=2)


# Convenience functions
def analyze_repository_time(repo_path: str = ".") -> List[CommitAnalysis]:
    """Analyze repository time tracking."""
    calculator = TimeCalculator(repo_path)
    return calculator.analyze_repository()


def calculate_commit_time(commit_stats: CommitStats, commit_message: str) -> TimeEstimate:
    """Calculate time estimate for a single commit."""
    calculator = TimeCalculator()
    commit_type = calculator.get_commit_type(commit_message)
    complexity_type, complexity_level = calculator.analyze_complexity(commit_stats)
    return calculator.calculate_time_estimates(commit_stats, commit_type, complexity_type, complexity_level)
