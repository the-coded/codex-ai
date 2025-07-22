# Git Changes Tracker Documentation

## Overview

The `changes_tracker.py` module provides comprehensive Git repository change tracking and analysis capabilities for the Codex-AI project. It serves as the core component for monitoring file modifications, repository state analysis, and development workflow automation within the `src/core/git` directory.

### Key Responsibilities
- Track staged, modified, untracked, and ignored files in Git repositories
- Analyze changes between commits, branches, and time periods
- Provide repository state information including branch status and commit details
- Support intelligent file detection for documentation generation workflows
- Offer change pattern analysis and development trend insights

## Main Classes and Components

### ChangeType (Enum)
Enumeration of Git change types with standard Git status codes:
- `ADDED` ("A") - New files added to repository
- `MODIFIED` ("M") - Existing files with modifications
- `DELETED` ("D") - Files removed from repository
- `RENAMED` ("R") - Files moved or renamed
- `COPIED` ("C") - Files copied to new locations
- `UNMERGED` ("U") - Files with merge conflicts
- `UNTRACKED` ("??") - Files not tracked by Git
- `IGNORED` ("!!") - Files ignored by Git

### FileStatus (Enum)
Enumeration of Git file status states:
- `STAGED` - Changes staged for commit
- `MODIFIED` - Working directory modifications
- `UNTRACKED` - Files not under version control
- `IGNORED` - Files excluded by .gitignore
- `CLEAN` - No changes detected

### FileChange (Dataclass)
Represents a single file change with comprehensive metadata:

```python
@dataclass
class FileChange:
    path: str                    # File path
    change_type: ChangeType      # Type of change
    status: FileStatus           # Current status
    old_path: Optional[str]      # Original path for renames/copies
    similarity: Optional[int]    # Similarity percentage (0-100)
```

**Properties:**
- `is_added`, `is_modified`, `is_deleted`, `is_renamed` - Change type checks
- `is_staged`, `is_untracked` - Status checks

### RepositoryState (Dataclass)
Comprehensive repository state information:

```python
@dataclass
class RepositoryState:
    staged_changes: List[FileChange]      # Staged modifications
    modified_changes: List[FileChange]    # Working directory changes
    untracked_files: List[FileChange]     # Untracked files
    ignored_files: List[FileChange]       # Ignored files
    clean: bool                           # Repository clean status
    branch: Optional[str]                 # Current branch name
    commit_hash: Optional[str]            # Current commit SHA
    ahead_behind: Optional[Tuple[int, int]]  # Commits ahead/behind upstream
```

**Properties:**
- `has_changes` - True if any changes exist
- `total_changes` - Count of all changes
- `is_dirty` - True if working directory has modifications

### ChangesTracker (Main Class)
Core class for Git repository change tracking and analysis.

#### Constructor
```python
def __init__(self, repo_path: str = "."):
    """Initialize changes tracker for specified repository path."""
```

#### Key Methods

##### get_repository_state() → RepositoryState
Returns complete current repository state including all change types, branch information, and commit details.

```python
tracker = ChangesTracker("/path/to/repo")
state = tracker.get_repository_state()

print(f"Branch: {state.branch}")
print(f"Total changes: {state.total_changes}")
print(f"Clean: {state.clean}")
```

##### get_changes_since_commit(commit: str) → List[FileChange]
Retrieves all changes since a specific commit reference.

```python
# Get changes since last release
changes = tracker.get_changes_since_commit("v1.0.0")
for change in changes:
    print(f"{change.change_type.value}: {change.path}")
```

##### get_changes_between_commits(from_commit: str, to_commit: str) → List[FileChange]
Analyzes changes between two specific commits.

```python
# Compare two releases
changes = tracker.get_changes_between_commits("v1.0.0", "v1.1.0")
added_files = [c for c in changes if c.is_added]
```

##### get_changes_in_branch(branch: str, base_branch: str = "main") → List[FileChange]
Gets changes in a feature branch compared to base branch.

