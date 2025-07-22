"""
Doc-UI documentation command implementation.

Generates documentation for React, Sass, and Storybook files using AI with intelligent
file detection and mode selection. Follows the same patterns as map_tree and changelog.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from core.git import ChangesTracker, get_repository_state, get_changes_since_commit, auto_detect_mode, get_files_for_mode, get_files_for_path
from core.ai.model_selector import get_default_model, get_model_by_name
from core.ai.token_manager import count_tokens
from core.ai.aider_interface import run_doc_ui_generation
from constants.ai import get_effective_token_limit
from constants.git import GIT_STATUS_COMMANDS, GIT_DIFF_COMMANDS
from core import GIT_AVAILABLE

# ===== DOC-UI SPECIFIC CONSTANTS =====
# These are specific to documentation processing and differ from tree generation needs

# Doc-UI specific exclusion patterns
DOC_UI_EXCLUDE_DIRECTORIES = [
    # Build/dist directories
    "dist", "build", "out", ".next", ".nuxt",
    
    # Dependencies
    "node_modules", "venv",
    
    # IDE/editor files
    ".vscode", ".idea",
    
    # Version control
    ".git", ".github",
    
    # Cache directories
    "__pycache__", ".tmp", ".aider.tags.cache.v3",
    
    # Test directories (specific for doc-ui)
    "tests", "test", "__tests__",
    
    # Coverage/logs
    "coverage", ".nyc_output", "logs",
    
    # OS files
    ".DS_Store",
    
    # Documentation build (avoid recursion)
    "docs/build", "docs/dist"
]


def is_doc_ui_excluded_directory(dirname: str) -> bool:
    """
    Check if a directory should be excluded from doc-ui processing.
    
    Args:
        dirname: Directory name to check
        
    Returns:
        True if directory should be excluded
    """
    return dirname in DOC_UI_EXCLUDE_DIRECTORIES


# File type detection patterns (following constants pattern)
DOC_UI_FILE_PATTERNS = {
    "react": {
        "extensions": [".tsx", ".jsx", ".ts", ".js"],
        "required_patterns": ["component", "src/", ".config.ts"],
        "exclude_patterns": [".test.", ".spec.", ".stories.", ".d.ts", "index."],
        "description": "React components and utilities"
    },
    "sass": {
        "extensions": [".scss", ".sass", ".css"],
        "required_patterns": [],
        "exclude_patterns": [".min.", ".map"],
        "description": "Sass/SCSS stylesheets"
    },
    "storybook": {
        "extensions": [".stories.tsx", ".stories.jsx", ".stories.ts", ".stories.js"],
        "required_patterns": [],
        "exclude_patterns": [],
        "description": "Storybook stories"
    }
}


def has_stories_file(file_path: str) -> bool:
    """
    Check if a component has a corresponding .stories file.
    
    Args:
        file_path: Path to component file
        
    Returns:
        bool: True if stories file exists
    """
    if not file_path:
        return False
        
    base_dir = get_component_base_path(file_path)
    if not base_dir:
        return False
    
    # Get component name from the file
    file_basename = os.path.splitext(os.path.basename(file_path))[0]
    # Remove suffixes to get component name
    component_name = file_basename
    for suffix in ['.config', '.stories', '.test']:
        if component_name.endswith(suffix):
            component_name = component_name[:-len(suffix)]
            break
    
    # Check for various story file extensions
    story_extensions = ['.stories.tsx', '.stories.ts', '.stories.jsx', '.stories.js']
    for ext in story_extensions:
        stories_path = f"{base_dir}/{component_name}{ext}"
        if os.path.exists(stories_path):
            return True
    
    return False


def detect_file_types(files: List[str]) -> Dict[str, List[str]]:
    """
    Detect file types and categorize them with cross-type triggers.
    
    Logic:
    - Component.tsx/config.ts modified → React docs + Storybook docs (if stories exist)
    - Component.stories.tsx modified → Storybook docs only
    - Component.scss modified → Sass docs only
    
    Args:
        files: List of file paths
        
    Returns:
        Dict[str, List[str]]: Categorized files by type
    """
    if not files:
        return {file_type: [] for file_type in DOC_UI_FILE_PATTERNS.keys()}
        
    categorized = {file_type: [] for file_type in DOC_UI_FILE_PATTERNS.keys()}
    
    for file_path in files:
        if not file_path:  # Skip empty strings
            continue
            
        # Check if file is in excluded directory
        path_obj = Path(file_path)
        if any(is_doc_ui_excluded_directory(part) for part in path_obj.parts):
            continue
        
        # Cross-type trigger logic
        is_react_component = (
            _matches_file_pattern(file_path, DOC_UI_FILE_PATTERNS["react"]) and
            not file_path.endswith(('.stories.tsx', '.stories.ts', '.stories.jsx', '.stories.js'))
        )
        is_stories_file = _matches_file_pattern(file_path, DOC_UI_FILE_PATTERNS["storybook"])
        is_sass_file = _matches_file_pattern(file_path, DOC_UI_FILE_PATTERNS["sass"])
        
        # Apply cross-type triggers
        if is_react_component:
            # Always add to react
            categorized["react"].append(file_path)
            
            # If component has stories, also trigger storybook
            if has_stories_file(file_path):
                categorized["storybook"].append(file_path)
                
        elif is_stories_file:
            # Stories files only trigger storybook
            categorized["storybook"].append(file_path)
            
        elif is_sass_file:
            # Sass files only trigger sass
            categorized["sass"].append(file_path)
    
    return categorized


def _matches_file_pattern(file_path: str, patterns: Dict[str, Any]) -> bool:
    """Check if file matches pattern criteria."""
    # Check extensions
    if not any(file_path.endswith(ext) for ext in patterns["extensions"]):
        return False
    
    # Check exclude patterns
    if any(exclude in file_path for exclude in patterns["exclude_patterns"]):
        return False
    
    # Check required patterns (if any)
    if patterns["required_patterns"]:
        if not any(pattern in file_path for pattern in patterns["required_patterns"]):
            return False
    
    return True


def get_component_base_path(file_path: str) -> str:
    """
    Get component base path for sibling detection.
    
    Example: 
    - src/components/atoms/Button/Button.tsx → src/components/atoms/Button
    - src/components/atoms/Button/Button.config.ts → src/components/atoms/Button
    """
    if not file_path:
        return ""
    
    # Remove extension
    base = os.path.splitext(file_path)[0]
    
    # Remove .config, .stories, .test suffixes
    for suffix in ['.config', '.stories', '.test']:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    
    # Return directory path only (remove filename)
    return os.path.dirname(base)


def detect_workspace_root(file_path: str, file_type: str) -> str:
    """
    Detect workspace root based on file path and type.
    
    Examples:
    - react/src/components/Button/Button.tsx → react/
    - sass/src/default/Button/Button.scss → sass/
    - src/components/Button/Button.tsx → ./
    
    Args:
        file_path: Path to the file
        file_type: Type of file (react, sass, storybook)
        
    Returns:
        str: Workspace root path
    """
    if not file_path:
        return "."
    
    path_parts = Path(file_path).parts
    
    if file_type in ["react", "storybook"]:
        if "react" in path_parts:
            # Workspace: react/src/... → react/
            react_index = path_parts.index("react")
            return "/".join(path_parts[:react_index + 1])
        else:
            # No workspace: src/... → ./
            return "."
            
    elif file_type == "sass":
        if "sass" in path_parts:
            # Workspace: sass/src/... → sass/
            sass_index = path_parts.index("sass")
            return "/".join(path_parts[:sass_index + 1])
        else:
            # No workspace: src/... → ./
            return "."
    
    return "."


def find_workspace_configs(file_path: str, file_type: str) -> List[str]:
    """
    Find configuration files in the appropriate workspace.
    
    Args:
        file_path: Path to the file being processed
        file_type: Type of documentation (react, sass, storybook)
        
    Returns:
        List[str]: List of configuration file paths that exist
    """
    workspace_root = detect_workspace_root(file_path, file_type)
    config_files = []
    
    if file_type in ["react", "storybook"]:
        # React/Storybook configs: ESLint + Prettier + TypeScript
        config_names = [
            ".eslintrc.cjs",
            ".prettierrc.cjs",
            "tsconfig.json",
            "tsconfig.node.json",
            "package.json"
        ]
    elif file_type == "sass":
        # Sass configs: StyleLint + Prettier + PostCSS
        config_names = [
            ".stylelintrc.cjs",
            ".prettierrc.cjs",
            "postcss.config.cjs",
            "package.json"
        ]
    else:
        config_names = []
    
    # Find existing config files in workspace root
    for config_name in config_names:
        config_path = f"{workspace_root}/{config_name}"
        if os.path.exists(config_path):
            config_files.append(config_path)
    
    return config_files


def get_component_siblings(changed_file: str) -> List[str]:
    """
    Detect component sibling files for comprehensive documentation.
    
    Args:
        changed_file: The file that was changed
        
    Returns:
        List of related files that should be read for context
    """
    if not changed_file:
        return []
        
    base_dir = get_component_base_path(changed_file)
    if not base_dir:
        return []
    
    # Get component name from the changed file
    file_basename = os.path.splitext(os.path.basename(changed_file))[0]
    # Remove suffixes to get component name
    component_name = file_basename
    for suffix in ['.config', '.stories', '.test']:
        if component_name.endswith(suffix):
            component_name = component_name[:-len(suffix)]
            break
    
    # Potential sibling files in the same directory
    potential_siblings = [
        f"{base_dir}/{component_name}.tsx",
        f"{base_dir}/{component_name}.ts", 
        f"{base_dir}/{component_name}.jsx",
        f"{base_dir}/{component_name}.js",
        f"{base_dir}/{component_name}.config.ts",
        f"{base_dir}/{component_name}.stories.tsx",
        f"{base_dir}/{component_name}.stories.ts",
        f"{base_dir}/{component_name}.stories.jsx",
        f"{base_dir}/{component_name}.stories.js",
        f"{base_dir}/{component_name}.scss",
        f"{base_dir}/{component_name}.sass",
        f"{base_dir}/{component_name}.css"
    ]
    
    # Return only existing files, excluding the input file itself
    existing_siblings = [f for f in potential_siblings if os.path.exists(f) and f != changed_file]
    return existing_siblings


def map_files_for_doc_type(file_type: str, changed_files: List[str]) -> Dict[str, Any]:
    """
    Map changed files to context files (for reading) and output files (for writing).
    
    Args:
        file_type: Type of documentation (react, sass, storybook)
        changed_files: List of files that were changed
        
    Returns:
        Dict with 'context_files' and 'output_files'
    """
    context_files = []
    output_files = []
    
    if file_type == "react":
        # React: For each component, read .tsx + .config.ts, write docs/react/Component.md
        processed_components = set()
        
        for file in changed_files:
            base_path = get_component_base_path(file)
            if base_path in processed_components:
                continue
            processed_components.add(base_path)
            
            # Get siblings for context
            siblings = get_component_siblings(file)
            # Filter to only .tsx/.ts/.jsx/.js and .config.ts
            react_siblings = [s for s in siblings if 
                            (s.endswith(('.tsx', '.ts', '.jsx', '.js')) and not s.endswith('.stories.tsx')) or 
                            s.endswith('.config.ts')]
            context_files.extend(react_siblings)
            
            # IMPORTANT: Always include the original component file itself
            if file not in context_files:
                context_files.append(file)
            
            # Include workspace configuration files for React
            workspace_configs = find_workspace_configs(file, "react")
            context_files.extend(workspace_configs)
            
            # Generate output path with smart naming logic
            relative_path = os.path.relpath(base_path, os.getcwd())
            # Remove react/ prefix if present
            if relative_path.startswith('react/'):
                relative_path = relative_path[6:]  # Remove 'react/' prefix
            
            # Remove src/ prefix if present
            if relative_path.startswith('src/'):
                relative_path = relative_path[4:]  # Remove 'src/' prefix
            
            # Get component directory and filename
            component_dir = os.path.dirname(relative_path)
            component_filename = os.path.basename(relative_path)
            folder_name = os.path.basename(base_path)  # Use base_path to get actual folder name
            
            # Smart naming: if filename matches folder name, use README.md
            # Otherwise, use FILENAME.md (uppercase)
            if component_filename.lower() == folder_name.lower():
                doc_filename = "README.md"
                # Use the folder name in the path structure
                output_file = f"docs/react/{relative_path}/README.md"
            else:
                doc_filename = f"{component_filename.upper()}.md"
                output_file = f"docs/react/{component_dir}/{doc_filename}"
            
            output_files.append(output_file)
            
            # If documentation already exists, include it in context for incremental updates
            if os.path.exists(output_file):
                context_files.append(output_file)
    
    elif file_type == "storybook":
        # Storybook: For each component, read .tsx + .config.ts + .stories.tsx, write .stories.tsx
        processed_components = set()
        
        for file in changed_files:
            base_path = get_component_base_path(file)
            if base_path in processed_components:
                continue
            processed_components.add(base_path)
            
            # Get all siblings for context
            siblings = get_component_siblings(file)
            context_files.extend(siblings)
            
            # IMPORTANT: Always include the original component file itself for Storybook
            if file not in context_files:
                context_files.append(file)
            
            # Include workspace configuration files for Storybook (ESLint + Prettier + TypeScript)
            workspace_configs = find_workspace_configs(file, "storybook")
            context_files.extend(workspace_configs)
            
            # Output: modify the .stories.tsx file itself
            # Get component name from the changed file
            file_basename = os.path.splitext(os.path.basename(file))[0]
            # Remove suffixes to get component name
            component_name = file_basename
            for suffix in ['.config', '.stories', '.test']:
                if component_name.endswith(suffix):
                    component_name = component_name[:-len(suffix)]
                    break
            
            # Build correct stories file path: keep the full directory structure
            stories_file = f"{base_path}/{component_name}.stories.tsx"
            if not os.path.exists(stories_file):
                # Try other story extensions
                for ext in ['.stories.ts', '.stories.jsx', '.stories.js']:
                    alt_stories = f"{base_path}/{component_name}{ext}"
                    if os.path.exists(alt_stories):
                        stories_file = alt_stories
                        break
            output_files.append(stories_file)
    
    elif file_type == "sass":
        # Sass: 1:1 mapping, each .scss file → docs/sass/path/file.md
        for file in changed_files:
            context_files.append(file)
            
            # Include workspace configuration files for Sass
            workspace_configs = find_workspace_configs(file, "sass")
            context_files.extend(workspace_configs)
            
            # Generate output path: sass/src/components/button.scss → docs/sass/components/button.md
            base_name = os.path.splitext(os.path.basename(file))[0]
            dir_path = os.path.dirname(file)
            
            # Remove 'sass/' prefix if present
            if dir_path.startswith('sass/'):
                dir_path = dir_path[5:]
            elif dir_path.startswith('./sass/'):
                dir_path = dir_path[7:]
            
            # Remove 'src/' prefix if present (same as React)
            if dir_path.startswith('src/'):
                dir_path = dir_path[4:]
            
            # Smart naming for Sass: if filename matches folder name, use README.md
            folder_name = os.path.basename(dir_path) if dir_path else ""
            if base_name.lower() == folder_name.lower():
                output_file = f"docs/sass/{dir_path}/README.md" if dir_path else f"docs/sass/README.md"
            else:
                output_file = f"docs/sass/{dir_path}/{base_name}.md" if dir_path else f"docs/sass/{base_name}.md"
            
            output_files.append(output_file)
    
    # Remove duplicates while preserving order
    context_files = list(dict.fromkeys(context_files))
    output_files = list(dict.fromkeys(output_files))
    
    return {
        'context_files': context_files,
        'output_files': output_files
    }


def _is_doc_ui_relevant_file(file_path: str) -> bool:
    """
    Check if file is relevant for doc-ui processing.
    
    Args:
        file_path: Path to check
        
    Returns:
        bool: True if file is relevant for doc-ui
    """
    for patterns in DOC_UI_FILE_PATTERNS.values():
        if _matches_file_pattern(file_path, patterns):
            return True
    return False


def run_doc_ui(
    mode: Optional[str] = None,
    doc: str = "all",
    since_commit: Optional[str] = None,
    model_name: Optional[str] = None,
    output_dir: str = "docs",
    path: Optional[str] = None,
    verbose: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Generate documentation for Doc-UI files.
    Following changelog pattern for consistency and error handling.
    
    Args:
        mode: Detection mode ("local", "pipeline", or None for auto-detect)
        doc: Documentation type ("react", "sass", "storybook", "all")
        since_commit: For pipeline mode - compare since this commit
        model_name: AI model to use (default: claude-4-sonnet)
        output_dir: Output directory for documentation
        verbose: Enable verbose output
        dry_run: Preview mode - analyze but don't generate files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if verbose:
            print("🚀 Starting Doc-UI documentation generation...")
            if path:
                print(f"🎯 Path parameter received: {path}")
        
        # Check Git availability (following map_tree pattern)
        if not GIT_AVAILABLE:
            print("❌ Error: Git module not available")
            print("   Doc-UI requires Git for file detection")
            return False
        
        # Get files based on path or mode
        if path:
            all_files = get_files_for_path(path)
            mode = "path"
            if verbose:
                print(f"🎯 Processing specific path: {path}")
                print(f"📊 Found {len(all_files)} files to analyze (ignoring Git status)")
                print(f"📁 Path mode: ALL files in path will be considered for processing")
        else:
            # Auto-detect mode if not specified (following map_tree pattern)
            if mode is None:
                mode = auto_detect_mode()
                if verbose:
                    print(f"🔍 Auto-detected mode: {mode}")
            
            # Get files based on mode using core/git
            all_files = get_files_for_mode(mode, since_commit)
            
            if verbose:
                print(f"📊 Found {len(all_files)} files to analyze")
        
        if not all_files:
            print("📭 No files found to process")
            return True
        
        # Detect file types using our patterns
        categorized_files = detect_file_types(all_files)
        
        if verbose:
            print("📋 File categorization:")
            for file_type, files in categorized_files.items():
                if files:
                    pattern_desc = DOC_UI_FILE_PATTERNS[file_type]["description"]
                    mode_desc = "found in path" if mode == "path" else "changed"
                    print(f"   • {file_type.title()}: {len(files)} files {mode_desc} ({pattern_desc})")
        
        # Filter by doc (following map_tree pattern)
        if doc != "all":
            if doc in categorized_files:
                filtered_files = {doc: categorized_files[doc]}
                categorized_files = {k: v for k, v in filtered_files.items() if v}
            else:
                print(f"❌ Unknown documentation type: {doc}")
                valid_modes = list(DOC_UI_FILE_PATTERNS.keys()) + ["all"]
                print(f"   Valid types: {', '.join(valid_modes)}")
                return False
        
        # Check if we have files to process
        total_files = sum(len(files) for files in categorized_files.values())
        if total_files == 0:
            if mode == "path":
                print(f"📭 No {doc} files found in path: {path}")
                print(f"💡 Tip: Check if the path contains files matching the doc type patterns")
            else:
                print(f"📭 No {doc} files found to process")
            return True
        
        # Select model (following changelog pattern)
        if model_name:
            model = get_model_by_name(model_name)
            if not model:
                print(f"❌ Unknown model: {model_name}")
                return False
            if verbose:
                print(f"🤖 Using specified model: {model.name}")
        else:
            model = get_default_model()
            if verbose:
                print(f"🤖 Using default model: {model.name}")
        
        # Get token limit (following changelog pattern)
        token_limit = get_effective_token_limit("CLAUDE_4_SONNET")
        
        # Setup .tmp directory (following changelog pattern)
        os.makedirs(".tmp", exist_ok=True)
        
        # Clean .tmp directory before starting
        import shutil
        if os.path.exists(".tmp"):
            shutil.rmtree(".tmp")
        os.makedirs(".tmp", exist_ok=True)
        
        if verbose:
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📊 Token limit: {token_limit:,}")
        
        # Dry run mode (following changelog pattern)
        if dry_run:
            print("🔍 DRY RUN MODE - Preview only, NO AI calls (no costs)")
            print(f"📄 Mode: {mode}")
            print(f"📄 Doc type: {doc}")
            print(f"📄 Output directory: {output_dir}")
            print(f"🤖 Would use model: {model.name}")
            print(f"💰 AI costs: $0.00 (dry run - no API calls made)")
            print(f"📁 Working directory: {os.getcwd()}")
            
            # Show prompt files that would be used
            print(f"\n📄 Prompt files to be created:")
            for file_type, files in categorized_files.items():
                if files:
                    prompt_file = f".tmp/doc_ui_{file_type}_prompt.md"
                    print(f"  • {file_type.title()}: {prompt_file}")
            
            print("\n📋 File mapping per type:")
            for file_type, files in categorized_files.items():
                if files:
                    pattern_desc = DOC_UI_FILE_PATTERNS[file_type]["description"]
                    print(f"\n{file_type.title()} ({len(files)} changed) - {pattern_desc}:")
                    
                    # Map files using new sibling detection
                    file_mapping = map_files_for_doc_type(file_type, files)
                    context_files = file_mapping['context_files']
                    output_files = file_mapping['output_files']
                    
                    print(f"  📖 Context files (for reading - {len(context_files)} files):")
                    for ctx_file in context_files:
                        exists = "✅" if os.path.exists(ctx_file) else "❌"
                        print(f"    {exists} {ctx_file}")
                    
                    print(f"  📝 Output files (for writing - {len(output_files)} files):")
                    for out_file in output_files:
                        print(f"    • {out_file}")
                    
                    print(f"  🎯 Original changed files:")
                    for file_path in files:
                        print(f"    • {file_path}")
                    
                    # Show prompt content if verbose
                    if verbose:
                        try:
                            if file_type == "react":
                                from core.ai.prompt_processor import get_react_prompt
                                prompt_content = get_react_prompt()
                            elif file_type == "sass":
                                from core.ai.prompt_processor import get_sass_prompt  
                                prompt_content = get_sass_prompt()
                            elif file_type == "storybook":
                                from core.ai.prompt_processor import get_storybook_prompt
                                prompt_content = get_storybook_prompt()
                            else:
                                prompt_content = f"No prompt available for {file_type}"
                            
                            print(f"  📋 Prompt content preview (first 300 chars):")
                            print("    " + "─" * 60)
                            preview = prompt_content[:300].replace('\n', '\n    ')
                            print(f"    {preview}{'...' if len(prompt_content) > 300 else ''}")
                            print("    " + "─" * 60)
                            
                        except ImportError:
                            print(f"  📋 Prompt: ⚠️ Not available for {file_type}")
                    
                    # Show aider command that would be executed if verbose
                    if verbose:
                        try:
                            from constants.ai import build_aider_command, get_model_name_mapping
                            
                            # Get model key for command template
                            model_map = get_model_name_mapping()
                            model_key = model_map.get(model.name, "CLAUDE_4_SONNET")
                            
                            # Build command that would be executed
                            context_files_str = " ".join(context_files)
                            output_files_str = " ".join(output_files)
                            prompt_file = f".tmp/doc_ui_{file_type}_prompt.md"
                            
                            if file_type == "react":
                                aider_command = build_aider_command(
                                    "DOC_UI_REACT",
                                    model_key,
                                    context_path=context_files_str,
                                    prompt_file=prompt_file,
                                    react_files=output_files_str
                                )
                            elif file_type == "sass":
                                aider_command = build_aider_command(
                                    "DOC_UI_SASS",
                                    model_key,
                                    context_path=context_files_str,
                                    prompt_file=prompt_file,
                                    sass_files=output_files_str
                                )
                            elif file_type == "storybook":
                                aider_command = build_aider_command(
                                    "DOC_UI_STORYBOOK",
                                    model_key,
                                    context_path=context_files_str,
                                    prompt_file=prompt_file,
                                    storybook_files=output_files_str
                                )
                            else:
                                aider_command = f"# No aider command template for {file_type}"
                            
                            print(f"  🔧 Aider command that would be executed:")
                            print("    " + "─" * 60)
                            print(f"    {aider_command}")
                            print("    " + "─" * 60)
                            
                        except ImportError:
                            print(f"  🔧 Aider command: ⚠️ Constants not available")
            
            print("\n✅ Dry run completed - no files generated, no AI costs incurred")
            return True
        
        # Process each file type with AI (following changelog pattern)
        success_count = 0
        total_types = len([t for t, f in categorized_files.items() if f])
        
        for file_type, files in categorized_files.items():
            if not files:
                continue
                
            if verbose:
                print(f"\n🤖 Processing {file_type.title()} files ({len(files)} changed files)...")
            
            # Map changed files to context and output files using sibling detection
            file_mapping = map_files_for_doc_type(file_type, files)
            context_files = file_mapping['context_files']
            output_files = file_mapping['output_files']
            
            if verbose:
                print(f"🎯 Original changed files that triggered this documentation ({len(files)}):")
                for file_path in files:
                    print(f"   • {file_path}")
                
                print(f"📖 Context files for reading ({len(context_files)}):")
                for ctx_file in context_files:
                    exists = "✅" if os.path.exists(ctx_file) else "❌"
                    print(f"   {exists} {ctx_file}")
                
                print(f"📝 Output files for writing ({len(output_files)}):")
                for out_file in output_files:
                    print(f"   • {out_file}")
            
            # Get appropriate prompt for file type
            try:
                if file_type == "react":
                    from core.ai.prompt_processor import get_react_prompt
                    prompt_content = get_react_prompt()
                elif file_type == "sass":
                    from core.ai.prompt_processor import get_sass_prompt  
                    prompt_content = get_sass_prompt()
                elif file_type == "storybook":
                    from core.ai.prompt_processor import get_storybook_prompt
                    prompt_content = get_storybook_prompt()
                else:
                    print(f"⚠️ No prompt available for {file_type}, skipping...")
                    continue
            except ImportError:
                print(f"⚠️ Prompt processor not available for {file_type}, skipping...")
                continue
            
            # Create prompt file in .tmp/
            prompt_file = f".tmp/doc_ui_{file_type}_prompt.md"
            with open(prompt_file, 'w') as f:
                f.write(prompt_content)
            
            # Calculate token usage using context files (files that will be read)
            prompt_tokens = count_tokens(prompt_content)
            
            # Calculate context file tokens
            total_context_tokens = 0
            for ctx_file in context_files:
                try:
                    with open(ctx_file, 'r') as f:
                        content = f.read()
                    total_context_tokens += count_tokens(content)
                except:
                    continue
            
            # Total estimated input tokens
            estimated_input_tokens = prompt_tokens + total_context_tokens
            
            if verbose:
                print(f"📊 Token breakdown for {file_type}:")
                print(f"   • Prompt tokens: {prompt_tokens:,}")
                print(f"   • Context files tokens: {total_context_tokens:,}")
                print(f"   • Total estimated input: {estimated_input_tokens:,}")
                print(f"   • Token limit: {token_limit:,}")
                print(f"   • Efficiency: {(estimated_input_tokens/token_limit)*100:.1f}% of limit used")
            
            # Check if within token limits
            if estimated_input_tokens > token_limit:
                print(f"⚠️ {file_type.title()} files exceed token limit ({estimated_input_tokens:,} > {token_limit:,})")
                print("   Consider processing fewer components or using a different approach")
                continue
            
            # Prepare strings for aider (following changelog pattern)
            context_files_str = " ".join(context_files)
            output_files_str = " ".join(output_files)
            
            # Create output directories
            for output_file in output_files:
                output_dir_path = os.path.dirname(output_file)
                if output_dir_path:
                    os.makedirs(output_dir_path, exist_ok=True)
            
            if verbose:
                print(f"🤖 Running AI generation for {file_type}...")
                print(f"📁 Working directory: {os.getcwd()}")
                print(f"📄 Prompt file: {prompt_file} (exists: {os.path.exists(prompt_file)})")
                print(f"📖 Context files: {context_files_str}")
                print(f"📝 Output files: {output_files_str}")
            
            # Run AI generation using aider interface (following changelog pattern)
            try:
                # Import the specific doc-ui generation function
                from core.ai.aider_interface import run_doc_ui_generation
                
                result = run_doc_ui_generation(
                    model=model,
                    file_type=file_type,
                    files=context_files,  # Files to read for context
                    prompt_file=prompt_file,
                    output_dir=output_files,  # Files to write/modify
                    verbose=verbose  # Pass verbose flag to aider interface
                )
                
                if result.success:
                    success_count += 1
                    if verbose:
                        print(f"✅ {file_type.title()} documentation generated successfully")
                        if result.output:
                            print(f"📄 AI Output preview: {result.output[:200]}...")
                else:
                    print(f"❌ Failed to generate {file_type} documentation: {result.error}")
                    if verbose and result.command:
                        print(f"🔧 Command: {result.command}")
                        
            except ImportError:
                print(f"⚠️ AI generation not available for {file_type} yet")
                print("🚧 Doc-UI AI interface under development")
            except Exception as e:
                print(f"❌ Error processing {file_type}: {e}")
        
        # Move Aider history files to .tmp for pipeline artifacts (following changelog pattern)
        import shutil
        aider_files = [".aider.chat.history.md", ".aider.input.history"]
        for aider_file in aider_files:
            if os.path.exists(aider_file):
                dest_file = f".tmp/{aider_file}"
                shutil.move(aider_file, dest_file)
                if verbose:
                    print(f"📦 Moved Aider history to artifacts: {aider_file} → {dest_file}")
        
        # Final results
        if success_count == total_types:
            print(f"✅ All documentation generated successfully!")
            print(f"📁 Output directory: {output_dir}")
            return True
        elif success_count > 0:
            print(f"⚠️ Partial success: {success_count}/{total_types} file types processed")
            print(f"📁 Output directory: {output_dir}")
            return True
        else:
            print("❌ No documentation was generated")
            return False
                
    except Exception as e:
        print(f"❌ Error generating Doc-UI documentation: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False


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


def add_doc_ui_arguments(parser):
    """
    Add doc-ui specific arguments to argument parser.
    Following map_tree pattern for consistency.
    
    Args:
        parser: ArgumentParser instance
    """
    parser.add_argument(
        '--mode',
        choices=['local', 'pipeline'],
        help='File detection mode (default: auto-detect based on git status)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        help='Process specific directory/file path instead of git changes'
    )
    
    parser.add_argument(
        '--doc',
        choices=['react', 'sass', 'storybook', 'all'],
        default='all',
        help='Documentation type to generate (default: all)'
    )
    
    parser.add_argument(
        '--since',
        type=str,
        help='For pipeline mode: generate docs for files changed since this commit'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='AI model to use (default: claude-4-sonnet)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='docs',
        help='Output directory for documentation (default: docs)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview mode - analyze files but don\'t generate documentation (no AI costs)'
    )


def get_doc_ui_help() -> str:
    """Get help text for doc-ui command."""
    return """
