# Project Constants Module Documentation

## Overview

The `src/constants/project.py` module serves as the central hub for project metadata management in Codex-AI. It provides a unified interface for accessing project information by reading directly from `pyproject.toml` as the single source of truth. This approach ensures consistency across the application and eliminates the need to maintain duplicate project metadata in multiple locations.

### Key Responsibilities
- Load and parse project configuration from `pyproject.toml`
- Provide convenient getter functions for common project metadata
- Handle cross-platform compatibility for TOML parsing
- Centralize project information access throughout the codebase

## Implementation Details

### Main Components

#### Data Loading
The module uses a lazy-loading pattern where `pyproject.toml` is read once during module import and cached in `_PYPROJECT_DATA`. This ensures efficient access to project metadata without repeated file I/O operations.

#### Cross-Platform TOML Support
The implementation handles Python version compatibility by using:
- `tomllib` (built-in) for Python 3.11+
- `tomli` (external dependency) for Python < 3.11

#### Error Handling
The module includes robust error handling for:
- Missing `pyproject.toml` files
- Invalid TOML syntax
- Missing required dependencies

### Data Structures

```python
# Internal data structure (loaded from pyproject.toml)
_PYPROJECT_DATA = {
    "project": {
        "name": "codex-ai",
        "version": "1.0.0",
        "description": "AI-powered code analysis tool",
        "authors": [{"name": "Author Name", "email": "author@example.com"}],
        "urls": {"Homepage": "https://github.com/user/codex-ai"}
    }
}
```

## Dependencies & Imports

### Standard Library
- `sys`: Python version detection for TOML library selection
- `pathlib.Path`: Cross-platform file path handling

### External Dependencies
- `tomllib` (Python 3.11+): Built-in TOML parsing library
- `tomli` (Python < 3.11): Third-party TOML parsing library

### Internal Dependencies
None - this module is designed to be self-contained and serve as a foundation for other modules.

### Installation Requirements
For Python versions < 3.11:
```bash
pip install tomli
```

## API Documentation

### Core Functions

#### `_load_pyproject_data()`
- **Purpose**: Internal function to load and parse `pyproject.toml`
- **Parameters**: None
- **Returns**: `dict` - Parsed TOML data structure
- **Raises**: 
  - `FileNotFoundError`: If `pyproject.toml` is not found
  - `tomllib.TOMLDecodeError`: If TOML syntax is invalid
- **Usage**: Called automatically during module import

#### `get_version()`
- **Purpose**: Retrieve the project version string
- **Parameters**: None
- **Returns**: `str` - Project version (e.g., "1.0.0")
- **Example**:
```python
from src.constants.project import get_version
version = get_version()  # Returns "1.0.0"
```

#### `get_name()`
- **Purpose**: Retrieve the project name
- **Parameters**: None
- **Returns**: `str` - Project name
- **Example**:
```python
from src.constants.project import get_name
name = get_name()  # Returns "codex-ai"
```

#### `get_author()`
- **Purpose**: Retrieve the primary author's name
- **Parameters**: None
- **Returns**: `str` - Author name from first author entry
- **Example**:
```python
from src.constants.project import get_author
author = get_author()  # Returns first author's name
```

#### `get_author_email()`
- **Purpose**: Retrieve the primary author's email address
- **Parameters**: None
- **Returns**: `str` - Author email from first author entry
- **Example**:
```python
from src.constants.project import get_author_email
email = get_author_email()  # Returns first author's email
```

#### `get_description()`
- **Purpose**: Retrieve the project description
- **Parameters**: None
- **Returns**: `str` - Project description text
- **Example**:
```python
from src.constants.project import get_description
desc = get_description()  # Returns project description
```

#### `get_url()`
- **Purpose**: Retrieve the project homepage URL
- **Parameters**: None
- **Returns**: `str` - Homepage URL or empty string if not set
- **Example**:
```python
from src.constants.project import get_url
url = get_url()  # Returns homepage URL or ""
```

### Module Variables

#### `PROJECT_INFO`
- **Type**: `dict`
- **Purpose**: Direct access to the project section of `pyproject.toml`
- **Usage**: For advanced use cases requiring direct data access
- **Example**:
```python
from src.constants.project import PROJECT_INFO
all_authors = PROJECT_INFO["authors"]  # List of all authors
```

