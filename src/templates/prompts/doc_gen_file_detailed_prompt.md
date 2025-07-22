<prompt>
<context>
You are creating detailed technical documentation for a specific file in a software project. This documentation should provide comprehensive information about the file's purpose, implementation, and usage.
</context>

<input_data>
- **File Path**: {file_path}
- **File Extension**: {file_extension}
- **File Contents**: {file_contents}
- **Related Files**: {related_files}
- **Folder Context**: {folder_context}
</input_data>

<output_requirements>
Create comprehensive technical documentation that includes:

### 1. File Overview
- Clear description of the file's purpose
- Role within the larger project/module
- Key responsibilities and functionality

### 2. Implementation Details
- Main functions, classes, or components
- Key algorithms or logic patterns
- Data structures and types used

### 3. Dependencies & Imports
- External libraries and modules used
- Internal project dependencies
- Configuration or environment requirements

### 4. API Documentation
- Public interfaces and functions
- Parameters, return values, and types
- Usage examples and code samples

### 5. Usage Examples
- Common use cases and patterns
- Integration with other components
- Best practices and recommendations

### 6. Implementation Notes
- Important design decisions
- Performance considerations
- Known limitations or edge cases
- Future improvement opportunities
</output_requirements>

<documentation_guidelines>

### Structure Requirements
- Use clear, hierarchical headings (H1, H2, H3)
- Provide code examples in proper syntax-highlighted blocks
- Include practical examples that developers can use
- Add cross-references to related files and documentation

### Technical Focus
Based on file type, emphasize:

#### For Code Files (.py, .js, .ts, etc.)
- Function/class signatures and documentation
- Algorithm explanations and complexity
- Error handling and edge cases
- Testing considerations

#### For Configuration Files (.yaml, .json, .toml, etc.)
- Configuration options and their effects
- Default values and valid ranges
- Environment-specific considerations
- Examples of common configurations

#### For Documentation Files (.md, .txt, etc.)
- Purpose and target audience
- Content organization and structure
- Maintenance and update procedures
- Related documentation references

#### For Build/Tool Files (.sh, Makefile, etc.)
- Purpose and when to use
- Prerequisites and dependencies
- Usage instructions and parameters
- Troubleshooting common issues

### Content Quality
- Write for developers who may be unfamiliar with the code
- Balance technical accuracy with readability
- Include practical examples and real-world usage
- Maintain consistency with project coding standards

### Code Examples
- Use proper syntax highlighting for code blocks
- Include complete, runnable examples where possible
- Show both basic and advanced usage patterns
- Demonstrate error handling and edge cases
</documentation_guidelines>

<example_structure>
[CODE_BLOCK:markdown]
# [File Name] Documentation

## Overview
Brief description of the file's purpose and role.

## Main Functions/Classes
### FunctionName
- **Purpose**: What it does
- **Parameters**: Input parameters
- **Returns**: What it returns
- **Example**: Usage example

## Dependencies
- List of imports and dependencies
- Internal vs external dependencies

## Usage Examples
Practical examples of how to use this file.

## Implementation Notes
Technical details and considerations.

## See Also
- [Related File](../other-file.md)
- [Folder Documentation](../README.md)
[/CODE_BLOCK]
</example_structure>

<critical_formatting>
**CRITICAL:** Always use [CODE_BLOCK:language] and [/CODE_BLOCK] markers instead of triple backticks (```).
This prevents file parsing issues during generation.

Examples:
- [CODE_BLOCK:python] ... [/CODE_BLOCK] for Python code
- [CODE_BLOCK:javascript] ... [/CODE_BLOCK] for JavaScript code  
- [CODE_BLOCK:bash] ... [/CODE_BLOCK] for shell commands
- [CODE_BLOCK] ... [/CODE_BLOCK] for plain text code blocks
</critical_formatting>

<quality_guidelines>
### Accuracy
- Ensure all code examples are syntactically correct
- Verify function signatures and parameter types
- Test examples to ensure they work as documented

### Completeness
- Cover all public interfaces and main functionality
- Include error cases and exception handling
- Document configuration options and environment variables

### Maintainability
- Use consistent formatting throughout
- Keep examples focused and relevant
- Update documentation when code changes

### Integration
- Reference related files and documentation
- Maintain consistency with overall project documentation
- Use the same terminology and conventions
</quality_guidelines>

<output_instruction>
Generate detailed, accurate, and practical documentation that serves as both a reference and learning resource for developers working with this file.

Generate ONLY the markdown content. Do not add meta-comments, explanations, or repeat the filename.
</output_instruction>

</prompt>
