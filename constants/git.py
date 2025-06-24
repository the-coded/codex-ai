"""
Git-related constants for repository analysis and operations.

This module contains Git commands, patterns, and configurations used throughout
the Codex-AI system for analyzing repositories, extracting commit information,
and managing Git operations.
"""

from typing import Dict, List, Any

# ===== CONVENTIONAL COMMIT TYPES =====
#
# 📊 EXPLANATION:
# Based on Conventional Commits specification (conventionalcommits.org)
# These patterns help categorize commits for changelog generation and time tracking
#
# Each type has:
# - emoji: Visual representation for reports
# - description: What this commit type represents
# - changelog_section: Where it appears in changelog
# - time_impact: Relative time complexity (used with timetrack constants)

CONVENTIONAL_COMMIT_TYPES = {
    "feat": {
        "emoji": "✨",
        "description": "New feature",
        "changelog_section": "Features",
        "time_impact": "high"
    },
    "fix": {
        "emoji": "🐛", 
        "description": "Bug fix",
        "changelog_section": "Bug Fixes",
        "time_impact": "medium"
    },
    "docs": {
        "emoji": "📚",
        "description": "Documentation changes",
        "changelog_section": "Documentation", 
        "time_impact": "low"
    },
    "style": {
        "emoji": "💄",
        "description": "Code style changes (formatting, etc)",
        "changelog_section": "Styles",
        "time_impact": "low"
    },
    "refactor": {
        "emoji": "♻️",
        "description": "Code refactoring",
        "changelog_section": "Code Refactoring",
        "time_impact": "medium"
    },
    "perf": {
        "emoji": "⚡",
        "description": "Performance improvements",
        "changelog_section": "Performance",
        "time_impact": "medium"
    },
    "test": {
        "emoji": "✅",
        "description": "Test changes",
        "changelog_section": "Tests",
        "time_impact": "medium"
    },
    "build": {
        "emoji": "👷",
        "description": "Build system changes",
        "changelog_section": "Build System",
        "time_impact": "low"
    },
    "ci": {
        "emoji": "💚",
        "description": "CI/CD changes",
        "changelog_section": "Continuous Integration",
        "time_impact": "low"
    },
    "chore": {
        "emoji": "🔧",
        "description": "Maintenance tasks",
        "changelog_section": "Chores",
        "time_impact": "low"
    },
    "revert": {
        "emoji": "⏪",
        "description": "Revert previous commit",
        "changelog_section": "Reverts",
        "time_impact": "low"
    }
}

# ===== EXCLUDE PATTERNS =====
#
# 📊 EXPLANATION:
# Files to exclude from Git analysis and changelog generation.
# These are typically auto-generated, temporary, or non-essential files.
#
# Patterns use Git pathspec format:
# - :(exclude)pattern excludes files matching pattern
# - ** matches any number of directories
# - * matches any characters except /

EXCLUDE_PATTERNS = [
    # Lock files (auto-generated)
    ":(exclude)yarn.lock",
    ":(exclude)package-lock.json", 
    ":(exclude)pnpm-lock.yaml",
    ":(exclude)Pipfile.lock",
    ":(exclude)poetry.lock",
    
    # Python cache and compiled files
    ":(exclude)*.pyc",
    ":(exclude)__pycache__/**",
    ":(exclude)*.pyo",
    ":(exclude)*.pyd",
    ":(exclude).Python",
    
    # Environment and config files
    ":(exclude).env",
    ":(exclude).env.local",
    ":(exclude).env.*.local",
    
    # Build and distribution directories
    ":(exclude)dist/**",
    ":(exclude)build/**",
    ":(exclude)out/**",
    ":(exclude).next/**",
    ":(exclude).nuxt/**",
    
    # Log files
    ":(exclude)*.log",
    ":(exclude)logs/**",
    ":(exclude)npm-debug.log*",
    ":(exclude)yarn-debug.log*",
    ":(exclude)yarn-error.log*",
    
    # OS generated files
    ":(exclude).DS_Store",
    ":(exclude).DS_Store?",
    ":(exclude)._*",
    ":(exclude).Spotlight-V100",
    ":(exclude).Trashes",
    ":(exclude)ehthumbs.db",
    ":(exclude)Thumbs.db",
    
    # Coverage and test output
    ":(exclude)coverage/**",
    ":(exclude).nyc_output/**",
    ":(exclude).coverage",
    ":(exclude)htmlcov/**",
    
    # Minified files
    ":(exclude)*.min.js",
    ":(exclude)*.min.css",
    ":(exclude)*.min.map",
    
    # Backup and temporary files
    ":(exclude)_old/**",
    ":(exclude)*.bak",
    ":(exclude)*.tmp",
    ":(exclude)*.temp",
    
    # IDE and editor files
    ":(exclude).vscode/**",
    ":(exclude).idea/**",
    ":(exclude)*.swp",
    ":(exclude)*.swo",
    ":(exclude)*~",
    
    # Node modules and dependencies
    ":(exclude)node_modules/**",
    ":(exclude).pnp/**",
    ":(exclude).pnp.js"
]

