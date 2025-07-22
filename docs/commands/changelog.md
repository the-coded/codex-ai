# Changelog Command Documentation

## Overview

The `changelog.py` file implements an AI-powered changelog generation system that analyzes Git commit history and produces structured changelog files. This command is part of the `src/commands` directory and serves as the primary interface for automated changelog creation using various AI models, with intelligent commit range detection and token optimization.

### Key Responsibilities
- Analyze Git commit history within specified ranges
- Generate structured changelogs using AI models (default: Claude-4 Sonnet)
- Implement intelligent token management and model fallback strategies
- Support tagged releases and development branch workflows
- Provide dry-run capabilities for cost estimation

## Main Functions

### `run_changelog()`

The core function that orchestrates the entire changelog generation process.

**Signature:**
```python
def run_changelog(
    output_file: str = "CHANGELOG.md",
    since_commit: Optional[str] = None,
    branch: Optional[str] = None,
    model_name: Optional[str] = None,
    verbose: bool = False,
    dry_run: bool = False
) -> bool
```

**Parameters:**
- `output_file` (str): Target changelog file path (default: "CHANGELOG.md")
- `since_commit` (Optional[str]): Starting commit for changelog range
- `branch` (Optional[str]): Git branch to analyze (default: current branch)
- `model_name` (Optional[str]): AI model identifier (default: Claude-4 Sonnet)
- `verbose` (bool): Enable detailed logging output
- `dry_run` (bool): Preview mode without AI generation or costs

**Returns:**
- `bool`: True if successful, False on error

**Key Features:**
- Intelligent range detection using Git tags
- Automatic token optimization with fallback strategies
- Tagged release detection and handling
- Comprehensive error handling and logging

### `changelog_command()`

CLI command handler that bridges command-line arguments to the core functionality.

**Signature:**
```python
def changelog_command(args) -> bool
```

**Parameters:**
- `args`: Parsed command-line arguments object with attributes matching `run_changelog()` parameters

## Dependencies & Imports

### External Dependencies
- `os`: File system operations and environment management
- `tempfile`: Temporary file handling (imported but not actively used)
- `pathlib.Path`: Modern path handling utilities
- `typing.Optional`: Type hints for optional parameters
- `shutil`: File operations for cleanup and moving

### Internal Project Dependencies
- `core.git.log_analyzer.GitLogAnalyzer`: Git history analysis and log generation
- `core.ai.model_selector`: AI model selection and management
  - `get_default_model()`: Returns Claude-4 Sonnet as default
  - `get_model_by_name()`: Model lookup by identifier
- `core.ai.token_manager.count_tokens()`: Token counting for optimization
- `core.ai.prompt_processor.get_changelog_prompt()`: Changelog-specific AI prompts
- `core.ai.aider_interface.run_changelog_generation()`: AI generation interface
- `constants.ai.get_effective_token_limit()`: Model-specific token limits

## Implementation Details

### Git Analysis Workflow

The system implements a sophisticated Git analysis workflow:

1. **Range Detection**: Uses `GitLogAnalyzer.get_changelog_range()` for intelligent commit range detection
2. **Tag Handling**: Detects if current commit is tagged and adjusts range accordingly
3. **Log Generation**: Implements three-tier fallback strategy:
   - Detailed log (full commit information)
   - Medium log (reduced detail)
   - Simple log (minimal information)

### Token Optimization Strategy

The implementation includes advanced token management:

```python
# Token optimization with fallback
tokens = count_tokens(log_content)
if tokens > token_limit:
    # Try medium log
    success = git_analyzer.generate_medium_log(log_file, since_commit, branch)
    # Further fallback to simple log if needed
```

### Working Directory Management

Uses `.tmp/` directory for intermediate files:
- `git_log.txt`: Generated Git log content
- `prompt.md`: AI prompt template
- Aider history files (moved post-generation)

## Usage Examples

### Basic Changelog Generation

```python
from src.commands.changelog import run_changelog

# Generate changelog with defaults
success = run_changelog()
if success:
    print("Changelog generated successfully!")
```

### Advanced Usage with Custom Parameters

```python
# Generate changelog for specific range with verbose output
success = run_changelog(
    output_file="RELEASE_NOTES.md",
    since_commit="v1.0.0",
    branch="main",
    model_name="anthropic/claude-4-sonnet-20250514",
    verbose=True,
    dry_run=False
)
```

### Dry Run for Cost Estimation

