<prompt>
<context>
You are creating documentation for a folder/directory in a software project. This documentation should provide an overview of the folder's purpose, its contents, and how the files work together.
</context>

<input_data>
- **Folder Path**: {folder_path}
- **Documentation Strategy**: {docs_strategy} (separated or inline)
- **Files in Folder**: {folder_files}
- **File Contents**: {file_contents}
</input_data>

<output_requirements>
### For SEPARATED strategy (docs/ directory):
Create a comprehensive README.md that includes:
1. **Folder Overview** - Purpose and role in the project
2. **File Index** - Embedded index with descriptions
3. **Architecture** - How files interact and dependencies
4. **Usage Examples** - Common use cases and patterns
5. **Implementation Notes** - Important details for developers

### For INLINE strategy (./docs/ subdirectory):
Create a focused README.md that includes:
1. **Folder Overview** - Purpose and role in the project  
2. **Quick Reference** - Brief file descriptions
3. **See Also** - Reference to detailed INDEX.md for technical docs
</output_requirements>

<documentation_guidelines>
### Structure Requirements
- Start with a clear, descriptive title
- Use proper Markdown formatting
- Include code examples where relevant
- Add cross-references to related files/docs

### Technical Focus
- Explain the architectural patterns used
- Document key interfaces and abstractions
- Highlight important dependencies
- Note any configuration or setup requirements

### Content Quality
- Write for both newcomers and experienced developers
- Balance technical detail with accessibility
- Use consistent terminology throughout
- Include practical examples and use cases

### Cross-References
- Link to individual file documentation
- Reference related folders/modules
- Point to relevant external resources
- Maintain navigation consistency
</documentation_guidelines>

<example_structure>
[CODE_BLOCK:markdown]
# [Folder Name]

## Overview
Brief description of the folder's purpose and role.

## Contents
{file_index_content}

## Architecture
How components work together...

## Usage
Common patterns and examples...

## Implementation Details
Technical notes and considerations...
[/CODE_BLOCK]
</example_structure>

<critical_formatting>
**CRITICAL:** Always use [CODE_BLOCK:language] and [/CODE_BLOCK] markers instead of triple backticks (```).
This prevents file parsing issues during generation.

Examples:
- [CODE_BLOCK:python] ... [/CODE_BLOCK] for Python code
- [CODE_BLOCK:bash] ... [/CODE_BLOCK] for shell commands  
- [CODE_BLOCK:markdown] ... [/CODE_BLOCK] for markdown examples
- [CODE_BLOCK] ... [/CODE_BLOCK] for plain text code blocks
</critical_formatting>

<output_instruction>
- Focus on the folder as a cohesive unit
- Explain relationships between files
- Provide context for the folder's role in the larger project
- Use language appropriate for the codebase (technical but clear)
- Include practical information that helps developers work with the code

Generate comprehensive, well-structured documentation that serves as both an introduction and reference for this folder.

Generate ONLY the markdown content. Do not add meta-comments, explanations, or repeat the filename.
</output_instruction>

</prompt>
