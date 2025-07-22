# Output Constants Documentation

## Overview

The `src/constants/output.py` module provides a comprehensive set of constants, templates, and utility functions for consistent output formatting throughout the Codex-AI system. This module serves as the central hub for all output-related configurations including supported file formats, visual elements (emojis and colors), report templates, and formatting utilities.

**Key Responsibilities:**
- Define supported output formats with metadata
- Provide standardized emojis and color schemes
- Supply report templates for different document types
- Offer utility functions for text formatting and colorization
- Maintain progress indicators and visual feedback elements

## Main Components

### Output Formats (`OUTPUT_FORMATS`)

A comprehensive dictionary defining all supported output formats with their metadata:

```python
OUTPUT_FORMATS = {
    "JSON": {
        "extension": ".json",
        "mime_type": "application/json",
        "description": "Machine-readable JSON format",
        "use_cases": ["API responses", "data export", "pipeline integration"],
        "pretty": True
    },
    # ... other formats
}
```

**Supported Formats:**
- **JSON**: Machine-readable format for APIs and data export
- **YAML**: Human-readable format for configuration and documentation
- **MARKDOWN**: Documentation format for reports and README files
- **HTML**: Web format for dashboards and presentations
- **TEXT**: Plain text for logs and simple reports
- **CSV**: Tabular data format for analysis and spreadsheets

### Visual Elements

#### Emojis (`EMOJIS`)
Standardized emoji constants organized by category:

```python
# Status indicators
"SUCCESS": "✅",
"ERROR": "❌", 
"WARNING": "⚠️",

# Actions
"PROCESSING": "⚙️",
"GENERATING": "🔄",
"ANALYZING": "🔍",

# Content types
"FILE": "📄",
"FOLDER": "📁",
"CODE": "💻"
```

#### Colors (`COLORS` and `SEMANTIC_COLORS`)
ANSI color codes for terminal output with semantic mappings:

```python
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "RED": "\033[31m",
    "GREEN": "\033[32m"
}

SEMANTIC_COLORS = {
    "SUCCESS": COLORS["BRIGHT_GREEN"],
    "ERROR": COLORS["BRIGHT_RED"],
    "WARNING": COLORS["BRIGHT_YELLOW"]
}
```

### Report Templates (`REPORT_TEMPLATES`)

Pre-defined templates for different types of reports:

- **CHANGELOG**: Version release documentation
- **ANALYSIS**: Code analysis and metrics reports
- **DOCS**: General documentation generation
- **ERROR**: Error reporting and debugging information

## API Documentation

### Core Utility Functions

#### `colorize(text: str, color: str) -> str`

Applies color formatting to text for terminal output.

**Parameters:**
- `text` (str): Text to colorize
- `color` (str): Color name from COLORS or SEMANTIC_COLORS dictionaries

**Returns:**
- `str`: Colorized text with ANSI reset code appended

**Example:**
```python
from src.constants.output import colorize

# Using semantic colors
success_msg = colorize("Operation completed!", "SUCCESS")
error_msg = colorize("Something went wrong", "ERROR")

# Using direct colors
highlighted = colorize("Important text", "BRIGHT_CYAN")
print(success_msg)  # Prints in bright green
```

#### `format_with_emoji(text: str, emoji_name: str) -> str`

Formats text with an emoji prefix for visual feedback.

**Parameters:**
- `text` (str): Text to format
- `emoji_name` (str): Emoji name from EMOJIS dictionary

**Returns:**
- `str`: Text with emoji prefix, or original text if emoji not found

**Example:**
```python
from src.constants.output import format_with_emoji

status_msg = format_with_emoji("Task completed successfully", "SUCCESS")
print(status_msg)  # Output: "✅ Task completed successfully"

processing_msg = format_with_emoji("Analyzing code...", "ANALYZING")
print(processing_msg)  # Output: "🔍 Analyzing code..."
```

#### `get_output_extension(format_name: str) -> str`

Retrieves the file extension for a given output format.

**Parameters:**
- `format_name` (str): Format name from OUTPUT_FORMATS (case-insensitive)

**Returns:**
- `str`: File extension including dot, defaults to ".txt" if format not found

**Example:**
```python
from src.constants.output import get_output_extension

json_ext = get_output_extension("JSON")     # Returns ".json"
yaml_ext = get_output_extension("yaml")     # Returns ".yaml"
unknown_ext = get_output_extension("XYZ")   # Returns ".txt"
```

