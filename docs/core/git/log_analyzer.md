# Git Log Analyzer Documentation

## Overview

The `log_analyzer.py` module provides comprehensive Git repository analysis capabilities for the Codex-AI project. It serves as a Python replacement for legacy shell scripts (`git_log_*.sh`), offering structured data output, improved error handling, and detailed commit analysis with special handling for merge commits.

### Key Responsibilities
- Analyze Git commits with detailed or simple output modes
- Handle merge commits and track introduced changes
- Generate structured commit data for changelog generation
- Provide tag-based analysis for release management
- Export analysis results to various output formats

### Role in Project
This module is part of the `src/core/git` directory and works alongside related components:
- `release_analyzer.py` - Release and version analysis
- `commit_parser.py` - Commit message parsing
- `tree_generator.py` - Repository tree visualization
- `changes_tracker.py` - Change tracking and diff analysis

## Main Classes and Functions

### CommitInfo (Dataclass)

A structured representation of Git commit information.

**Attributes:**
- `hash: str` - Git commit hash
- `author: str` - Commit author name
- `date: str` - Commit date
- `message: str` - Commit message (first line)
- `body: str` - Full commit body
- `is_merge: bool` - Whether this is a merge commit
- `parents: List[str]` - Parent commit hashes
- `files_changed: List[str]` - Files modified in commit
- `patch: str` - Full diff patch content

### GitLogAnalyzer (Main Class)

The primary class for Git repository analysis and log generation.

#### Constructor

```python
def __init__(self, repo_path: str = ".", output_dir: Optional[str] = None):
    """
    Initialize Git log analyzer.
    
    Args:
        repo_path: Path to Git repository (default: current directory)
        output_dir: Output directory for generated files (default: .tmp)
    """
```

#### Core Analysis Methods

##### analyze_last_commit()

```python
def analyze_last_commit(self, mode: str = 'detailed') -> CommitInfo:
    """
    Analyze the last commit (HEAD).
    
    Args:
        mode: Analysis mode ('detailed', 'medium', or 'simple')
        
    Returns:
        CommitInfo object with commit details
    """
```

**Example Usage:**
```python
analyzer = GitLogAnalyzer()
last_commit = analyzer.analyze_last_commit('detailed')
print(f"Last commit: {last_commit.hash} by {last_commit.author}")
print(f"Message: {last_commit.message}")
```

##### analyze_commit_range()

```python
def analyze_commit_range(self, since: Optional[str] = None, 
                       until: Optional[str] = None, 
                       mode: str = 'detailed') -> List[CommitInfo]:
    """
    Analyze a range of commits.
    
    Args:
        since: Start commit/tag/date (exclusive)
        until: End commit/tag/date (inclusive, default: HEAD)
        mode: Analysis mode ('detailed', 'medium', or 'simple')
        
    Returns:
        List of CommitInfo objects
    """
```

**Example Usage:**
```python
# Analyze commits since last tag
analyzer = GitLogAnalyzer()
commits = analyzer.analyze_commit_range(since="v1.0.0", mode="simple")
for commit in commits:
    print(f"{commit.hash[:8]}: {commit.message}")
```

#### Tag and Release Methods

##### get_changelog_range()

```python
def get_changelog_range(self, since_commit: Optional[str] = None) -> tuple[Optional[str], str]:
    """
    Get the correct range for changelog generation based on current context.
    
    Args:
        since_commit: Explicit since commit (overrides automatic detection)
        
    Returns:
        Tuple of (start_ref, end_ref) for git log range
    """
```

This method intelligently determines the appropriate commit range for changelog generation:
- If on a tagged commit: generates changelog FOR that tag (from previous tag to current tag)
- If not on tagged commit: generates changelog from latest tag to HEAD
- Handles first tag scenario (all history up to tag)

##### is_current_commit_tagged()

```python
def is_current_commit_tagged(self) -> Optional[str]:
    """
    Check if current commit (HEAD) has a tag.
    
    Returns:
        Tag name if current commit is tagged, None otherwise
    """
```

#### Merge Commit Handling

##### is_merge_commit()

```python
def is_merge_commit(self, commit_hash: str) -> bool:
    """
    Check if a commit is a merge commit.
    
    Args:
        commit_hash: Git commit hash
        
    Returns:
        True if commit is a merge commit
    """
```

##### get_commits_in_merge()

```python
def get_commits_in_merge(self, commit_hash: str) -> List[str]:
    """
    Get list of commits introduced by a merge.
    
    Args:
        commit_hash: Git commit hash of merge commit
        
    Returns:
        List of commit hashes introduced by the merge
    """
```