```python
# Analyze feature branch changes
changes = tracker.get_changes_in_branch("feature/new-api", "main")
```

##### get_file_history(file_path: str, max_commits: int = 10) → List[Dict[str, Any]]
Retrieves commit history for a specific file.

```python
history = tracker.get_file_history("src/main.py", max_commits=5)
for commit in history:
    print(f"{commit['commit']}: {commit['message']}")
```

##### Utility Methods
- `is_file_tracked(file_path: str) → bool` - Check if file is under Git control
- `is_file_ignored(file_path: str) → bool` - Check if file is ignored
- `get_conflicted_files() → List[str]` - Get files with merge conflicts

### ChangeAnalyzer
Advanced analysis class for change patterns and development statistics.

```python
analyzer = ChangeAnalyzer("/path/to/repo")
analysis = analyzer.analyze_repository_state()

print(f"File types changed: {analysis['file_types']}")
print(f"Change distribution: {analysis['change_types']}")
```

### FileDetector
Intelligent file detection for documentation generation workflows.

#### Key Methods

##### auto_detect_mode() → str
Automatically determines whether to use "local" (staged/modified files) or "pipeline" (branch comparison) mode.

```python
detector = FileDetector()
mode = detector.auto_detect_mode()  # Returns "local" or "pipeline"
```

##### get_files_for_mode(mode: str, since_commit: Optional[str] = None) → List[str]
Retrieves files based on detection mode for documentation generation.

```python
# Get files for local changes
files = detector.get_files_for_mode("local")

# Get files changed since specific commit
files = detector.get_files_for_mode("pipeline", since_commit="main")
```

##### get_files_for_path(path: str, shallow: bool = False) → List[str]
Gets all relevant files in a specified directory path.

```python
# Recursive file discovery
files = detector.get_files_for_path("src/", shallow=False)

# Shallow (single directory level)
files = detector.get_files_for_path("src/", shallow=True)
```

## Dependencies & Imports

### External Dependencies
- `subprocess` - Git command execution
- `pathlib.Path` - File system path handling
- `dataclasses` - Data structure definitions
- `typing` - Type hints and annotations
- `enum.Enum` - Enumeration types
- `datetime` - Timestamp handling

### Internal Dependencies
- `constants.git` - Git-related constants and configuration
  - `EXCLUDE_PATTERNS` - File patterns to exclude from tracking
  - `GIT_STATUS_COMMANDS` - Standard Git status commands
  - `GIT_DIFF_COMMANDS` - Git diff command configurations
  - `PIPELINE_DEFAULT_BRANCHES` - Default branches for pipeline mode

## Usage Examples

### Basic Repository Analysis

```python
from src.core.git.changes_tracker import ChangesTracker, get_repository_state

# Quick repository state check
state = get_repository_state()
if state.has_changes:
    print(f"Repository has {state.total_changes} changes")
    print(f"Staged: {len(state.staged_changes)}")
    print(f"Modified: {len(state.modified_changes)}")
    print(f"Untracked: {len(state.untracked_files)}")
```

### Change Analysis Workflow

```python
from src.core.git.changes_tracker import ChangesTracker, ChangeAnalyzer

# Initialize tracker and analyzer
tracker = ChangesTracker()
analyzer = ChangeAnalyzer()

# Get changes since last release
changes = tracker.get_changes_since_commit("v1.0.0")

# Analyze change patterns
analysis = analyzer.analyze_changes_since_commit("v1.0.0")
print(f"Total files changed: {analysis['total_changes']}")
print(f"Added: {analysis['added_files']}")
print(f"Modified: {analysis['modified_files']}")
print(f"File types: {analysis['file_types']}")
```

### Documentation Generation Integration

```python
from src.core.git.changes_tracker import FileDetector, auto_detect_mode

# Auto-detect appropriate mode
mode = auto_detect_mode()
print(f"Using {mode} mode for file detection")

# Get files for documentation generation
detector = FileDetector()
files = detector.get_files_for_mode(mode)

# Process each file for documentation
for file_path in files:
    print(f"Processing: {file_path}")
    # Generate documentation for file...
```

