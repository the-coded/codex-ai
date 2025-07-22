# Doc-UI Command Documentation

## Overview

The `doc_ui.py` file implements the Doc-UI documentation command for the Codex-AI system. This command generates AI-powered documentation for React, Sass, and Storybook files using intelligent file detection and mode selection. It follows the same architectural patterns as other commands like `map_tree` and `changelog`, providing consistent behavior and error handling across the system.

The Doc-UI command automatically detects file types, maps component relationships, and generates comprehensive documentation using AI models while respecting token limits and workspace configurations.

## Main Functions and Classes

### `run_doc_ui()`
- **Purpose**: Main entry point for Doc-UI documentation generation
- **Parameters**:
  - `mode` (Optional[str]): Detection mode ("local", "pipeline", or None for auto-detect)
  - `doc` (str): Documentation type ("react", "sass", "storybook", "all")
  - `since_commit` (Optional[str]): For pipeline mode - compare since this commit
  - `model_name` (Optional[str]): AI model to use (default: claude-4-sonnet)
  - `output_dir` (str): Output directory for documentation
  - `path` (Optional[str]): Process specific directory/file path
  - `verbose` (bool): Enable verbose output
  - `dry_run` (bool): Preview mode - analyze but don't generate files
- **Returns**: `bool` - True if successful, False otherwise
- **Example**:

```python
# Generate all documentation types in auto-detect mode
success = run_doc_ui(verbose=True)

# Generate only React documentation for specific path
success = run_doc_ui(
    doc="react",
    path="src/components/Button",
    verbose=True
)

# Dry run to preview without AI costs
success = run_doc_ui(dry_run=True, verbose=True)
```

### `detect_file_types()`
- **Purpose**: Categorizes files by type with cross-type trigger logic
- **Parameters**: `files` (List[str]) - List of file paths to analyze
- **Returns**: `Dict[str, List[str]]` - Categorized files by type (react, sass, storybook)
- **Logic**:
  - Component.tsx/config.ts modified → React docs + Storybook docs (if stories exist)
  - Component.stories.tsx modified → Storybook docs only
  - Component.scss modified → Sass docs only
- **Example**:

```python
files = [
    "src/components/Button/Button.tsx",
    "src/components/Card/Card.stories.tsx",
    "src/styles/button.scss"
]
categorized = detect_file_types(files)
# Returns: {
#   "react": ["src/components/Button/Button.tsx"],
#   "storybook": ["src/components/Card/Card.stories.tsx"],
#   "sass": ["src/styles/button.scss"]
# }
```

### `map_files_for_doc_type()`
- **Purpose**: Maps changed files to context files (for reading) and output files (for writing)
- **Parameters**:
  - `file_type` (str): Type of documentation (react, sass, storybook)
  - `changed_files` (List[str]): List of files that were changed
- **Returns**: `Dict[str, Any]` with 'context_files' and 'output_files'
- **Example**:

```python
mapping = map_files_for_doc_type("react", ["src/components/Button/Button.tsx"])
# Returns: {
#   "context_files": [
#     "src/components/Button/Button.tsx",
#     "src/components/Button/Button.config.ts",
#     "react/.eslintrc.cjs",
#     "react/tsconfig.json"
#   ],
#   "output_files": ["docs/react/components/Button/README.md"]
# }
```

### `get_component_siblings()`
- **Purpose**: Detects component sibling files for comprehensive documentation
- **Parameters**: `changed_file` (str) - The file that was changed
- **Returns**: `List[str]` - Related files that should be read for context
- **Example**:

```python
siblings = get_component_siblings("src/components/Button/Button.tsx")
# Returns: [
#   "src/components/Button/Button.config.ts",
#   "src/components/Button/Button.stories.tsx",
#   "src/components/Button/Button.scss"
# ]
```

### `detect_workspace_root()`
- **Purpose**: Detects workspace root based on file path and type
- **Parameters**:
  - `file_path` (str): Path to the file
  - `file_type` (str): Type of file (react, sass, storybook)
- **Returns**: `str` - Workspace root path
- **Examples**:
  - `react/src/components/Button/Button.tsx` → `react/`
  - `sass/src/default/Button/Button.scss` → `sass/`
  - `src/components/Button/Button.tsx` → `./`

### `find_workspace_configs()`
- **Purpose**: Finds configuration files in the appropriate workspace
- **Parameters**:
  - `file_path` (str): Path to the file being processed
  - `file_type` (str): Type of documentation (react, sass, storybook)
- **Returns**: `List[str]` - List of configuration file paths that exist
- **Configuration Types**:
  - React/Storybook: ESLint, Prettier, TypeScript configs
  - Sass: StyleLint, Prettier, PostCSS configs

## Dependencies & Imports

### External Dependencies
- `os`, `json`, `pathlib`: Standard library modules for file system operations
- `typing`: Type hints for better code documentation

### Internal Dependencies
- `core.git`: Git operations and file detection
- `core.ai.model_selector`: AI model selection and management
- `core.ai.token_manager`: Token counting and limit management
- `core.ai.aider_interface`: AI generation interface
- `constants.ai`: AI-related constants and configurations
- `constants.git`: Git command constants

### Configuration Requirements
- Git repository (required for file detection)
- AI model access (Claude, GPT, etc.)
- Workspace configuration files (.eslintrc.cjs, tsconfig.json, etc.)

## File Type Patterns