# ===== GIT COMMANDS =====
#
# 📊 EXPLANATION:
# Common Git commands used throughout the system.
# These are templates that can be formatted with specific parameters.
#
# Command categories:
# - log: Getting commit history and information
# - show: Showing commit details and changes
# - status: Repository status and changes
# - diff: Comparing changes between commits/branches
# - rev: Getting commit hashes and references

GIT_COMMANDS = {
    # Log commands for commit history
    "log": {
        "last_commit_hash": "git rev-parse HEAD",
        "commit_parents": "git rev-list --parents -n 1 {commit_hash}",
        "commit_history": "git log --pretty=format:\"{format}\" {options}",
        "commit_history_with_stats": "git log --pretty=format:\"{format}\" --numstat {options}",
        "commits_in_range": "git log --pretty=format:\"%H\" --reverse {range}",
        "is_merge_commit": "git rev-list --parents -n 1 {commit_hash} | wc -w"
    },
    
    # Show commands for commit details
    "show": {
        "commit_details": "git show --pretty=format:\"{format}\" --patch {commit_hash} -- . {exclude_pathspec}",
        "commit_details_simple": "git show --pretty=format:\"{format}\" --name-status {commit_hash} -- . {exclude_pathspec}",
        "commit_files": "git show --name-status --format= {commit_hash}",
        "commit_stats": "git show --stat {commit_hash}"
    },
    
    # Status commands for current repository state
    "status": {
        "porcelain": "git status --porcelain",
        "staged_files": "git diff --cached --name-only",
        "modified_files": "git diff --name-only", 
        "untracked_files": "git ls-files --others --exclude-standard",
        "all_changes": "git status --porcelain"
    },
    
    # Diff commands for comparing changes
    "diff": {
        "since_commit": "git diff --name-only {commit}",
        "between_commits": "git diff --name-only {commit1}..{commit2}",
        "branch_range": "git diff --name-only {base}..{head}",
        "last_commit": "git diff --name-only HEAD~1",
        "staged_changes": "git diff --cached --name-only"
    },
    
    # Rev commands for getting references
    "rev": {
        "parse_ref": "git rev-parse {ref}",
        "git_dir": "git rev-parse --git-dir",
        "show_toplevel": "git rev-parse --show-toplevel",
        "current_branch": "git rev-parse --abbrev-ref HEAD",
        "commit_parents": "git rev-parse {commit_hash}^1 {commit_hash}^2"
    }
}

# ===== GIT STATUS COMMANDS =====
#
# 📊 EXPLANATION:
# Specific commands for different Git status operations.
# Used primarily by the uidocs command for local vs pipeline mode detection.
#
# Each command returns different types of file lists:
# - staged: Files added to staging area (git add)
# - modified: Files changed but not staged
# - untracked: New files not tracked by Git
# - all_changes: All files with any changes (porcelain format)

