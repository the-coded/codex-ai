# Commit Parser Documentation

## Overview

The `commit_parser.py` module provides comprehensive parsing and analysis capabilities for Git commit messages, with specialized support for Conventional Commits specification. This module is part of the `src/core/git` directory and serves as a foundational component for commit analysis, release generation, and project reporting within the Codex-AI system.

The module extracts structured information from commit messages, enabling automated analysis of development patterns, breaking changes detection, and semantic versioning support.

## Main Classes and Components

### CommitType (Enum)

Enumeration of conventional commit types following the Conventional Commits specification.

**Available Types:**
- `FEAT`: New features
- `FIX`: Bug fixes
- `DOCS`: Documentation changes
- `STYLE`: Code style changes (formatting, missing semicolons, etc.)
- `REFACTOR`: Code refactoring without feature changes
- `PERF`: Performance improvements
- `TEST`: Test additions or modifications
- `BUILD`: Build system or external dependency changes
- `CI`: Continuous integration configuration changes
- `CHORE`: Maintenance tasks
- `REVERT`: Commit reverts
- `OTHER`: Unclassified commits

### CommitScope (Enum)

Enumeration of common commit scopes for categorizing changes.

**Available Scopes:**
- `API`: API-related changes
- `UI`: User interface changes
- `CORE`: Core functionality changes
- `DOCS`: Documentation scope
- `TESTS`: Test-related changes
- `CONFIG`: Configuration changes
- `DEPS`: Dependency updates
- `SECURITY`: Security-related changes
- `OTHER`: Unclassified scope

### ParsedCommit (Dataclass)

Represents a parsed commit message with structured information extracted from the raw commit text.

**Properties:**
- `raw_message`: Original commit message
- `type`: Commit type (CommitType enum)
- `scope`: Optional scope string
- `description`: Commit description/summary
- `body`: Optional commit body
- `footer`: Optional commit footer
- `breaking_change`: Boolean indicating breaking changes
- `is_conventional`: Boolean indicating conventional commit format
- `issues`: List of referenced issue numbers
- `co_authors`: List of co-author information

**Convenience Properties:**
- `is_feature`: Returns True for feature commits
- `is_bugfix`: Returns True for bug fix commits
- `is_breaking`: Returns True for breaking changes
- `is_documentation`: Returns True for documentation commits
- `formatted_type`: Returns formatted type string for display

### CommitParser

Main parser class that handles the parsing logic for Git commit messages.

#### Key Methods

##### `parse(commit_message: str) -> ParsedCommit`

Parses a single commit message into structured information.

**Parameters:**
- `commit_message`: Raw commit message string to parse

**Returns:**
- `ParsedCommit` object with extracted information

**Example:**
```python
parser = CommitParser()
commit = parser.parse("feat(api): add user authentication endpoint")

print(commit.type)  # CommitType.FEAT
print(commit.scope)  # "api"
print(commit.description)  # "add user authentication endpoint"
print(commit.is_conventional)  # True
```

##### `parse_multiple(commit_messages: List[str]) -> List[ParsedCommit]`

Parses multiple commit messages efficiently.

**Parameters:**
- `commit_messages`: List of commit message strings

**Returns:**
- List of `ParsedCommit` objects

**Example:**
```python
messages = [
    "feat: add new feature",
    "fix: resolve critical bug",
    "docs: update README"
]
commits = parser.parse_multiple(messages)
```

#### Internal Methods

