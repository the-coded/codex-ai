# Constants Module

## Overview

The `src/constants` module serves as the centralized configuration hub for Codex-AI, providing standardized constants, configurations, and helper functions used throughout the application. This module follows the principle of single source of truth for all system-wide settings, from AI model configurations to Git operations and output formatting.

The constants module enables consistent behavior across all Codex-AI commands (changelog, doc-gen, doc-ui) by centralizing:
- AI model definitions and token management
- Git command templates and repository analysis patterns  
- Output formatting standards and color schemes
- Project metadata from pyproject.toml

## Contents

- **[ai.py](ai.py)**: AI model configurations, token strategies, and Aider command templates for automated code generation and documentation processing
- **[git.py](git.py)**: Git command templates, conventional commit patterns, repository analysis configurations, and merge commit detection
- **[output.py](output.py)**: Output formatting constants including colors, emojis, report templates, and progress indicators for consistent user experience
- **[project.py](project.py)**: Project metadata loader that reads from pyproject.toml as the single source of truth for version, author, and project information

## Architecture

### Dependency Flow
```
pyproject.toml → project.py → [Project Metadata]
                     ↓
ai.py → [Model Selection] → [Aider Commands]
  ↓
git.py → [Repository Analysis] → [Commit Processing]
  ↓
output.py → [Formatted Results] → [User Interface]
```

### Key Design Patterns

**Configuration as Code**: All constants are defined as Python dictionaries with structured metadata, enabling programmatic access and validation.

**Fallback Strategies**: AI models and Git operations include automatic fallback mechanisms (e.g., model selection by token count, default branch detection).

**Template-Based Commands**: Git and Aider commands use parameterized templates that can be dynamically formatted with runtime values.

**Semantic Organization**: Constants are grouped by functional domain (AI, Git, Output, Project) with clear separation of concerns.

## Usage Examples

### AI Model Selection
```python
from src.constants.ai import select_model_by_tokens, build_aider_command

# Automatic model selection based on content size
model = select_model_by_tokens(150000)
print(f"Selected: {model['name']}")  # anthropic/claude-4-sonnet-20250514

# Build Aider command for changelog generation
command = build_aider_command(
    "CHANGELOG", 
    "CLAUDE_4_SONNET",
    log_file="git_log.txt",
    prompt_file="changelog_prompt.txt", 
    output_file="CHANGELOG.md"
)
```

### Git Repository Analysis
```python
from src.constants.git import GIT_COMMANDS, get_conventional_commit_type

# Format Git command for commit history
cmd = GIT_COMMANDS["log"]["commit_history"].format(
    format="%H|%an|%ad|%s",
    options="--since='2024-01-01'"
)

# Analyze commit message
commit_type = get_conventional_commit_type("feat: add new documentation system")
print(commit_type)  # "feat"
```

### Output Formatting
```python
from src.constants.output import colorize, format_with_emoji, build_report

# Colorized terminal output
print(colorize("Operation successful!", "SUCCESS"))
print(format_with_emoji("Processing files", "PROCESSING"))

# Generate structured report
report = build_report(
    "CHANGELOG",
    title="Project Updates",
    version="1.2.0", 
    date="2024-01-15"
)
```

### Project Metadata Access
```python
from src.constants.project import get_version, get_name, PROJECT_INFO

# Simple getters
version = get_version()  # "0.1.0"
name = get_name()       # "codex-ai"

# Full project data
authors = PROJECT_INFO["authors"]
dependencies = PROJECT_INFO.get("dependencies", [])
```

## Implementation Details

### Token Management Strategy

The AI module implements sophisticated token management with safety margins and automatic model fallback:

- **Safety Margin**: Uses 95% of model's context window to prevent token overflow
- **Component Allocation**: Reserves tokens for AI response (64K) and Aider overhead (5K)
- **Dynamic Selection**: Automatically selects the best model based on content size

### Git Command Architecture

Git operations use a template-based system with built-in exclusion patterns:

- **Pathspec Exclusions**: Automatically excludes lock files, cache directories, and build artifacts
- **Conventional Commits**: Supports standard commit types (feat, fix, docs, etc.) with emoji mapping
- **Merge Detection**: Identifies merge commits through parent count and message patterns

### Output Consistency

The output module ensures consistent user experience across all commands:

- **Semantic Colors**: Maps logical concepts (SUCCESS, ERROR) to ANSI color codes
- **Emoji Standards**: Standardized emoji usage for visual feedback and status indication
- **Template System**: Reusable report templates for changelogs, analysis, and documentation

### Configuration Loading

Project metadata is loaded once on import and cached for performance:

- **Single Source**: pyproject.toml serves as the authoritative source for all project information
- **Version Compatibility**: Supports both Python 3.11+ (tomllib) and older versions (tomli)
- **Error Handling**: Graceful handling of missing or malformed configuration files

## Cross-Module Integration

### Command Integration
- **changelog**: Uses `ai.py` for model selection, `git.py` for commit analysis, `output.py` for formatting
- **doc-gen**: Leverages `git.py` for file change detection, `ai.py` for content generation
- **doc-ui**: Combines all modules for React/Sass/Storybook documentation generation

### Pipeline vs Local Mode
The constants support both execution modes:
- **Pipeline Mode**: Uses Git diff commands to detect changes between branches
- **Local Mode**: Uses Git status commands to process working directory changes

### Extensibility Points
- **New AI Models**: Add to `AI_MODELS` dictionary with priority and token limits
- **Custom Git Commands**: Extend `GIT_COMMANDS` with new operation templates  
- **Output Formats**: Add new formats to `OUTPUT_FORMATS` with appropriate metadata
- **Report Types**: Create new templates in `REPORT_TEMPLATES` for different use cases

## Best Practices

### Adding New Constants
1. Group related constants in appropriate modules
2. Include comprehensive metadata (descriptions, use cases, examples)
3. Add helper functions for complex operations
4. Update `__all__` exports for public API

### Using Constants
1. Import specific constants rather than entire modules
2. Use helper functions instead of direct dictionary access
3. Leverage fallback mechanisms for robust error handling
4. Follow established naming conventions (UPPER_CASE for constants)

### Testing Considerations
- Constants should be testable through their helper functions
- Mock external dependencies (Git commands, file system access)
- Validate template formatting with various parameter combinations
- Test fallback scenarios (missing models, invalid Git repositories)
