# Git Constants Documentation

## Overview

The `src/constants/git.py` module serves as the central configuration hub for all Git-related operations within the Codex-AI system. It provides standardized Git commands, conventional commit type definitions, file exclusion patterns, and utility functions for repository analysis, changelog generation, and documentation processing.

This module is essential for maintaining consistency across Git operations and ensuring proper handling of repository data throughout the system's doc-gen, doc-ui, and changelog generation features.

## Key Components

### Conventional Commit Types

The module defines a comprehensive mapping of conventional commit types following the [Conventional Commits specification](https://conventionalcommits.org). Each commit type includes:

- **Emoji**: Visual representation for reports and UI
- **Description**: Human-readable explanation of the commit type
- **Changelog Section**: Categorization for changelog generation

```python
# Example usage
from src.constants.git import CONVENTIONAL_COMMIT_TYPES

commit_type = get_conventional_commit_type("feat: add new user authentication")
print(CONVENTIONAL_COMMIT_TYPES[commit_type]["emoji"])  # ✨
print(CONVENTIONAL_COMMIT_TYPES[commit_type]["description"])  # New feature
```

### File Exclusion Patterns

Defines comprehensive patterns for excluding files from Git analysis using Git pathspec format. These patterns cover:

- Lock files (yarn.lock, package-lock.json, etc.)
- Python cache files (__pycache__, *.pyc)
- Build directories (dist, build, out)
- Log files and OS-generated files
- IDE and editor files
- Minified and temporary files

```python
# Build complete exclude pathspec
exclude_spec = build_exclude_pathspec()
# Returns: ":(exclude)yarn.lock :(exclude)package-lock.json ..."
```

### Git Command Templates

Provides organized templates for common Git operations across five categories:

1. **Log Commands**: Commit history and information retrieval
2. **Show Commands**: Detailed commit information and changes
3. **Status Commands**: Repository state analysis
4. **Diff Commands**: Change comparison between commits/branches
5. **Rev Commands**: Reference parsing and branch information

## Main Functions

### build_exclude_pathspec()

- **Purpose**: Constructs a complete exclude pathspec string for Git commands
- **Parameters**: None
- **Returns**: `str` - Space-separated exclude patterns
- **Example**:

```python
exclude_patterns = build_exclude_pathspec()
git_command = f"git log --name-only -- . {exclude_patterns}"
```

### format_git_command(command_template, **kwargs)

- **Purpose**: Formats Git command templates with provided parameters
- **Parameters**: 
  - `command_template` (str): Template string with {placeholders}
  - `**kwargs`: Values to substitute in placeholders
- **Returns**: `str` - Formatted Git command
- **Example**:

```python
template = GIT_COMMANDS["log"]["commit_history"]
command = format_git_command(template, format="%h - %s", options="--since='1 week ago'")
```

### get_log_format(format_name)

- **Purpose**: Retrieves Git log format string by name
- **Parameters**: `format_name` (str) - Format identifier (detailed, simple, oneline, structured)
- **Returns**: `str` - Git log format string
- **Example**:

```python
detailed_format = get_log_format("detailed")
# Returns: "Author: %an%nDate: %ad%nMessage: %s%n%nBody:%n%b"
```

### is_merge_commit_message(message)

- **Purpose**: Determines if a commit message indicates a merge commit
- **Parameters**: `message` (str) - Commit message to analyze
- **Returns**: `bool` - True if message matches merge patterns
- **Example**:

```python
is_merge = is_merge_commit_message("Merge pull request #123 from feature/auth")
# Returns: True
```

### get_conventional_commit_type(message)

- **Purpose**: Extracts conventional commit type from commit message
- **Parameters**: `message` (str) - Commit message to analyze
- **Returns**: `str` - Commit type or 'unknown'
- **Example**:

```python
commit_type = get_conventional_commit_type("feat(auth): add OAuth integration")
# Returns: "feat"
```

## Dependencies

### External Libraries
- **re**: Regular expression operations for pattern matching
- **typing**: Type hints (Dict, List, Any)

### Internal Dependencies
- Part of the `src.constants` package
- Used by doc-gen, doc-ui, and changelog generation modules
- Integrates with Git repository analysis components

## Configuration Constants

### Git Log Limits
Controls content generation in medium mode to balance quality with token usage:

```python
GIT_LOG_LIMITS = {
    "MEDIUM_MAX_LINES_PER_FILE": 50,
    "MEDIUM_MAX_LINE_LENGTH": 200,
    "MEDIUM_TRUNCATION_MARKER": "... [truncated]"
}
```

### Pipeline Default Branches
Defines branch priority order for pipeline mode operations:

```python
PIPELINE_DEFAULT_BRANCHES = [
    "origin/main",      # Modern default (GitHub, GitLab)
    "origin/master",    # Traditional default
    "origin/production", # Enterprise production
    "main",             # Local main
    "master",           # Local master
    "production",       # Local production
    "HEAD~1"            # Fallback
]
```

## Usage Examples

### Basic Git Command Execution

```python
from src.constants.git import GIT_COMMANDS, format_git_command, build_exclude_pathspec

# Get commit history with exclusions
exclude_spec = build_exclude_pathspec()
log_template = GIT_COMMANDS["log"]["commit_history"]
command = format_git_command(
    log_template,
    format="%h|%an|%ad|%s",
    options=f"--since='1 month ago' -- . {exclude_spec}"
)
# Result: git log --pretty=format:"%h|%an|%ad|%s" --since='1 month ago' -- . :(exclude)yarn.lock ...
```

### Commit Analysis Pipeline

```python
from src.constants.git import get_conventional_commit_type, CONVENTIONAL_COMMIT_TYPES

def analyze_commit(message):
    commit_type = get_conventional_commit_type(message)
    if commit_type != 'unknown':
        type_info = CONVENTIONAL_COMMIT_TYPES[commit_type]
        return {
            'type': commit_type,
            'emoji': type_info['emoji'],
            'section': type_info['changelog_section']
        }
    return None

# Usage
result = analyze_commit("fix(api): resolve authentication timeout issue")
# Returns: {'type': 'fix', 'emoji': '🐛', 'section': 'Bug Fixes'}
```

### Repository Validation

```python
from src.constants.git import REPOSITORY_VALIDATION
import subprocess

def validate_repository():
    """Validate Git repository state using predefined commands."""
    try:
        # Check if it's a Git repository
        subprocess.run(REPOSITORY_VALIDATION["is_git_repo"], 
                      shell=True, check=True, capture_output=True)
        
        # Check if repository has commits
        subprocess.run(REPOSITORY_VALIDATION["has_commits"], 
                      shell=True, check=True, capture_output=True)
        
        return True
    except subprocess.CalledProcessError:
        return False
```

### Merge Commit Detection

```python
from src.constants.git import MERGE_COMMIT_DETECTION, is_merge_commit_message

def is_merge_commit(commit_hash, commit_message):
    """Comprehensive merge commit detection."""
    # Check message patterns
    if is_merge_commit_message(commit_message):
        return True
    
    # Check parent count
    parent_cmd = MERGE_COMMIT_DETECTION["parent_count_command"].format(
        commit_hash=commit_hash
    )
    # Execute command and check if parent count > threshold
    # Implementation would use subprocess to execute parent_cmd
    
    return False
```

## Implementation Notes

### Design Decisions

1. **Centralized Configuration**: All Git-related constants are consolidated in a single module to ensure consistency and ease of maintenance.

2. **Template-Based Commands**: Git commands use template strings with placeholders, allowing for flexible parameter substitution while maintaining command structure.

3. **Comprehensive Exclusions**: The exclude patterns cover a wide range of file types to prevent analysis of generated, temporary, or non-essential files.

4. **Conventional Commits Support**: Full integration with the Conventional Commits specification enables automated changelog generation and commit categorization.

### Performance Considerations

- **String Operations**: Command formatting uses Python's built-in string formatting, which is efficient for the expected usage patterns.
- **Pattern Matching**: Regular expressions are compiled once and reused for commit message analysis.
- **Memory Usage**: Constants are loaded once at import time, minimizing runtime overhead.

### Known Limitations

1. **Git Version Compatibility**: Commands assume Git 2.0+ features. Older Git versions may not support all pathspec patterns.

2. **Platform Dependencies**: Some exclude patterns are OS-specific (e.g., .DS_Store for macOS).

3. **Regex Complexity**: Merge commit detection relies on message patterns that may not cover all merge commit variations.

### Future Improvements

1. **Dynamic Configuration**: Support for user-defined exclude patterns and commit types.
2. **Git Version Detection**: Automatic adaptation of commands based on installed Git version.
3. **Performance Optimization**: Caching of frequently used command strings.
4. **Extended Commit Types**: Support for custom conventional commit types beyond the standard set.

## Integration Points

### Doc-Gen Command
- Uses `GIT_DIFF_COMMANDS` for detecting changed files in pipeline mode
- Leverages `PIPELINE_DEFAULT_BRANCHES` for base branch detection
- Applies `EXCLUDE_PATTERNS` to filter relevant files

### Doc-UI Command  
- Utilizes `GIT_STATUS_COMMANDS` for local mode file detection
- Implements `GIT_DIFF_COMMANDS` for pipeline mode comparisons
- Uses `build_exclude_pathspec()` for consistent file filtering

### Changelog Generation
- Employs `CONVENTIONAL_COMMIT_TYPES` for commit categorization
- Uses `GIT_LOG_FORMATS` for structured commit information
- Applies `MERGE_COMMIT_DETECTION` for proper merge handling

## Error Handling

The module provides constants and utilities but does not implement error handling directly. Consuming modules should handle:

- **Git Command Failures**: When Git commands return non-zero exit codes
- **Repository State Issues**: When repository is not initialized or corrupted
- **Pattern Matching Failures**: When commit messages don't match expected formats

```python
# Example error handling in consuming code
try:
    command = format_git_command(template, **params)
    result = subprocess.run(command, shell=True, check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    # Handle Git command failure
    logger.error(f"Git command failed: {e}")
except KeyError as e:
    # Handle missing template parameters
    logger.error(f"Missing parameter for Git command: {e}")
```

## See Also

- [AI Constants](ai.md) - AI model and processing configurations
- [Output Constants](output.md) - Output formatting and file handling
- [Project Constants](project.md) - Project-wide configuration settings
- [Constants Package](../README.md) - Overview of all constants modules