```python
# Preview changelog generation without AI costs
success = run_changelog(
    verbose=True,
    dry_run=True
)
# Outputs token counts, model selection, and cost estimates
```

### CLI Integration

```bash
# Command-line usage (assuming proper CLI setup)
python -m changelog --output CHANGELOG.md --since v1.0.0 --verbose
python -m changelog --dry-run --verbose  # Preview mode
```

## Tagged Release Handling

The system provides special handling for tagged releases:

```python
current_tag = git_analyzer.is_current_commit_tagged()
if current_tag:
    print(f"🏷️ Detected current commit is tagged: {current_tag}")
    # Automatically generates changelog FOR the tag
    # Uses range from previous tag to current tag
```

### Version Context Injection

For tagged releases, the system injects version context:

```python
version_context = f"""
=== CHANGELOG GENERATION CONTEXT ===
TARGET VERSION: {current_tag}
RANGE: {start_ref}..{current_tag}
HEADER MUST USE: {current_tag}
"""
```

## Error Handling & Logging

### Comprehensive Error Management

```python
try:
    # Main changelog generation logic
    success = git_analyzer.generate_detailed_log(log_file, since_commit, branch)
    if not success:
        print("❌ Failed to generate git log")
        return False
except Exception as e:
    print(f"❌ Error generating changelog: {e}")
    return False
```

### Verbose Logging

When `verbose=True`, the system provides detailed progress information:
- Git analysis progress
- Token usage statistics
- Model selection details
- File operation status
- AI generation progress

## Performance Considerations

### Token Efficiency

The system implements intelligent token management:
- Calculates precise token usage before AI calls
- Implements three-tier fallback strategy
- Reports efficiency metrics in verbose mode

```python
print(f"📊 Precise token breakdown:")
print(f"   • Prompt tokens: {prompt_tokens:,}")
print(f"   • Git log tokens: {git_log_tokens:,}")
print(f"   • Total input: {total_input_tokens:,}")
print(f"   • Efficiency: {(total_input_tokens/token_limit)*100:.1f}% of limit used")
```

### File System Optimization

- Uses `.tmp/` directory for intermediate files
- Implements cleanup strategies for temporary files
- Moves Aider history files to artifacts directory

## Configuration Options

### Model Selection

Default model: `anthropic/claude-4-sonnet-20250514`

Available through:
- `model_name` parameter
- `get_default_model()` for system default
- `get_model_by_name()` for custom models

### Token Limits

Configured through `constants.ai.get_effective_token_limit()`:
- Model-specific limits
- Safety margins included
- Automatic optimization based on limits

## Integration Points

### Git Integration

- Requires Git repository context
- Uses `GitLogAnalyzer` for all Git operations
- Supports branch and tag-based workflows

### AI Integration

- Interfaces with Aider for AI generation
- Supports multiple AI model providers
- Implements cost-aware generation strategies

### File System Integration

- Creates and manages `.tmp/` directory
- Handles output file generation and cleanup
- Preserves Aider artifacts for debugging

## Known Limitations

1. **Repository Dependency**: Requires Git repository context
2. **Token Limits**: Large repositories may hit token limits even with fallback
3. **AI Dependency**: Requires external AI service availability
4. **File System**: Assumes write permissions for `.tmp/` and output directories

## Future Improvement Opportunities

1. **Incremental Updates**: Support for updating existing changelogs
2. **Custom Templates**: User-defined changelog formats
3. **Multi-Repository**: Support for monorepo changelog generation
4. **Caching**: Implement intelligent caching for repeated operations
5. **Parallel Processing**: Optimize for large repository analysis

## Troubleshooting

### Common Issues

**Git Log Generation Fails**
- Ensure valid Git repository
- Check commit range validity
- Verify branch existence

**Token Limit Exceeded**
- Use `dry_run=True` to preview token usage
- Consider narrower commit ranges
- Check if simple log fallback is sufficient

**AI Generation Fails**
- Verify model availability
- Check API credentials
- Review token limits and usage

### Debug Information

Enable verbose mode for detailed diagnostics:
```python
success = run_changelog(verbose=True, dry_run=True)
```

## See Also

- [Git Log Analyzer](../core/git/log_analyzer.md) - Git history analysis
- [AI Model Selector](../core/ai/model_selector.md) - Model management
- [Token Manager](../core/ai/token_manager.md) - Token optimization
- [Aider Interface](../core/ai/aider_interface.md) - AI generation interface
- [Commands Overview](./README.md) - Command system documentation