GIT_STATUS_COMMANDS = {
    "staged": {
        "command": "git diff --cached --name-only",
        "description": "Files staged for commit",
        "use_case": "uidocs local mode - process only staged files"
    },
    "modified": {
        "command": "git diff --name-only",
        "description": "Modified files not yet staged", 
        "use_case": "uidocs local mode - process working directory changes"
    },
    "untracked": {
        "command": "git ls-files --others --exclude-standard",
        "description": "New files not tracked by Git",
        "use_case": "uidocs local mode - include new files if requested"
    },
    "all_changes": {
        "command": "git status --porcelain",
        "description": "All changes in porcelain format",
        "use_case": "uidocs local mode - comprehensive change detection"
    }
}

# ===== GIT DIFF COMMANDS =====
#
# 📊 EXPLANATION:
# Commands for getting file differences between commits, branches, or states.
# Used primarily by uidocs pipeline mode and changelog generation.
#
# Templates use {placeholders} that should be replaced with actual values:
# - {commit}: Specific commit hash
# - {base}: Base branch or commit
# - {head}: Head branch or commit
# - {range}: Git range specification (e.g., "main..feature")

GIT_DIFF_COMMANDS = {
    "since_commit": {
        "command": "git diff --name-only {commit}",
        "description": "Files changed since specific commit",
        "use_case": "uidocs pipeline mode - changes since last deployment"
    },
    "branch_range": {
        "command": "git diff --name-only {base}..{head}",
        "description": "Files changed between branches",
        "use_case": "uidocs pipeline mode - PR/MR changes"
    },
    "last_commit": {
        "command": "git diff --name-only HEAD~1",
        "description": "Files changed in last commit",
        "use_case": "changelog generation - recent changes"
    },
    "commit_range": {
        "command": "git diff --name-only {range}",
        "description": "Files changed in commit range",
        "use_case": "uidocs pipeline mode - feature branch changes"
    },
    "with_stats": {
        "command": "git diff --stat {range}",
        "description": "Changes with line count statistics",
        "use_case": "timetrack analysis - quantify changes"
    }
}

# ===== GIT LOG FORMATS =====
#
# 📊 EXPLANATION:
# Pretty format strings for git log commands.
# These control how commit information is displayed in outputs.
#
# Format placeholders:
# - %H: Full commit hash
# - %h: Abbreviated commit hash  
# - %an: Author name
# - %ae: Author email
# - %ad: Author date
# - %s: Subject (commit message first line)
# - %b: Body (commit message without subject)

GIT_LOG_FORMATS = {
    "detailed": {
        "format": "Author: %an%nDate: %ad%nMessage: %s%n%nBody:%n%b",
        "use_case": "Detailed changelog generation with full context"
    },
    "simple": {
        "format": "%an - %ad%n%s%n%b", 
        "use_case": "Simple changelog when detailed log is too large"
    },
    "oneline": {
        "format": "%h - %s",
        "use_case": "Quick commit summaries"
    },
    "structured": {
        "format": "%h|%an|%ad|%s",
        "use_case": "Machine-readable format for parsing"
    },
    "timetrack": {
        "format": "%h|%an|%ad|%s",
        "use_case": "Time tracking analysis with structured data"
    }
}

# ===== MERGE COMMIT DETECTION =====
#
# 📊 EXPLANATION:
# Patterns and commands for detecting and handling merge commits.
# Merge commits require special handling in changelog and time tracking.
#
# Detection methods:
# - parent_count: Count parents to identify merge commits (>1 parent = merge)
# - message_patterns: Regex patterns for merge commit messages
# - git_commands: Commands to analyze merge commit structure

MERGE_COMMIT_DETECTION = {
    "parent_count_command": "git rev-list --parents -n 1 {commit_hash} | wc -w",
    "parent_threshold": 2,  # More than 2 words = merge commit (hash + parents)
    "message_patterns": [
        r"^Merge pull request #\d+",
        r"^Merge branch '.*'",
        r"^Merge remote-tracking branch",
        r"^Merge tag '.*'",
        r"^Merge commit '.*'"
    ],
    "parent_commands": {
        "get_parents": "git rev-list --parents -n 1 {commit_hash} | cut -d' ' -f2-",
        "first_parent": "git rev-parse {commit_hash}^1",
        "second_parent": "git rev-parse {commit_hash}^2",
        "merge_base": "git merge-base {commit1} {commit2}"
    }
}

