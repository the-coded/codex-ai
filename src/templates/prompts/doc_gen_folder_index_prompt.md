<prompt>
<context>
You are creating a technical navigation INDEX.md file for inline documentation strategy. This INDEX is specifically for the ./docs/ subdirectory and serves as a detailed navigation hub for technical documentation.
</context>

<input_data>
- **Folder Path**: {folder_path}
- **Files in Folder**: {folder_files}
- **Documentation Files**: {documentation_files}
- **File Summaries**: {file_summaries}
</input_data>

<output_requirements>
Create a comprehensive INDEX.md that serves as:
1. **Navigation Hub** - Easy access to all technical documentation
2. **Content Organization** - Logical grouping and categorization
3. **Quick Reference** - Overview of what each document contains
4. **Development Guide** - Helpful information for developers

### Required Sections

#### 1. Header
- Clear title indicating the folder being documented
- Brief description of the folder's purpose

#### 2. Documentation Map
- Organized list of all documentation files
- Brief description of what each document covers
- Clear categorization (by file type, functionality, etc.)

#### 3. Quick Navigation
- Links to most commonly needed documents
- Shortcuts to key implementation files
- Related documentation in other folders

#### 4. Development Notes
- Important implementation details
- Common patterns used in this folder
- Known gotchas or considerations
</output_requirements>

<documentation_guidelines>
### Organization Principles
- Group related documentation together
- Use clear, descriptive headings
- Maintain consistent link formatting
- Order items logically (alphabetical, by importance, or by workflow)

### Link Format
Use relative links to documentation files:
- `[File Documentation](filename.md)` for individual file docs
- `../folder/README.md` for related folder documentation
- Clear, descriptive link text

### Categorization Examples
- **Core Components** - Main implementation files
- **Utilities** - Helper and support functions  
- **Configuration** - Settings and configuration files
- **Tests** - Test files and test utilities
- **Types/Interfaces** - Type definitions and contracts

### Content Focus
- Technical accuracy over marketing language
- Practical information for developers
- Clear navigation paths
- Consistent formatting throughout

### Maintenance Considerations
- Use relative paths that won't break
- Keep descriptions concise but informative
- Update when new files are added
- Maintain alphabetical or logical ordering

### Integration
- Reference the main folder README.md
- Link to related documentation in other folders
- Point to external resources when relevant
- Maintain consistency with project documentation standards
</documentation_guidelines>

<example_structure>
[CODE_BLOCK:markdown]
# [Folder Name] - Technical Documentation

## Overview
Brief description of this folder's role and purpose.

## Documentation Index

### Core Components
- **[component.md](component.md)** - Main implementation details
- **[manager.md](manager.md)** - Management and orchestration logic

### Utilities & Helpers
- **[helpers.md](helpers.md)** - Utility functions and common operations
- **[validators.md](validators.md)** - Input validation and checking

### Configuration
- **[config.md](config.md)** - Configuration options and settings

## Quick Access

### Most Used
- [Main Implementation](component.md) - Start here for core functionality
- [Configuration Guide](config.md) - Setup and configuration

### Development
- [Helper Functions](helpers.md) - Commonly used utilities
- [Testing Guide](../tests/README.md) - Related test documentation

## Development Notes

### Key Patterns
- Description of architectural patterns used
- Common development workflows

### Important Considerations  
- Performance considerations
- Security notes
- Known limitations
[/CODE_BLOCK]
</example_structure>

<critical_formatting>
**CRITICAL:** Always use [CODE_BLOCK:language] and [/CODE_BLOCK] markers instead of triple backticks (```).
This prevents file parsing issues during generation.
</critical_formatting>

<output_instruction>
Generate a comprehensive INDEX.md that serves as an effective navigation and reference tool for developers working with this folder's technical documentation.

Generate ONLY the markdown content. Do not add meta-comments, explanations, or repeat the filename.
</output_instruction>

</prompt>
