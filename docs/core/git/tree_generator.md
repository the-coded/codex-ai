# Git Tree Generator Documentation

## Overview

The `tree_generator.py` module provides a comprehensive Python implementation for generating JSON tree structures from Git repositories. This module replaces the functionality of legacy shell scripts (`tree_*.sh`) with improved error handling, structured data output, and a unified API for all tree generation operations.

**Key Purpose**: Generate hierarchical JSON representations of project files, Git changes, and related file structures for analysis and visualization.

**Role in Project**: Core component of the Git analysis system, providing structured data for other modules like `log_analyzer.py`, `release_analyzer.py`, and `changes_tracker.py`.

## Main Classes and Functions

### GitTreeGenerator Class

The primary class that handles all tree generation operations.

**Constructor**:
```python
GitTreeGenerator(repo_path: str = ".", output_dir: Optional[str] = None)
```

- **repo_path**: Path to Git repository (default: current directory)
- **output_dir**: Output directory for generated files (default: `.tmp`)

### Core Generation Methods

#### generate_project_tree()
- **Purpose**: Creates complete project structure tree
- **Parameters**: `start_path: Optional[str] = None`
- **Returns**: `TreeGenerationResult`
- **Equivalent**: Replaces `tree_project.sh`

```python
generator = GitTreeGenerator()
result = generator.generate_project_tree()
if result.success:
    print(f"Generated tree with {result.file_count} files at {result.output_file}")
```

#### generate_git_changes_trees()
- **Purpose**: Generates trees for Git changes (changed, removed, all)
- **Returns**: `List[TreeGenerationResult]`
- **Equivalent**: Replaces `tree_git_changes.sh`

```python
results = generator.generate_git_changes_trees()
for result in results:
    print(f"{result.tree_type}: {result.file_count} files")
```

#### generate_release_changes_trees()
- **Purpose**: Generates trees for changes between releases
- **Returns**: `List[TreeGenerationResult]`
- **Equivalent**: Replaces `tree_git_release_changes.sh`

#### generate_siblings_tree()
- **Purpose**: Creates tree of sibling files for changed files
- **Returns**: `TreeGenerationResult`
- **Equivalent**: Replaces `tree_git_siblings.sh`

#### generate_all_trees()
- **Purpose**: Generates all tree structures in one operation
- **Returns**: `List[TreeGenerationResult]`
- **Equivalent**: Replaces `tree_generate_all.sh`

### TreeGenerationResult Dataclass

Represents the result of a tree generation operation:

```python
@dataclass
class TreeGenerationResult:
    tree_type: str
    output_file: str
    file_count: int
    success: bool
    error_message: Optional[str] = None
    generation_time: Optional[float] = None
```

## Configuration Constants

### Tree Output Types

The module supports multiple tree types defined in `TREE_OUTPUTS`:

- **project**: Complete project structure
- **git_changed**: Files changed in last commit
- **git_removed**: Files removed in last commit
- **git_all**: All git changes (changed + removed)
- **release_changed**: Files changed between releases
- **release_removed**: Files removed between releases
- **release_all**: All release changes
- **git_siblings**: Sibling files of changed files

### Exclusion Patterns

Directories excluded from tree generation:

```python
TREE_EXCLUDE_DIRECTORIES = [
    "dist", "node_modules", "venv", "examples", ".git",
    ".vscode", ".tmp", ".github", "__pycache__", ".idea",
    ".next", ".nuxt", "build", "out", "coverage"
]
```

## Dependencies & Imports

### External Libraries
- `json`: JSON serialization
- `os`: Operating system interface
- `subprocess`: Process management for Git commands
- `pathlib.Path`: Modern path handling
- `datetime`: Timestamp generation
- `re`: Regular expression matching

### Internal Dependencies
- `constants.git.EXCLUDE_PATTERNS`: Git exclusion patterns
- Related modules: `log_analyzer.py`, `release_analyzer.py`, `changes_tracker.py`

### System Requirements
- Git repository (for Git-related operations)
- Python 3.7+ (uses dataclasses and pathlib)
- Read/write permissions for output directory

## API Documentation

### Public Functions

#### generate_project_tree()
Convenience function for simple project tree generation:

```python
def generate_project_tree(start_path: str = ".", 
                         output_file: str = ".tmp/tree_project.json") -> str
```

**Returns**: Output file path or empty string on failure

#### generate_git_changes_trees()
Convenience function for Git changes:

```python
def generate_git_changes_trees() -> List[str]
```

**Returns**: List of output file paths for successful generations

#### generate_all_trees()
Convenience function for all tree types:

```python
def generate_all_trees() -> List[str]
```

**Returns**: List of all successfully generated file paths

### Helper Functions

#### is_tree_excluded_directory()
```python
def is_tree_excluded_directory(dirname: str) -> bool
```

Checks if a directory should be excluded from tree generation.

#### validate_file_path()
```python
def validate_file_path(filepath: str) -> bool
```

Validates file paths for security and compatibility.

## Usage Examples

### Basic Project Tree Generation

```python
from src.core.git.tree_generator import GitTreeGenerator

# Initialize generator
generator = GitTreeGenerator(repo_path="/path/to/repo", output_dir=".output")

# Generate project tree
result = generator.generate_project_tree()

if result.success:
    print(f"Project tree generated: {result.output_file}")
    print(f"Total files: {result.file_count}")
    print(f"Generation time: {result.generation_time:.2f}s")
else:
    print(f"Error: {result.error_message}")
```

### Git Changes Analysis