## Usage Examples

### Basic Project Information Access
```python
from src.constants.project import get_name, get_version, get_description

# Display project banner
print(f"{get_name()} v{get_version()}")
print(f"Description: {get_description()}")
```

### Version Comparison
```python
from src.constants.project import get_version
from packaging import version

current_version = version.parse(get_version())
minimum_version = version.parse("1.0.0")

if current_version >= minimum_version:
    print("Version requirements met")
```

### Integration with Logging
```python
import logging
from src.constants.project import get_name, get_version

logger = logging.getLogger(get_name())
logger.info(f"Starting {get_name()} version {get_version()}")
```

### CLI Application Header
```python
from src.constants.project import get_name, get_version, get_author

def print_header():
    print(f"{'='*50}")
    print(f"{get_name().upper()} v{get_version()}")
    print(f"Author: {get_author()}")
    print(f"{'='*50}")
```

### Error Handling Example
```python
try:
    from src.constants.project import get_version
    version = get_version()
except FileNotFoundError:
    print("Error: pyproject.toml not found")
    version = "unknown"
except ImportError as e:
    print(f"Error: Missing dependency - {e}")
    version = "unknown"
```

## Implementation Notes

### Design Decisions

#### Single Source of Truth
The module enforces the principle of having `pyproject.toml` as the single source of truth for project metadata. This eliminates inconsistencies that can arise from maintaining duplicate information in multiple files.

#### Lazy Loading Pattern
Project data is loaded once during module import rather than on each function call. This provides better performance for applications that frequently access project metadata.

#### Defensive Programming
The module includes comprehensive error handling and graceful degradation for missing dependencies or malformed configuration files.

### Performance Considerations

#### Memory Usage
The entire `pyproject.toml` content is loaded into memory during import. For large configuration files, consider implementing selective loading if memory usage becomes a concern.

#### File I/O
File reading occurs only once during module import, making subsequent metadata access very fast (O(1) dictionary lookups).

### Known Limitations

#### Multiple Authors
The `get_author()` and `get_author_email()` functions only return information for the first author. Applications needing all authors should access `PROJECT_INFO["authors"]` directly.

#### URL Handling
The `get_url()` function specifically looks for the "Homepage" key in URLs. Other URL types (documentation, repository, etc.) require direct access to `PROJECT_INFO`.

#### Path Resolution
The module assumes `pyproject.toml` is located three directories up from the module file. This may need adjustment if the project structure changes.

### Future Improvement Opportunities

#### Enhanced URL Support
```python
def get_repository_url():
    """Get repository URL from pyproject.toml."""
    return PROJECT_INFO.get("urls", {}).get("Repository", "")

def get_documentation_url():
    """Get documentation URL from pyproject.toml."""
    return PROJECT_INFO.get("urls", {}).get("Documentation", "")
```

#### Configuration Validation
Consider adding validation to ensure required fields are present in `pyproject.toml`:
```python
def validate_project_config():
    """Validate that required project fields are present."""
    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in PROJECT_INFO:
            raise ValueError(f"Required field '{field}' missing from pyproject.toml")
```

#### Caching Improvements
For applications with changing `pyproject.toml` files, consider implementing cache invalidation:
```python
def reload_project_data():
    """Reload project data from pyproject.toml."""
    global _PYPROJECT_DATA, PROJECT_INFO
    _PYPROJECT_DATA = _load_pyproject_data()
    PROJECT_INFO = _PYPROJECT_DATA["project"]
```

## Testing Considerations

### Unit Test Coverage
- Test all getter functions with valid `pyproject.toml`
- Test error handling for missing files
- Test error handling for invalid TOML syntax
- Test cross-platform TOML library selection

### Integration Testing
- Verify compatibility with actual project `pyproject.toml`
- Test module import in different Python versions
- Validate performance with large configuration files

## See Also

- [Constants Module Overview](../constants/README.md)
- [AI Constants](ai.md)
- [Git Constants](git.md)
- [Output Constants](output.md)
- [Project Configuration Guide](../../docs/configuration.md)
