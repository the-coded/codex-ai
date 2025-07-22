# Git Core Module

## Overview

The `src/core/git` module provides comprehensive Git repository analysis and manipulation capabilities for Codex-AI. This module serves as the foundation for Git-based operations throughout the project, offering structured interfaces for commit analysis, change tracking, release management, and repository tree generation.

The module abstracts Git operations into Python classes and functions, providing consistent error handling, structured data output, and integration with the project's constants and configuration systems.

## Contents

- **commit_parser.py**: Parses Git commit messages according to Conventional Commits specification, extracting structured information including commit types, scopes, breaking changes, and issue references
- **log_analyzer.py**: Analyzes Git commit history with detailed or simple output modes, handling merge commits and providing formatted changelog generation
- **release_analyzer.py**: Compares changes between Git tags/releases, generating detailed analysis of commits, diffs, and file changes between versions
- **tree_generator.py**: Generates JSON tree structures representing project files, Git changes, and sibling files for development workflow automation
- **changes_tracker.py**: Tracks and analyzes Git repository state including staged changes, modifications, untracked files, and file history

## Architecture

### Core Components

The module follows a layered architecture with three main patterns:

1. **Analyzers**: High-level classes that provide comprehensive analysis (`GitLogAnalyzer`, `GitReleaseAnalyzer`, `CommitAnalyzer`)
2. **Trackers**: State-focused classes that monitor repository changes (`ChangesTracker`, `FileDetector`)
3. **Generators**: Output-focused classes that create structured data (`GitTreeGenerator`, `CommitParser`)

### Data Flow

```text
Git Repository
     ↓
ChangesTracker → Repository State
     ↓
CommitParser → Structured Commits
     ↓
LogAnalyzer/ReleaseAnalyzer → Formatted Analysis
     ↓
TreeGenerator → JSON Structures
```

### Key Abstractions

- **ParsedCommit**: Structured representation of commit messages with conventional commit support
- **RepositoryState**: Complete snapshot of repository status including all change types
- **FileChange**: Individual file modification with change type and status information
- **TreeGenerationResult**: Outcome of tree generation operations with metadata

### Dependencies

The module integrates with:
- `constants.git`: Git-related constants, patterns, and configuration
- Standard subprocess module for Git command execution
- Pathlib for cross-platform file path handling
- Dataclasses for structured data representation

## Usage

### Basic Repository Analysis

```python
from src.core.git.changes_tracker import ChangesTracker

# Get current repository state
tracker = ChangesTracker()
state = tracker.get_repository_state()

print(f"Branch: {state.branch}")
print(f"Total changes: {state.total_changes}")
print(f"Staged files: {len(state.staged_changes)}")
```

### Commit Message Parsing

```python
from src.core.git.commit_parser import CommitParser

parser = CommitParser()
commit = parser.parse("feat(api): add user authentication\n\nImplements OAuth2 flow")

print(f"Type: {commit.type.value}")
print(f"Scope: {commit.scope}")
print(f"Is feature: {commit.is_feature}")
```

### Release Analysis

```python
from src.core.git.release_analyzer import GitReleaseAnalyzer

analyzer = GitReleaseAnalyzer()
comparison = analyzer.analyze_current_release('detailed')

if comparison:
    print(f"Current: {comparison.current_release.tag}")
    print(f"Commits: {len(comparison.commits)}")
```

### Tree Generation

```python
from src.core.git.tree_generator import GitTreeGenerator

generator = GitTreeGenerator()
results = generator.generate_all_trees()

for result in results:
    if result.success:
        print(f"{result.tree_type}: {result.file_count} files")
```

### File Detection and Mode Analysis

```python
from src.core.git.changes_tracker import FileDetector

detector = FileDetector()
mode = detector.auto_detect_mode()  # "local" or "pipeline"
files = detector.get_files_for_mode(mode)

print(f"Mode: {mode}")
print(f"Files to process: {len(files)}")
```

## Implementation Details

### Error Handling

All modules implement consistent error handling patterns:
- Git command failures raise `RuntimeError` with descriptive messages
- Invalid inputs return empty results or None rather than exceptions
- File operations include proper encoding and path validation

### Performance Considerations

- Git commands are executed with minimal overhead using subprocess
- Large diffs and logs can be truncated based on configurable limits
- Tree generation uses efficient path splitting and deduplication

### Output Formats

The module supports multiple output formats:
- **Detailed**: Full patches, complete commit information, comprehensive diffs
- **Simple**: File lists, basic commit info, summary statistics
- **Medium**: Balanced output with truncated patches and file statistics
- **JSON**: Structured data for programmatic consumption

### Configuration Integration

All components respect configuration from `constants.git`:
- File exclusion patterns for analysis
- Git command templates and options
- Output formatting preferences
- Pipeline and branch detection settings

### Extensibility

The module is designed for extension:
- Abstract base patterns for new analyzers
- Pluggable commit message parsers
- Configurable tree generation rules
- Extensible file detection modes

## Common Patterns

### Convenience Functions

Each module provides convenience functions for common operations:

```python
# Direct functions for simple use cases
from src.core.git.commit_parser import parse_commit
from src.core.git.changes_tracker import get_repository_state
from src.core.git.log_analyzer import analyze_last_commit_detailed

commit = parse_commit("fix: resolve authentication bug")
state = get_repository_state()
log_file = analyze_last_commit_detailed()
```

### Class-Based APIs

For advanced usage, instantiate classes directly:

```python
# Full control with class instances
analyzer = GitLogAnalyzer(repo_path="/path/to/repo", output_dir="/custom/output")
commits = analyzer.analyze_commit_range(since="v1.0.0", until="v2.0.0")
```

### Integration with Project Workflows

The module integrates seamlessly with project automation:
- Tree generation for documentation workflows
- Change detection for CI/CD pipelines  
- Release analysis for changelog generation
- Commit parsing for automated categorization

This module serves as the Git foundation for Codex-AI's development and documentation automation systems, providing reliable, structured access to repository information and change analysis.