```python
# Generate all Git change trees
results = generator.generate_git_changes_trees()

for result in results:
    if result.success:
        print(f"{result.tree_type}: {result.file_count} files")
        
        # Load and examine the tree
        import json
        with open(result.output_file, 'r') as f:
            tree_data = json.load(f)
            # Process tree data...
```

### Complete Analysis Workflow

```python
# Generate all trees and get summary
generator = GitTreeGenerator()
all_results = generator.generate_all_trees()
summary = generator.get_generation_summary(all_results)

print(f"Generated {summary['successful']}/{summary['total_trees']} trees")
print(f"Total files analyzed: {summary['total_files']}")
print(f"Output directory: {summary['output_directory']}")

# Access specific tree files
if 'git_changed' in summary['generated_files']:
    changed_file = summary['generated_files']['git_changed']
    # Process changed files...
```

### Error Handling

```python
try:
    generator = GitTreeGenerator("/invalid/path")
    results = generator.generate_all_trees()
    
    # Check for errors
    failed_results = [r for r in results if not r.success]
    if failed_results:
        for result in failed_results:
            print(f"Failed {result.tree_type}: {result.error_message}")
            
except Exception as e:
    print(f"Initialization error: {e}")
```

## Tree Structure Format

Generated JSON trees follow this hierarchical structure:

```json
{
  "subdirectory": {
    "files": ["file1.py", "file2.py"],
    "nested_dir": {
      "files": ["nested_file.js"]
    }
  },
  "files": ["root_file.md"]
}
```

### Key Structure Rules
- **files**: Array containing filenames in current directory
- **Directory names**: Keys representing subdirectories
- **Sorting**: All arrays and keys are sorted alphabetically
- **Relative paths**: All paths are relative to repository root

## Implementation Notes

### Design Decisions

1. **Python over Shell Scripts**: Provides better error handling, structured data, and cross-platform compatibility
2. **Dataclass Results**: Structured return values with comprehensive metadata
3. **Unified API**: Single class handles all tree generation types
4. **JSON Output**: Standardized format for easy consumption by other tools

### Performance Considerations

- **Lazy Loading**: Trees are generated on-demand
- **Memory Efficient**: Processes files incrementally rather than loading all into memory
- **Git Command Optimization**: Minimizes Git subprocess calls
- **Path Validation**: Early validation prevents processing invalid paths

### Git Integration

The module integrates deeply with Git through subprocess calls:

```python
# Example Git commands used internally
git show --name-status --format= HEAD           # Last commit changes
git describe --tags --abbrev=0                  # Current tag
git diff --name-status tag1..tag2               # Release changes
```

### Error Handling Strategy

1. **Graceful Degradation**: Continues processing even if some operations fail
2. **Detailed Error Messages**: Provides specific error information
3. **Validation**: Input validation prevents common errors
4. **Recovery**: Attempts alternative approaches when possible

### Known Limitations

1. **Large Repositories**: Performance may degrade with very large repositories
2. **Git Dependency**: Requires Git to be installed and accessible
3. **File System Permissions**: Requires read access to repository and write access to output directory
4. **Memory Usage**: Large trees may consume significant memory during generation

### Future Improvement Opportunities

1. **Streaming Output**: For very large trees, implement streaming JSON generation
2. **Caching**: Cache intermediate results for repeated operations
3. **Parallel Processing**: Generate multiple trees concurrently
4. **Configuration Files**: Support external configuration for exclusion patterns
5. **Progress Reporting**: Add progress callbacks for long-running operations

## Integration with Related Modules

### With log_analyzer.py
```python
# Tree generator provides file lists for log analysis
from src.core.git.tree_generator import GitTreeGenerator
from src.core.git.log_analyzer import LogAnalyzer

generator = GitTreeGenerator()
results = generator.generate_git_changes_trees()

# Use changed files for targeted log analysis
changed_result = next(r for r in results if r.tree_type == "git_changed")
if changed_result.success:
    analyzer = LogAnalyzer()
    # Analyze logs for changed files...
```

### With release_analyzer.py
```python
# Release trees provide context for release analysis
release_results = generator.generate_release_changes_trees()
# Feed release changes to release analyzer...
```

### With changes_tracker.py
```python
# Sibling trees help track related file changes
siblings_result = generator.generate_siblings_tree()
# Use sibling information for change impact analysis...
```

## Testing Considerations

### Unit Testing
- Mock Git commands for consistent testing
- Test with various repository states (empty, single commit, multiple releases)
- Validate JSON output structure and content
- Test error conditions and edge cases

### Integration Testing
- Test with real Git repositories
- Verify output file generation and cleanup
- Test cross-platform compatibility
- Performance testing with large repositories

### Example Test Structure
```python
import unittest
from unittest.mock import patch, MagicMock
from src.core.git.tree_generator import GitTreeGenerator

class TestGitTreeGenerator(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_git_changes_parsing(self, mock_run):
        mock_run.return_value.stdout = "M\tfile1.py\nA\tfile2.py\nD\tfile3.py"
        
        generator = GitTreeGenerator()
        changed, removed = generator._get_git_changes()
        
        self.assertIn("file1.py", changed)
        self.assertIn("file2.py", changed)
        self.assertIn("file3.py", removed)
```

## See Also

- [Git Log Analyzer](log_analyzer.md) - Analyzes Git commit logs
- [Release Analyzer](release_analyzer.md) - Analyzes release patterns
- [Changes Tracker](changes_tracker.md) - Tracks file change patterns
- [Git Constants](../../constants/git.md) - Git-related configuration constants
- [Core Git Module](README.md) - Overview of the Git analysis system