- `_parse_type()`: Extracts and validates commit type
- `_infer_type_from_message()`: Infers type for non-conventional commits
- `_split_body_footer()`: Separates body and footer sections
- `_has_breaking_changes()`: Detects breaking change indicators
- `_extract_issues()`: Finds issue references (#123, closes #456)
- `_extract_co_authors()`: Extracts co-author information

### CommitAnalyzer

Provides statistical analysis and pattern recognition for collections of commits.

#### Key Methods

##### `analyze_commits(commit_messages: List[str]) -> Dict[str, Any]`

Analyzes commit patterns and returns comprehensive statistics.

**Parameters:**
- `commit_messages`: List of commit messages to analyze

**Returns:**
Dictionary containing:
- `total_commits`: Total number of commits
- `conventional_commits`: Number of conventional commits
- `conventional_percentage`: Percentage following conventional format
- `type_distribution`: Distribution of commit types
- `scope_distribution`: Distribution of commit scopes
- `breaking_changes`: Number of breaking changes
- `features`: Number of feature commits
- `bugfixes`: Number of bug fix commits
- `documentation`: Number of documentation commits
- `issues_referenced`: Count of unique issues referenced
- `co_authored_commits`: Number of commits with co-authors
- `average_description_length`: Average length of descriptions

**Example:**
```python
analyzer = CommitAnalyzer()
stats = analyzer.analyze_commits(commit_messages)

print(f"Conventional commits: {stats['conventional_percentage']:.1f}%")
print(f"Breaking changes: {stats['breaking_changes']}")
print(f"Type distribution: {stats['type_distribution']}")
```

## Dependencies & Imports

### Standard Library
- `re`: Regular expression operations for pattern matching
- `dataclasses`: For the ParsedCommit dataclass
- `typing`: Type hints and annotations
- `enum`: Enumeration support

### Internal Dependencies
- `constants.git.CONVENTIONAL_COMMIT_TYPES`: Configuration constants for valid commit types

### External Dependencies
None - the module uses only Python standard library components.

## Regular Expression Patterns

The parser uses several compiled regex patterns for efficient parsing:

### Conventional Commit Pattern
```python
CONVENTIONAL_PATTERN = re.compile(
    r'^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<description>.+)$',
    re.MULTILINE
)
```

Matches: `type(scope)!: description` format

### Breaking Change Patterns
- `BREAKING CHANGE:` in footer
- `BREAKING-CHANGE:` in footer  
- `!:` in subject line

### Issue Reference Patterns
- `#123` - Simple issue references
- `closes #123` - Closing issue references
- `fixes owner/repo#123` - Cross-repository references

### Co-Author Pattern
```python
CO_AUTHOR_PATTERN = re.compile(
    r'^Co-authored-by:\s*(.+)\s*<(.+)>$', 
    re.MULTILINE | re.IGNORECASE
)
```

## Usage Examples

### Basic Parsing

```python
from src.core.git.commit_parser import CommitParser

parser = CommitParser()

# Parse a conventional commit
commit = parser.parse("feat(auth): add OAuth2 support\n\nImplements OAuth2 authentication flow")
print(f"Type: {commit.type.value}")
print(f"Scope: {commit.scope}")
print(f"Breaking: {commit.breaking_change}")
```

### Batch Analysis

```python
from src.core.git.commit_parser import CommitAnalyzer

# Analyze multiple commits
messages = [
    "feat: add user management",
    "fix: resolve login issue", 
    "docs: update API documentation",
    "feat!: change authentication method"
]

analyzer = CommitAnalyzer()
results = analyzer.analyze_commits(messages)

print(f"Features: {results['features']}")
print(f"Breaking changes: {results['breaking_changes']}")
print(f"Type distribution: {results['type_distribution']}")
```

### Convenience Functions

```python
from src.core.git.commit_parser import parse_commit, analyze_commit_patterns

# Parse single commit
commit = parse_commit("fix(ui): resolve button alignment issue")

# Analyze patterns
stats = analyze_commit_patterns([
    "feat: new feature",
    "fix: bug fix", 
    "docs: documentation"
])
```

### Working with ParsedCommit Properties

```python
commit = parse_commit("feat!: redesign user interface\n\nBREAKING CHANGE: removes old UI components")

# Check commit characteristics
if commit.is_feature:
    print("This is a new feature")

if commit.is_breaking:
    print("This contains breaking changes")

if commit.is_conventional:
    print("Follows conventional commit format")

# Access structured data
print(f"Formatted type: {commit.formatted_type}")
print(f"Description: {commit.description}")
```

## Integration with Other Components

### Release Analysis
The commit parser integrates with `release_analyzer.py` to:
- Determine semantic version bumps based on commit types
- Generate release notes from commit messages
- Identify breaking changes for major version increments

### Log Analysis  
Works with `log_analyzer.py` to:
- Analyze commit patterns over time
- Generate development statistics
- Track project evolution metrics

### Change Tracking
Supports `changes_tracker.py` by:
- Providing structured commit data
- Enabling automated changelog generation
- Supporting impact analysis

## Implementation Notes

### Performance Considerations

1. **Regex Compilation**: All patterns are pre-compiled for efficient reuse
2. **Batch Processing**: `parse_multiple()` method optimizes for bulk operations
3. **Memory Efficiency**: Uses dataclasses for structured data with minimal overhead

### Design Decisions

1. **Enum Usage**: Provides type safety and IDE support for commit types and scopes
2. **Fallback Parsing**: Non-conventional commits are still parsed with type inference
3. **Comprehensive Extraction**: Captures issues, co-authors, and breaking changes beyond basic conventional commit spec

### Error Handling

The parser is designed to be robust:
- Invalid commit types default to `CommitType.OTHER`
- Malformed messages are still parsed with best-effort extraction
- Empty or None messages are handled gracefully

### Known Limitations

1. **Language Support**: Currently optimized for English commit messages
2. **Custom Patterns**: Limited support for organization-specific commit conventions
3. **Complex Footers**: May not parse all possible footer formats perfectly

### Future Improvements

1. **Configurable Patterns**: Support for custom regex patterns
2. **Internationalization**: Multi-language commit message support
3. **Plugin Architecture**: Extensible parsing for custom commit formats
4. **Performance Optimization**: Caching and parallel processing for large repositories

## Testing Considerations

When testing this module:

1. **Conventional Commits**: Test all standard types and scopes
2. **Edge Cases**: Empty messages, malformed syntax, unusual characters
3. **Breaking Changes**: Various breaking change indicators
4. **Issue References**: Different issue reference formats
5. **Performance**: Large batches of commits for performance testing

```python
# Example test cases
test_cases = [
    "feat(api): add new endpoint",
    "fix!: critical security fix",
    "docs: update README\n\nCloses #123",
    "refactor: improve code structure\n\nCo-authored-by: John Doe <john@example.com>",
    "chore: update dependencies\n\nBREAKING CHANGE: removes deprecated API"
]
```

## See Also

- [Git Log Analyzer](log_analyzer.md) - For commit history analysis
- [Release Analyzer](release_analyzer.md) - For semantic versioning and releases  
- [Changes Tracker](changes_tracker.md) - For changelog generation
- [Git Module Overview](README.md) - Overview of the git module
- [Conventional Commits Specification](https://www.conventionalcommits.org/) - External specification reference
