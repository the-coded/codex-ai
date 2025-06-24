"""
Commit parser for Codex-AI.

Provides parsing and analysis of conventional commits and Git commit messages.
Extracts structured information from commit messages for analysis and reporting.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum

from constants.git import CONVENTIONAL_COMMIT_TYPES


class CommitType(Enum):
    """Enumeration of conventional commit types."""
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    REVERT = "revert"
    OTHER = "other"


class CommitScope(Enum):
    """Enumeration of common commit scopes."""
    API = "api"
    UI = "ui"
    CORE = "core"
    DOCS = "docs"
    TESTS = "tests"
    CONFIG = "config"
    DEPS = "deps"
    SECURITY = "security"
    OTHER = "other"


@dataclass
class ParsedCommit:
    """Represents a parsed commit message with structured information."""
    raw_message: str
    type: CommitType
    scope: Optional[str]
    description: str
    body: Optional[str]
    footer: Optional[str]
    breaking_change: bool
    is_conventional: bool
    issues: List[str]
    co_authors: List[str]
    
    @property
    def is_feature(self) -> bool:
        """Check if commit introduces a new feature."""
        return self.type == CommitType.FEAT
    
    @property
    def is_bugfix(self) -> bool:
        """Check if commit fixes a bug."""
        return self.type == CommitType.FIX
    
    @property
    def is_breaking(self) -> bool:
        """Check if commit contains breaking changes."""
        return self.breaking_change
    
    @property
    def is_documentation(self) -> bool:
        """Check if commit is documentation-related."""
        return self.type == CommitType.DOCS
    
    @property
    def formatted_type(self) -> str:
        """Get formatted commit type for display."""
        return self.type.value.title()


class CommitParser:
    """
    Parser for Git commit messages with support for conventional commits.
    
    Parses commit messages according to the Conventional Commits specification
    and extracts structured information for analysis and reporting.
    """
    
    # Conventional commit pattern
    CONVENTIONAL_PATTERN = re.compile(
        r'^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<description>.+)$',
        re.MULTILINE
    )
    
    # Breaking change patterns
    BREAKING_PATTERNS = [
        re.compile(r'^BREAKING CHANGE:', re.MULTILINE | re.IGNORECASE),
        re.compile(r'^BREAKING-CHANGE:', re.MULTILINE | re.IGNORECASE),
        re.compile(r'!\s*:', re.MULTILINE),
    ]
    
    # Issue reference patterns
    ISSUE_PATTERNS = [
        re.compile(r'#(\d+)'),
        re.compile(r'(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)', re.IGNORECASE),
        re.compile(r'(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+(\w+/\w+#\d+)', re.IGNORECASE),
    ]
    
    # Co-author pattern
    CO_AUTHOR_PATTERN = re.compile(r'^Co-authored-by:\s*(.+)\s*<(.+)>$', re.MULTILINE | re.IGNORECASE)
    
    def __init__(self):
        """Initialize commit parser."""
        self.valid_types = set(CONVENTIONAL_COMMIT_TYPES.keys())
    
    def parse(self, commit_message: str) -> ParsedCommit:
        """
        Parse a commit message into structured information.
        
        Args:
            commit_message: Raw commit message to parse
            
        Returns:
            ParsedCommit object with structured information
        """
        # Split message into parts
        lines = commit_message.strip().split('\n')
        subject = lines[0] if lines else ""
        body_lines = lines[1:] if len(lines) > 1 else []
        
        # Remove empty lines at the beginning of body
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        
        # Split body and footer
        body, footer = self._split_body_footer(body_lines)
        
        # Parse conventional commit format
        conventional_match = self.CONVENTIONAL_PATTERN.match(subject)
        
        if conventional_match:
            commit_type = self._parse_type(conventional_match.group('type'))
            scope = conventional_match.group('scope')
            description = conventional_match.group('description').strip()
            breaking_from_subject = bool(conventional_match.group('breaking'))
            is_conventional = True
        else:
            # Fallback parsing for non-conventional commits
            commit_type = self._infer_type_from_message(subject)
            scope = None
            description = subject
            breaking_from_subject = False
            is_conventional = False
        
        # Check for breaking changes
        breaking_change = breaking_from_subject or self._has_breaking_changes(commit_message)
        
        # Extract issues
        issues = self._extract_issues(commit_message)
        
        # Extract co-authors
        co_authors = self._extract_co_authors(commit_message)
        
        return ParsedCommit(
            raw_message=commit_message,
            type=commit_type,
            scope=scope,
            description=description,
            body=body,
            footer=footer,
            breaking_change=breaking_change,
            is_conventional=is_conventional,
            issues=issues,
            co_authors=co_authors
        )
    
    def parse_multiple(self, commit_messages: List[str]) -> List[ParsedCommit]:
        """
        Parse multiple commit messages.
        
        Args:
            commit_messages: List of commit messages to parse
            
        Returns:
            List of ParsedCommit objects
        """
        return [self.parse(message) for message in commit_messages]
    
    def _parse_type(self, type_str: str) -> CommitType:
        """Parse commit type from string."""
        type_lower = type_str.lower()
        
        if type_lower in self.valid_types:
            try:
                return CommitType(type_lower)
            except ValueError:
                pass
        
        return CommitType.OTHER
    
    def _infer_type_from_message(self, message: str) -> CommitType:
        """Infer commit type from message content for non-conventional commits."""
        message_lower = message.lower()
        
        # Common patterns for type inference
        if any(word in message_lower for word in ['add', 'implement', 'create', 'introduce']):
            return CommitType.FEAT
        elif any(word in message_lower for word in ['fix', 'bug', 'issue', 'error', 'problem']):
            return CommitType.FIX
        elif any(word in message_lower for word in ['doc', 'readme', 'comment', 'documentation']):
            return CommitType.DOCS
        elif any(word in message_lower for word in ['refactor', 'restructure', 'reorganize', 'cleanup']):
            return CommitType.REFACTOR
        elif any(word in message_lower for word in ['test', 'spec', 'coverage']):
            return CommitType.TEST
        elif any(word in message_lower for word in ['style', 'format', 'lint', 'prettier']):
            return CommitType.STYLE
        elif any(word in message_lower for word in ['perf', 'performance', 'optimize', 'speed']):
            return CommitType.PERF
        elif any(word in message_lower for word in ['build', 'compile', 'bundle', 'package']):
            return CommitType.BUILD
        elif any(word in message_lower for word in ['ci', 'pipeline', 'workflow', 'action']):
            return CommitType.CI
        elif any(word in message_lower for word in ['chore', 'maintenance', 'update', 'upgrade']):
            return CommitType.CHORE
        elif 'revert' in message_lower:
            return CommitType.REVERT
        
        return CommitType.OTHER
    
    def _split_body_footer(self, body_lines: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Split body lines into body and footer sections."""
        if not body_lines:
            return None, None
        
        # Look for footer markers (lines that look like "Key: Value")
        footer_start = None
        for i, line in enumerate(body_lines):
            if self._is_footer_line(line):
                footer_start = i
                break
        
        if footer_start is not None:
            body_part = body_lines[:footer_start]
            footer_part = body_lines[footer_start:]
            
            # Remove trailing empty lines from body
            while body_part and not body_part[-1].strip():
                body_part.pop()
            
            body = '\n'.join(body_part).strip() if body_part else None
            footer = '\n'.join(footer_part).strip() if footer_part else None
        else:
            body = '\n'.join(body_lines).strip() if body_lines else None
            footer = None
        
        return body, footer
    
    def _is_footer_line(self, line: str) -> bool:
        """Check if a line looks like a footer line (Key: Value format)."""
        line = line.strip()
        
        # Common footer patterns
        footer_patterns = [
            r'^BREAKING CHANGE:',
            r'^BREAKING-CHANGE:',
            r'^Co-authored-by:',
            r'^Signed-off-by:',
            r'^Reviewed-by:',
            r'^Tested-by:',
            r'^Closes?:',
            r'^Fixes?:',
            r'^Resolves?:',
            r'^Refs?:',
            r'^See:',
            r'^\w+(-\w+)*:\s+',
        ]
        
        return any(re.match(pattern, line, re.IGNORECASE) for pattern in footer_patterns)
    
    def _has_breaking_changes(self, message: str) -> bool:
        """Check if commit message indicates breaking changes."""
        return any(pattern.search(message) for pattern in self.BREAKING_PATTERNS)
    
    def _extract_issues(self, message: str) -> List[str]:
        """Extract issue references from commit message."""
        issues = []
        
        for pattern in self.ISSUE_PATTERNS:
            matches = pattern.findall(message)
            issues.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_issues = []
        for issue in issues:
            if issue not in seen:
                seen.add(issue)
                unique_issues.append(issue)
        
        return unique_issues
    
    def _extract_co_authors(self, message: str) -> List[str]:
        """Extract co-authors from commit message."""
        matches = self.CO_AUTHOR_PATTERN.findall(message)
        return [f"{name} <{email}>" for name, email in matches]