# ===== REPOSITORY VALIDATION =====
#
# 📊 EXPLANATION:
# Commands to validate Git repository state and detect issues.
# Used for error handling and environment validation.

REPOSITORY_VALIDATION = {
    "is_git_repo": "git rev-parse --git-dir",
    "has_commits": "git rev-parse --verify HEAD",
    "is_clean": "git diff-index --quiet HEAD --",
    "has_staged": "git diff-index --quiet --cached HEAD --",
    "remote_exists": "git remote -v",
    "current_branch": "git rev-parse --abbrev-ref HEAD"
}

# ===== HELPER FUNCTIONS =====

def build_exclude_pathspec() -> str:
    """
    Build the complete exclude pathspec string for Git commands.
    
    Returns:
        String with all exclude patterns joined
    """
    return " ".join(EXCLUDE_PATTERNS)


def format_git_command(command_template: str, **kwargs) -> str:
    """
    Format a Git command template with provided parameters.
    
    Args:
        command_template: Template string with {placeholders}
        **kwargs: Values to substitute in placeholders
        
    Returns:
        Formatted Git command string
    """
    return command_template.format(**kwargs)


def get_log_format(format_name: str) -> str:
    """
    Get a Git log format string by name.
    
    Args:
        format_name: Name of the format (detailed, simple, etc.)
        
    Returns:
        Git log format string
    """
    return GIT_LOG_FORMATS.get(format_name, {}).get("format", "%h - %s")


def is_merge_commit_message(message: str) -> bool:
    """
    Check if a commit message indicates a merge commit.
    
    Args:
        message: Commit message to check
        
    Returns:
        True if message matches merge patterns
    """
    import re
    
    for pattern in MERGE_COMMIT_DETECTION["message_patterns"]:
        if re.match(pattern, message, re.IGNORECASE):
            return True
    return False


def get_conventional_commit_type(message: str) -> str:
    """
    Extract conventional commit type from message.
    
    Args:
        message: Commit message to analyze
        
    Returns:
        Commit type (feat, fix, etc.) or 'unknown'
    """
    import re
    
    # Match conventional commit pattern: type(scope): description
    match = re.match(r'^(\w+)(?:\([^)]+\))?\s*:\s*(.+)', message)
    if match:
        commit_type = match.group(1).lower()
        if commit_type in CONVENTIONAL_COMMIT_TYPES:
            return commit_type
    
    return 'unknown'


# ===== VALIDATION CONSTANTS =====

VALID_LOG_FORMATS = list(GIT_LOG_FORMATS.keys())
VALID_COMMIT_TYPES = list(CONVENTIONAL_COMMIT_TYPES.keys())
VALID_STATUS_COMMANDS = list(GIT_STATUS_COMMANDS.keys())
VALID_DIFF_COMMANDS = list(GIT_DIFF_COMMANDS.keys())

# ===== EXPORT ALL CONSTANTS =====

__all__ = [
    # Main constants
    "CONVENTIONAL_COMMIT_TYPES",
    "EXCLUDE_PATTERNS", 
    "GIT_COMMANDS",
    "GIT_STATUS_COMMANDS",
    "GIT_DIFF_COMMANDS",
    "GIT_LOG_FORMATS",
    "MERGE_COMMIT_DETECTION",
    "REPOSITORY_VALIDATION",
    
    # Helper functions
    "build_exclude_pathspec",
    "format_git_command",
    "get_log_format",
    "is_merge_commit_message",
    "get_conventional_commit_type",
    
    # Validation constants
    "VALID_LOG_FORMATS",
    "VALID_COMMIT_TYPES",
    "VALID_STATUS_COMMANDS", 
    "VALID_DIFF_COMMANDS"
]