### React Files
```python
DOC_UI_FILE_PATTERNS["react"] = {
    "extensions": [".tsx", ".jsx", ".ts", ".js"],
    "required_patterns": ["component", "src/", ".config.ts"],
    "exclude_patterns": [".test.", ".spec.", ".stories.", ".d.ts", "index."],
    "description": "React components and utilities"
}
```

### Sass Files
```python
DOC_UI_FILE_PATTERNS["sass"] = {
    "extensions": [".scss", ".sass", ".css"],
    "required_patterns": [],
    "exclude_patterns": [".min.", ".map"],
    "description": "Sass/SCSS stylesheets"
}
```

### Storybook Files
```python
DOC_UI_FILE_PATTERNS["storybook"] = {
    "extensions": [".stories.tsx", ".stories.jsx", ".stories.ts", ".stories.js"],
    "required_patterns": [],
    "exclude_patterns": [],
    "description": "Storybook stories"
}
```

## Usage Examples

### Basic Usage
```bash
# Auto-detect mode, all file types
codex-ai doc-ui

# Local mode: staged/modified files
codex-ai doc-ui --local

# Pipeline mode: changed files since origin/main
codex-ai doc-ui --pipeline
```

### Specific Documentation Types
```bash
# Only React components
codex-ai doc-ui --doc react

# Only Sass files
codex-ai doc-ui --doc sass

# Only Storybook stories
codex-ai doc-ui --doc storybook
```

### Path-Based Processing
```bash
# Process specific path
codex-ai doc-ui --path react/src/components/Button

# Path with doc filter
codex-ai doc-ui --path react/src/components/ --doc react
```

### Advanced Options
```bash
# Pipeline: files changed in last 5 commits
codex-ai doc-ui --since HEAD~5

# Preview without AI costs
codex-ai doc-ui --dry-run

# Detailed output
codex-ai doc-ui --verbose

# Custom model
codex-ai doc-ui --model gpt-4
```

### Programmatic Usage
```python
from src.commands.doc_ui import run_doc_ui

# Generate React documentation for specific components
success = run_doc_ui(
    doc="react",
    path="src/components/Button",
    model_name="claude-4-sonnet",
    verbose=True
)

# Dry run to analyze files without AI costs
success = run_doc_ui(
    mode="local",
    doc="all",
    dry_run=True,
    verbose=True
)
```

## Mode Detection Logic

### Auto-Detection
The system automatically detects the appropriate mode based on Git status:
- **Local mode**: Used when staged/modified files exist
- **Pipeline mode**: Used when no local changes are detected

### Mode Behaviors
- **Local mode**: Processes staged and modified files (`git status`)
- **Pipeline mode**: Processes files changed since specified commit or `origin/main`
- **Path mode**: Processes specific directory/file path (overrides mode detection)

## Cross-Type Trigger System

The Doc-UI command implements intelligent cross-type triggers:

### Component Modification Triggers
When a React component is modified:
1. **Always** generates React documentation
2. **Conditionally** generates Storybook documentation if `.stories` file exists

### File Type Isolation
- **Stories files**: Only trigger Storybook documentation
- **Sass files**: Only trigger Sass documentation
- **Test files**: Excluded from all documentation types

## Output Structure

### React Documentation
```
docs/react/
├── components/
│   ├── atoms/
│   │   └── Button/
│   │       └── README.md
│   └── molecules/
│       └── Card/
│           └── README.md
└── utils/
    └── helpers.md
```

### Sass Documentation
```
docs/sass/
├── components/
│   ├── button.md
│   └── card.md
└── utilities/
    └── mixins.md
```

### Storybook Documentation
Storybook documentation modifies the original `.stories.tsx` files in place, enhancing them with comprehensive documentation and examples.

## Implementation Notes

### Performance Considerations
- **Token Management**: Automatically calculates and respects AI model token limits
- **Batch Processing**: Groups related files to minimize AI API calls
- **Sibling Detection**: Efficiently finds related component files

### Error Handling
- **Git Availability**: Checks for Git module availability before processing
- **File Existence**: Validates file paths before processing
- **Token Limits**: Warns when files exceed model token limits
- **AI Failures**: Gracefully handles AI generation failures

### Design Decisions
- **Sibling File Detection**: Automatically includes related files (config, styles, stories) for comprehensive context
- **Workspace Detection**: Intelligently detects workspace roots for proper configuration file inclusion
- **Smart Naming**: Uses README.md when component name matches folder name, otherwise uses COMPONENT.md

### Known Limitations
- Requires Git repository for file detection
- AI model availability and API limits
- Large component trees may exceed token limits
- Configuration file detection depends on standard naming conventions

### Future Improvements
- Support for additional file types (Vue, Angular)
- Enhanced workspace detection for monorepos
- Incremental documentation updates
- Custom prompt templates per project

## CLI Integration

### Command Handler
```python
def doc_ui_command(args):
    """CLI command handler for Doc-UI documentation generation."""
    return run_doc_ui(
        mode=args.mode,
        doc=args.doc,
        since_commit=args.since,
        model_name=args.model,
        output_dir=args.output_dir,
        path=args.path,
        verbose=args.verbose,
        dry_run=args.dry_run
    )
```

### Argument Parser
The `add_doc_ui_arguments()` function adds all necessary CLI arguments following the project's argument parsing patterns.

## See Also

- [Map Tree Command](map_tree.md) - Similar file detection patterns
- [Changelog Command](changelog.md) - Similar AI integration approach
- [Core Git Module](../core/git.md) - File detection and Git operations
- [AI Interface](../core/ai/aider_interface.md) - AI generation implementation
- [Commands Overview](README.md) - All available commands