class CommitAnalyzer:
    """
    Analyzer for commit patterns and statistics.
    
    Provides analysis of commit patterns, types, and trends for reporting.
    """
    
    def __init__(self):
        """Initialize commit analyzer."""
        self.parser = CommitParser()
    
    def analyze_commits(self, commit_messages: List[str]) -> Dict[str, Any]:
        """
        Analyze a list of commit messages and return statistics.
        
        Args:
            commit_messages: List of commit messages to analyze
            
        Returns:
            Dictionary with analysis results
        """
        parsed_commits = self.parser.parse_multiple(commit_messages)
        
        return {
            'total_commits': len(parsed_commits),
            'conventional_commits': sum(1 for c in parsed_commits if c.is_conventional),
            'conventional_percentage': (sum(1 for c in parsed_commits if c.is_conventional) / len(parsed_commits) * 100) if parsed_commits else 0,
            'type_distribution': self._analyze_type_distribution(parsed_commits),
            'scope_distribution': self._analyze_scope_distribution(parsed_commits),
            'breaking_changes': sum(1 for c in parsed_commits if c.breaking_change),
            'features': sum(1 for c in parsed_commits if c.is_feature),
            'bugfixes': sum(1 for c in parsed_commits if c.is_bugfix),
            'documentation': sum(1 for c in parsed_commits if c.is_documentation),
            'issues_referenced': self._count_unique_issues(parsed_commits),
            'co_authored_commits': sum(1 for c in parsed_commits if c.co_authors),
            'average_description_length': sum(len(c.description) for c in parsed_commits) / len(parsed_commits) if parsed_commits else 0,
        }
    
    def _analyze_type_distribution(self, commits: List[ParsedCommit]) -> Dict[str, int]:
        """Analyze distribution of commit types."""
        distribution = {}
        for commit in commits:
            type_name = commit.type.value
            distribution[type_name] = distribution.get(type_name, 0) + 1
        return distribution
    
    def _analyze_scope_distribution(self, commits: List[ParsedCommit]) -> Dict[str, int]:
        """Analyze distribution of commit scopes."""
        distribution = {}
        for commit in commits:
            scope = commit.scope or 'no-scope'
            distribution[scope] = distribution.get(scope, 0) + 1
        return distribution
    
    def _count_unique_issues(self, commits: List[ParsedCommit]) -> int:
        """Count unique issues referenced across all commits."""
        all_issues = set()
        for commit in commits:
            all_issues.update(commit.issues)
        return len(all_issues)


# Convenience functions
def parse_commit(commit_message: str) -> ParsedCommit:
    """Parse a single commit message."""
    parser = CommitParser()
    return parser.parse(commit_message)


def parse_commits(commit_messages: List[str]) -> List[ParsedCommit]:
    """Parse multiple commit messages."""
    parser = CommitParser()
    return parser.parse_multiple(commit_messages)


def analyze_commit_patterns(commit_messages: List[str]) -> Dict[str, Any]:
    """Analyze commit patterns and return statistics."""
    analyzer = CommitAnalyzer()
    return analyzer.analyze_commits(commit_messages)
