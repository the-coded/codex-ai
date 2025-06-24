"""
Git operations module for Codex-AI.

Provides Git log analysis, commit parsing, repository operations, and change tracking.
"""

from .log_analyzer import (
    GitLogAnalyzer,
    CommitInfo,
    analyze_last_commit_detailed,
    analyze_last_commit_simple
)
from .release_analyzer import (
    GitReleaseAnalyzer,
    ReleaseInfo,
    ReleaseComparison,
    analyze_current_release_detailed,
    analyze_current_release_simple
)
from .tree_generator import (
    GitTreeGenerator,
    TreeGenerationResult,
    generate_project_tree,
    generate_git_changes_trees,
    generate_all_trees
)
from .commit_parser import (
    CommitParser,
    CommitAnalyzer,
    ParsedCommit,
    CommitType,
    CommitScope,
    parse_commit,
    parse_commits,
    analyze_commit_patterns
)
from .changes_tracker import (
    ChangesTracker,
    ChangeAnalyzer,
    FileChange,
    RepositoryState,
    ChangeType,
    FileStatus,
    CommitRange,
    get_repository_state,
    get_changes_since_commit,
    analyze_repository_changes
)

__all__ = [
    # Log Analysis
    'GitLogAnalyzer',
    'CommitInfo', 
    'analyze_last_commit_detailed',
    'analyze_last_commit_simple',
    # Release Analysis
    'GitReleaseAnalyzer',
    'ReleaseInfo',
    'ReleaseComparison',
    'analyze_current_release_detailed',
    'analyze_current_release_simple',
    # Tree Generation
    'GitTreeGenerator',
    'TreeGenerationResult',
    'generate_project_tree',
    'generate_git_changes_trees',
    'generate_all_trees',
    # Commit Parsing
    'CommitParser',
    'CommitAnalyzer',
    'ParsedCommit',
    'CommitType',
    'CommitScope',
    'parse_commit',
    'parse_commits',
    'analyze_commit_patterns',
    # Changes Tracking
    'ChangesTracker',
    'ChangeAnalyzer',
    'FileChange',
    'RepositoryState',
    'ChangeType',
    'FileStatus',
    'CommitRange',
    'get_repository_state',
    'get_changes_since_commit',
    'analyze_repository_changes'
]