#### `build_report(template_name: str, **kwargs) -> str`

Constructs a formatted report using predefined templates.

**Parameters:**
- `template_name` (str): Template name from REPORT_TEMPLATES
- `**kwargs`: Template variables for substitution

**Returns:**
- `str`: Formatted report string

**Example:**
```python
from src.constants.output import build_report

# Generate a changelog entry
changelog = build_report(
    "CHANGELOG",
    title="My Project Changelog",
    version="1.2.0",
    date="2024-01-15",
    section_title="Features",
    content="- Added new API endpoints\n- Improved performance"
)

# Generate an analysis report
analysis = build_report(
    "ANALYSIS",
    title="Code Quality Report",
    overview_content="Overall code quality is good",
    metrics_content="- Coverage: 85%\n- Complexity: Low",
    details_content="Detailed analysis results...",
    recommendations_content="Consider adding more tests"
)
```

#### `format_progress_bar(current: int, total: int, width: int = 50) -> str`

Creates a visual progress bar for terminal output.

**Parameters:**
- `current` (int): Current progress value
- `total` (int): Maximum/total value
- `width` (int, optional): Width of progress bar in characters (default: 50)

**Returns:**
- `str`: Formatted progress bar string

**Example:**
```python
from src.constants.output import format_progress_bar

# Show progress at different stages
progress_25 = format_progress_bar(25, 100)
print(progress_25)  # [████████████▌                     ] 25%

progress_75 = format_progress_bar(75, 100, width=30)
print(progress_75)  # [██████████████████████▌       ] 75%
```

#### `strip_colors(text: str) -> str`

Removes ANSI color codes from text for plain text output.

**Parameters:**
- `text` (str): Text potentially containing ANSI color codes

**Returns:**
- `str`: Text with all color codes removed

**Example:**
```python
from src.constants.output import colorize, strip_colors

colored_text = colorize("Hello World", "RED")
plain_text = strip_colors(colored_text)
print(plain_text)  # Output: "Hello World" (without colors)
```

## Dependencies

### External Libraries
- **re**: Regular expressions for ANSI code stripping
- **datetime**: Timestamp generation for reports
- **typing**: Type hints for better code documentation

### Internal Dependencies
This module is designed to be self-contained with minimal internal dependencies, making it a foundational module that other parts of the system can safely import.

## Usage Examples

### Basic Text Formatting

```python
from src.constants.output import colorize, format_with_emoji, EMOJIS

# Combine colors and emojis for rich output
def print_status(message: str, status: str):
    if status == "success":
        formatted = format_with_emoji(message, "SUCCESS")
        colored = colorize(formatted, "SUCCESS")
    elif status == "error":
        formatted = format_with_emoji(message, "ERROR")
        colored = colorize(formatted, "ERROR")
    else:
        formatted = format_with_emoji(message, "INFO")
        colored = colorize(formatted, "INFO")
    
    print(colored)

# Usage
print_status("File processed successfully", "success")
print_status("Failed to read configuration", "error")
print_status("Starting analysis...", "info")
```

### Progress Tracking

```python
from src.constants.output import format_progress_bar, colorize
import time

def show_progress(items):
    total = len(items)
    for i, item in enumerate(items, 1):
        # Process item here
        time.sleep(0.1)  # Simulate work
        
        # Show progress
        progress = format_progress_bar(i, total)
        status = colorize(f"Processing: {progress}", "INFO")
        print(f"\r{status}", end="", flush=True)
    
    print()  # New line when complete
    completion = colorize("✅ All items processed!", "SUCCESS")
    print(completion)
```

### Report Generation

```python
from src.constants.output import build_report, get_output_extension
import json

def generate_analysis_report(data, output_format="MARKDOWN"):
    # Build the report content
    report_content = build_report(
        "ANALYSIS",
        title="Code Analysis Report",
        overview_content=f"Analyzed {len(data.get('files', []))} files",
        metrics_content=format_metrics(data.get('metrics', {})),
        details_content=format_details(data.get('details', [])),
        recommendations_content=format_recommendations(data.get('recommendations', []))
    )
    
    # Get appropriate file extension
    extension = get_output_extension(output_format)
    filename = f"analysis_report{extension}"
    
    # Save report
    with open(filename, 'w') as f:
        if output_format.upper() == "JSON":
            json.dump({"report": report_content}, f, indent=2)
        else:
            f.write(report_content)
    
    return filename

def format_metrics(metrics):
    lines = []
    for key, value in metrics.items():
        lines.append(f"- **{key.title()}**: {value}")
    return "\n".join(lines)
```