#### Output Generation Methods

##### generate_detailed_log()

```python
def generate_detailed_log(self, output_file: str, since_commit: Optional[str] = None, 
                         branch: Optional[str] = None) -> bool:
    """
    Generate detailed git log to file.
    
    Args:
        output_file: Output file path
        since_commit: Start commit/tag/date (exclusive)
        branch: Branch to analyze (default: current)
        
    Returns:
        True if successful
    """
```

##### generate_simple_log()

```python
def generate_simple_log(self, output_file: str, since_commit: Optional[str] = None, 
                       branch: Optional[str] = None) -> bool:
    """
    Generate simple git log to file.
    
    Args:
        output_file: Output file path
        since_commit: Start commit/tag/date (exclusive)
        branch: Branch to analyze (default: current)
        
    Returns:
        True if successful
    """
```

##### generate_medium_log()

```python
def generate_medium_log(self, output_file: str, since_commit: Optional[str] = None, 
                       branch: Optional[str] = None) -> bool:
    """
    Generate medium git log to file (balanced between simple and detailed).
    
    Args:
        output_file: Output file path
        since_commit: Start commit/tag/date (exclusive)
        branch: Branch to analyze (default: current)
        
    Returns:
        True if successful
    """
```

## Dependencies & Imports

### External Libraries
- `subprocess` - Git command execution
- `pathlib.Path` - File system path handling
- `dataclasses.dataclass` - Structured data representation
- `typing` - Type hints and annotations
- `datetime` - Date/time handling

### Internal Dependencies
- `constants.git.EXCLUDE_PATTERNS` - File patterns to exclude from analysis
- `constants.git.GIT_COMMANDS` - Git command configurations
- `constants.git.GIT_LOG_LIMITS` - Output formatting limits

### Git Requirements
- Git must be installed and accessible via command line
- Repository must be a valid Git repository
- Appropriate Git permissions for the target repository

## Analysis Modes

The analyzer supports three analysis modes with different levels of detail:

### Detailed Mode
- **Purpose**: Complete commit analysis with full patches
- **Output**: Full diff content, complete file changes, comprehensive commit data
- **Use Case**: Code review, detailed change analysis, debugging

### Medium Mode  
- **Purpose**: Balanced analysis with summarized patches
- **Output**: File statistics, limited diff content, truncated patches
- **Use Case**: Release notes, change summaries, moderate detail requirements
- **Limits**: 
  - Maximum 50 lines per file in diff
  - Maximum 200 characters per line
  - Truncation markers for oversized content

### Simple Mode
- **Purpose**: Basic commit information with file lists
- **Output**: Commit metadata, file change status (A/M/D/R), no patch content
- **Use Case**: Quick overviews, changelog generation, performance-sensitive operations

## Usage Examples

### Basic Commit Analysis

```python
from src.core.git.log_analyzer import GitLogAnalyzer

# Initialize analyzer
analyzer = GitLogAnalyzer(repo_path="/path/to/repo")

# Analyze last commit
last_commit = analyzer.analyze_last_commit('simple')
print(f"Last commit: {last_commit.message}")
print(f"Files changed: {len(last_commit.files_changed)}")
```

### Range Analysis for Changelog

```python
# Get appropriate range for changelog
start_ref, end_ref = analyzer.get_changelog_range()
print(f"Analyzing range: {start_ref}..{end_ref}")

# Analyze the range
commits = analyzer.analyze_commit_range(since=start_ref, until=end_ref, mode='medium')
print(f"Found {len(commits)} commits")

for commit in commits:
    print(f"- {commit.message} ({commit.author})")
```

### Merge Commit Analysis

```python
# Check if commit is a merge
commit_hash = "abc123def456"
if analyzer.is_merge_commit(commit_hash):
    # Get commits introduced by merge
    introduced = analyzer.get_commits_in_merge(commit_hash)
    print(f"Merge introduces {len(introduced)} commits:")
    
    for intro_commit in introduced:
        commit_info = analyzer._analyze_commit(intro_commit, 'simple')
        print(f"  - {commit_info.message}")
```

### Output Generation

```python
# Generate detailed log file
success = analyzer.generate_detailed_log(
    output_file="detailed_changes.txt",
    since_commit="v1.0.0"
)

if success:
    print("Detailed log generated successfully")

# Generate simple log for quick review
analyzer.generate_simple_log(
    output_file="simple_changes.txt", 
    since_commit="v1.0.0"
)
```

### Convenience Functions