### Branch Comparison

```python
# Compare feature branch with main
tracker = ChangesTracker()
changes = tracker.get_changes_in_branch("feature/api-update", "main")

# Categorize changes
new_files = [c for c in changes if c.is_added]
modified_files = [c for c in changes if c.is_modified]
renamed_files = [c for c in changes if c.is_renamed]

print(f"New files: {len(new_files)}")
print(f"Modified files: {len(modified_files)}")
print(f"Renamed files: {len(renamed_files)}")
```

### Error Handling

```python
try:
    tracker = ChangesTracker("/path/to/repo")
    state = tracker.get_repository_state()
except RuntimeError as e:
    if "HEAD does not point to a branch" in str(e):
        print("Repository is in detached HEAD state")
        # Handle detached HEAD scenario
    else:
        print(f"Git operation failed: {e}")
```

## Implementation Notes

### Design Decisions

**Dataclass Usage**: Extensive use of dataclasses for clean, type-safe data structures that are easy to serialize and debug.

**Enum-based Status Tracking**: Uses enums for change types and file status to ensure type safety and prevent invalid state combinations.

**Subprocess Integration**: Direct Git command execution via subprocess for maximum compatibility and feature access.

**Flexible Path Handling**: Supports both absolute and relative repository paths with pathlib for cross-platform compatibility.

### Performance Considerations

**Command Batching**: Git commands are batched where possible to reduce subprocess overhead.

**Lazy Evaluation**: Repository state components are computed on-demand to avoid unnecessary Git operations.

**Pattern Exclusion**: File exclusion patterns are applied early to reduce processing overhead for large repositories.

**Caching Strategy**: Consider implementing caching for frequently accessed repository information in high-frequency usage scenarios.

### Error Handling

**Graceful Degradation**: Methods return empty lists or None values when Git operations fail, allowing applications to continue functioning.

**Detached HEAD Support**: Special handling for detached HEAD states common in CI/CD environments.

**Permission Handling**: Robust handling of permission errors when accessing repository files.

### Known Limitations

**Large Repository Performance**: Performance may degrade with very large repositories (>10k files). Consider implementing pagination for such cases.

**Binary File Detection**: Currently treats all files equally; binary file detection could improve performance.

**Network Operations**: No support for remote repository operations; focuses on local Git state only.

**Submodule Support**: Limited submodule support; submodule changes are not deeply analyzed.

### Future Improvement Opportunities

**Async Operations**: Implement async versions of Git operations for better performance in concurrent scenarios.

**Caching Layer**: Add intelligent caching for repository state to reduce Git command overhead.

**Plugin Architecture**: Extensible plugin system for custom change analysis and file detection rules.

**Performance Metrics**: Built-in performance monitoring and optimization suggestions.

**Remote Integration**: Support for remote repository analysis and comparison operations.

## Integration with Related Components

### log_analyzer.py
The changes tracker provides input data for log analysis by identifying which files have been modified and need log analysis.

### release_analyzer.py
Repository state and change information feeds into release analysis for determining release scope and impact.

### commit_parser.py
File change information complements commit message parsing for comprehensive change understanding.

### tree_generator.py
File detection capabilities support tree generation by identifying relevant files for documentation structure.

## Configuration

The module relies on constants defined in `constants.git`:

- **EXCLUDE_PATTERNS**: File patterns to exclude from change tracking
- **PIPELINE_DEFAULT_BRANCHES**: Default branches to compare against in pipeline mode
- **GIT_STATUS_COMMANDS**: Standard Git commands for status operations
- **GIT_DIFF_COMMANDS**: Git diff command configurations

## See Also

- [Git Log Analyzer](log_analyzer.md) - Analyze Git commit logs and history
- [Release Analyzer](release_analyzer.md) - Release planning and analysis
- [Commit Parser](commit_parser.md) - Parse and analyze commit messages
- [Tree Generator](tree_generator.md) - Generate project structure documentation
- [Git Module Overview](README.md) - Overview of the Git core module