### Integration with Logging

```python
from src.constants.output import colorize, format_with_emoji, strip_colors
import logging

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages"""
    
    LEVEL_COLORS = {
        'DEBUG': 'DEBUG',
        'INFO': 'INFO',
        'WARNING': 'WARNING',
        'ERROR': 'ERROR',
        'CRITICAL': 'ERROR'
    }
    
    LEVEL_EMOJIS = {
        'DEBUG': 'INFO',
        'INFO': 'INFO',
        'WARNING': 'WARNING',
        'ERROR': 'ERROR',
        'CRITICAL': 'ERROR'
    }
    
    def format(self, record):
        # Get base message
        message = super().format(record)
        
        # Add emoji and color for terminal output
        if hasattr(record, 'no_color') and record.no_color:
            return message
        
        emoji_name = self.LEVEL_EMOJIS.get(record.levelname, 'INFO')
        color_name = self.LEVEL_COLORS.get(record.levelname, 'INFO')
        
        formatted = format_with_emoji(message, emoji_name)
        colored = colorize(formatted, color_name)
        
        return colored

# Usage
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Application started")
logger.warning("Configuration file not found, using defaults")
logger.error("Failed to connect to database")
```

## Implementation Notes

### Design Decisions

1. **Centralized Constants**: All output-related constants are centralized to ensure consistency across the application and make updates easier.

2. **Semantic Color Mapping**: Colors are mapped to semantic meanings (SUCCESS, ERROR, etc.) rather than direct color names, making the code more maintainable and allowing for theme changes.

3. **Template-Based Reports**: Report generation uses a template system that separates content from formatting, enabling easy customization and extension.

4. **Extensible Format Support**: The OUTPUT_FORMATS structure includes metadata that can be used by other parts of the system for validation and processing.

### Performance Considerations

- **String Operations**: Most functions perform simple string operations and are lightweight
- **Color Code Caching**: Color codes are pre-defined constants, avoiding runtime computation
- **Template Reuse**: Report templates are reusable and don't require recompilation

### Known Limitations

1. **Terminal Compatibility**: ANSI color codes may not work in all terminal environments
2. **Unicode Support**: Emoji display depends on terminal and font support
3. **Template Flexibility**: Current template system is relatively simple and may need enhancement for complex formatting needs

### Future Improvement Opportunities

1. **Theme Support**: Add support for different color themes (dark/light mode)
2. **Localization**: Support for different languages and emoji sets
3. **Advanced Templates**: More sophisticated template engine with conditionals and loops
4. **Format Validation**: Add validation functions for output format compatibility
5. **Performance Optimization**: Caching for frequently used formatted strings

## Error Handling

The module includes graceful error handling:

- **Missing Colors**: Functions return unmodified text if color names are not found
- **Missing Emojis**: Functions return text without emoji if emoji names are not found
- **Invalid Formats**: Default extensions and formats are provided for unknown types
- **Template Errors**: Missing templates return error messages rather than crashing

## Testing Considerations

When testing code that uses this module:

```python
from src.constants.output import strip_colors, colorize

def test_colored_output():
    # Test that colors are applied
    colored = colorize("test", "RED")
    assert colored != "test"  # Should be different due to color codes
    
    # Test that stripping works
    stripped = strip_colors(colored)
    assert stripped == "test"  # Should be back to original

def test_emoji_formatting():
    from src.constants.output import format_with_emoji
    
    result = format_with_emoji("message", "SUCCESS")
    assert result.startswith("✅")
    
    # Test with invalid emoji
    result = format_with_emoji("message", "INVALID")
    assert result == "message"  # Should return unchanged
```

## See Also

- [Constants Module Overview](../constants/README.md)
- [Git Constants](./git.md) - Git-related constants and utilities
- [AI Constants](./ai.md) - AI and machine learning constants
- [Project Constants](./project.md) - Project-specific configuration constants
- [Main Constants Index](./__init__.md) - Module initialization and exports