```python
from src.core.git.log_analyzer import analyze_last_commit_detailed, analyze_last_commit_simple

# Quick analysis with default settings
detailed_file = analyze_last_commit_detailed()  # Saves to .tmp/git_log_detailed.txt
simple_file = analyze_last_commit_simple()      # Saves to .tmp/git_log_simple.txt

print(f"Analysis saved to: {detailed_file}")
```

## Output Format

### Commit Output Structure

The `format_commit_output()` method generates structured output:

```
COMMIT: abc123de | John Doe | 2024-01-15 10:30:00
  Add new feature for user authentication
  Body: Implements OAuth2 integration with Google and GitHub providers
  Files:
    M    src/auth/oauth.py
    A    src/auth/providers.py
    M    tests/test_auth.py
--------------------
```

### Merge Commit Output

```
MERGE: def456gh | Jane Smith | 2024-01-15 11:45:00
  Merge pull request #123 from feature/oauth
  
New Commits Introduced by This Merge:

COMMIT: abc123de | John Doe | 2024-01-15 10:30:00
  Add OAuth2 authentication
  Files:
    A    src/auth/oauth.py
--------------------
```

## Implementation Notes

### Performance Considerations

1. **Git Command Optimization**: Uses efficient Git commands with appropriate flags
2. **Memory Management**: Processes commits individually to avoid loading entire history
3. **File Exclusion**: Leverages Git pathspec for efficient file filtering
4. **Caching**: No internal caching - relies on Git's native performance

### Error Handling

- **Git Command Failures**: Wrapped in try-catch with meaningful error messages
- **Malformed Commits**: Graceful fallbacks for corrupted or incomplete commit data
- **Missing Dependencies**: Clear error messages for Git availability issues
- **Permission Issues**: Handles repository access problems

### Design Decisions

1. **Dataclass Usage**: Structured data representation for type safety and clarity
2. **Mode-Based Analysis**: Flexible output levels to balance detail vs. performance
3. **Merge Commit Special Handling**: Recognizes merge commits require different analysis
4. **Path Exclusion**: Configurable file exclusion for focused analysis

### Known Limitations

1. **Large Repositories**: Performance may degrade with very large commit ranges
2. **Binary Files**: Limited handling of binary file changes in patches
3. **Complex Merges**: Octopus merges (>2 parents) have simplified handling
4. **Git Version**: Requires modern Git version for all features

### Future Improvement Opportunities

1. **Caching Layer**: Add commit analysis caching for repeated operations
2. **Parallel Processing**: Multi-threaded analysis for large commit ranges
3. **Binary Diff Support**: Enhanced binary file change detection
4. **Custom Formatters**: Pluggable output formatters for different use cases
5. **Incremental Analysis**: Smart detection of already-analyzed commits

## Configuration

### Environment Variables

The analyzer respects standard Git environment variables:
- `GIT_DIR` - Git directory location
- `GIT_WORK_TREE` - Working tree location
- `GIT_CONFIG` - Git configuration file

### Constants Configuration

Behavior is controlled through `constants.git` module:

```python
# Example constants usage
EXCLUDE_PATTERNS = [
    "*.log",
    "node_modules/*",
    ".tmp/*"
]

GIT_LOG_LIMITS = {
    "MEDIUM_MAX_LINES_PER_FILE": 50,
    "MEDIUM_MAX_LINE_LENGTH": 200,
    "MEDIUM_TRUNCATION_MARKER": "..."
}
```

## Error Scenarios and Handling

### Common Error Cases

1. **Repository Not Found**
   ```python
   try:
       analyzer = GitLogAnalyzer("/invalid/path")
       commits = analyzer.analyze_last_commit()
   except RuntimeError as e:
       print(f"Git error: {e}")
   ```

2. **Invalid Commit Hash**
   ```python
   try:
       commit_info = analyzer._analyze_commit("invalid_hash")
   except RuntimeError:
       # Returns fallback CommitInfo with error message
       pass
   ```

3. **Permission Issues**
   - Graceful degradation with error messages
   - Fallback to available information
   - Clear user feedback

## Testing Considerations

### Unit Testing Approach
- Mock Git commands for consistent test environments
- Test with various commit types (regular, merge, initial)
- Validate output formatting across all modes
- Test error handling scenarios

### Integration Testing
- Test with real Git repositories
- Validate against known commit histories
- Performance testing with large repositories
- Cross-platform compatibility testing

## See Also

- [Release Analyzer](release_analyzer.md) - Release and version analysis
- [Commit Parser](commit_parser.md) - Commit message parsing utilities  
- [Changes Tracker](changes_tracker.md) - Change tracking and diff analysis
- [Tree Generator](tree_generator.md) - Repository tree visualization
- [Git Module Overview](README.md) - Complete git module documentation