Generate AI-powered documentation for React, Sass, and Storybook files.

Examples:
  codex-ai doc-ui                         # Auto-detect mode, all file types
  codex-ai doc-ui --local                 # Local mode: staged/modified files
  codex-ai doc-ui --pipeline              # Pipeline mode: changed files since origin/main
  codex-ai doc-ui --path react/src/components/Button  # Process specific path
  codex-ai doc-ui --path react/src/components/ --doc react  # Path + doc filter
  codex-ai doc-ui --doc react             # Only React components
  codex-ai doc-ui --doc sass              # Only Sass files
  codex-ai doc-ui --doc storybook         # Only Storybook stories
  codex-ai doc-ui --since HEAD~5         # Pipeline: files changed in last 5 commits
  codex-ai doc-ui --dry-run               # Preview without AI costs
  codex-ai doc-ui --verbose               # Detailed output

Mode Detection:
  • Auto-detect: Uses 'local' if staged/modified files exist, 'pipeline' otherwise
  • Local mode: Processes staged and modified files (git status)
  • Pipeline mode: Processes files changed since specified commit or origin/main
  • Path mode: Process specific directory/file path (overrides mode detection)

File Types:
  • React: .tsx/.jsx/.ts/.js files in components/src (excludes tests, .d.ts)
  • Sass: .scss/.sass/.css files (excludes .min, .map files)  
  • Storybook: .stories.tsx/.jsx/.ts/.js files

Cross-Type Triggers:
  • Component.tsx modified → React + Storybook docs (if stories exist)
  • Component.stories.tsx modified → Storybook docs only
  • Component.scss modified → Sass docs only

The doc-ui command uses AI to generate comprehensive documentation for your
components and styles, automatically detecting file types and changes with
intelligent sibling file detection.
"""
