"""
Doc-Gen documentation command implementation.

Generates generic documentation for any project/language using AI with intelligent
file detection, mode selection, and preset filtering. Supports both simple and detailed
documentation modes with separated or inline output strategies.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Core imports
from core.git import auto_detect_mode, get_files_for_mode, get_files_for_path, FileDetector
from core.ai.model_selector import get_default_model, get_model_by_name
from core.ai.token_manager import count_tokens
from core.config import CodexConfig
from core import GIT_AVAILABLE

# Constants imports
from constants.ai import get_effective_token_limit, build_aider_command, get_model_name_mapping
from constants.output import EMOJIS, format_with_emoji
from core.ai.prompt_processor import load_prompt

# Use the new generic method with DOC_GEN template flags
from core.ai.aider_interface import AiderInterface
from constants.ai import AIDER_COMMAND_TEMPLATES

# ===== DOC-GEN PRESETS =====
#
# 📊 EXPLANATION:
# File extension and exclusion patterns for different language presets.
# These can be combined or used individually to filter relevant files.

DOC_GEN_PRESETS = {
    "python": {
        "extensions": [".py", ".pyi", ".yaml", ".toml"],
        "exclude": ["*.pyc", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info", "__init__.py"],
        "description": "Python files and configuration"
    },
    "javascript": {
        "extensions": [".js", ".ts", ".jsx", ".tsx", ".json", ".mjs"],
        "exclude": ["node_modules", "*.min.js", "*.min.css", "*.map", "build", "dist", ".next", "index.js", "index.jsx", "index.ts", "index.tsx"],
        "description": "JavaScript/TypeScript files and configuration"
    },
    "generic": {
        "extensions": [".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".bash"],
        "exclude": [".git", ".tmp", "*.log", ".DS_Store", "Thumbs.db", ".vscode", ".idea", "__init__.py"],
        "description": "Documentation and configuration files"
    }
}

# ===== DOC-GEN DEFAULTS =====
#
# 📊 EXPLANATION:
# Default configuration values for doc-gen command.
# Following the same pattern as doc-ui but adapted for generic documentation.

DOC_GEN_DEFAULTS = {
    "docs_dir": "docs/",
    "strip_prefixes": ["src/"],
    "mode": "simple",
    "preset": None,  # None means merge all presets
    "shallow": False
}

# ===== DOC-GEN TEMPLATES =====
#
# 📊 EXPLANATION:
# Template paths for different documentation types.
# These correspond to the prompt files created in templates/prompts/

DOC_GEN_TEMPLATES = {
    "folder_readme": "templates/prompts/doc_gen_folder_readme_prompt.md",
    "folder_index": "templates/prompts/doc_gen_folder_index_prompt.md",
    "file_detailed": "templates/prompts/doc_gen_file_detailed_prompt.md"
}

# ===== DOC-GEN CLI CHOICES =====
#
# 📊 EXPLANATION:
# Valid choices for CLI arguments.
# Used by argument parser for validation.

DOC_GEN_CLI_CHOICES = {
    "modes": ["simple", "detailed"],
    "presets": ["python", "javascript"]  # generic sempre incluído automaticamente
}

# ===== DOC-GEN VALIDATION =====
#
# 📊 EXPLANATION:
# Validation limits and supported file types.
# Prevents excessive API usage and ensures quality output.

DOC_GEN_VALIDATION = {
    "max_files_per_run": 100,  # Evitar requests excessivos
    "supported_extensions": [
        ".py", ".pyi", ".js", ".ts", ".jsx", ".tsx", ".json", ".mjs",
        ".md", ".txt", ".yaml", ".yml", ".sh", ".bash", ".toml"
    ]
}


# ===== DOC-GEN AI GENERATION FUNCTIONS =====

def generate_folder_readme(
    folder_path: str,
    folder_files: List[str], 
    readme_path: str,
    strategy: str,
    model,
    verbose: bool = False
) -> bool:
    """Generate README.md for a folder using AI."""
    try:
        # Load template content
        template_content = load_prompt("doc_gen_folder_readme_prompt")
        
        # Fill template variables like changelog does with version context
        file_index_content = "\n".join([f"- **{os.path.basename(f)}**: [Description will be generated based on file content]" for f in folder_files])
        
        filled_template = template_content.format(
            folder_path=folder_path,
            docs_strategy=strategy,
            folder_files=", ".join([os.path.basename(f) for f in folder_files]),
            file_contents="Files will be read by Aider for context",
            file_index_content=file_index_content
        )
        
        # Create prompt file with filled template
        prompt_file = f".tmp/doc_gen_folder_readme_{folder_path.replace('/', '_')}.md"
        with open(prompt_file, 'w') as f:
            f.write(filled_template)
        
        if verbose:
            print(f"📝 Generating README: {readme_path}")
            print(f"📄 Prompt file: {prompt_file}")
            
            # Calculate token usage like doc-ui does
            prompt_tokens = count_tokens(filled_template)
            
            # Calculate context file tokens
            total_context_tokens = 0
            for ctx_file in folder_files:
                try:
                    with open(ctx_file, 'r') as f:
                        content = f.read()
                    total_context_tokens += count_tokens(content)
                except:
                    continue
            
            # Total estimated input tokens
            estimated_input_tokens = prompt_tokens + total_context_tokens
            token_limit = get_effective_token_limit("CLAUDE_4_SONNET")
            
            print(f"📊 Token breakdown for README generation:")
            print(f"   • Prompt tokens: {prompt_tokens:,}")
            print(f"   • Context files tokens: {total_context_tokens:,}")
            print(f"   • Total estimated input: {estimated_input_tokens:,}")
            print(f"   • Token limit: {token_limit:,}")
            print(f"   • Efficiency: {(estimated_input_tokens/token_limit)*100:.1f}% of limit used")
            
            print(f"📖 Context files for reading ({len(folder_files)}):")
            for ctx_file in folder_files:
                exists = "✅" if os.path.exists(ctx_file) else "❌"
                print(f"   {exists} {ctx_file}")
        
        # Run AI generation using aider interface (following changelog/doc-ui pattern)
        aider = AiderInterface(model)
        template = AIDER_COMMAND_TEMPLATES["DOC_GEN"]
        
        if verbose:
            print(f"🤖 Running AI generation for folder README...")
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📄 Prompt file: {prompt_file} (exists: {os.path.exists(prompt_file)})")
            print(f"📖 Context files: {' '.join(folder_files)}")
            print(f"📝 Output file: {readme_path}")
        
        result = aider.run_with_message_file(
            prompt_file=prompt_file,
            read_files=folder_files,
            output_files=[readme_path],
            additional_flags=template["additional_flags"],
            verbose=verbose
        )
        
        if result.success:
            if verbose:
                print(f"✅ README documentation generated successfully")
                if result.output:
                    print(f"📄 AI Output preview: {result.output[:200]}{'...' if len(result.output) > 200 else ''}")
            return True
        else:
            print(f"❌ Failed to generate README: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating folder README: {e}")
        return False


def generate_folder_index(
    folder_path: str,
    folder_files: List[str],
    file_docs: Dict[str, str],
    index_path: str,
    model,
    verbose: bool = False
) -> bool:
    """Generate INDEX.md for inline documentation strategy."""
    try:
        # Load folder INDEX template
        template_content = load_prompt("doc_gen_folder_index_prompt")
        
        # Fill template variables like folder README does
        documentation_files = list(file_docs.values()) if file_docs else []
        file_summaries = []
        for filename, doc_path in file_docs.items():
            file_summaries.append(f"- **{filename}**: Documentation at {os.path.basename(doc_path)}")
        
        filled_template = template_content.format(
            folder_path=folder_path,
            folder_files=", ".join([os.path.basename(f) for f in folder_files]),
            documentation_files=", ".join([os.path.basename(f) for f in documentation_files]),
            file_summaries="\n".join(file_summaries) if file_summaries else "No file documentation generated"
        )
        
        # Create prompt file with filled template
        prompt_file = f".tmp/doc_gen_folder_index_{folder_path.replace('/', '_')}.md"
        with open(prompt_file, 'w') as f:
            f.write(filled_template)
        
        if verbose:
            print(f"📋 Generating INDEX: {index_path}")
        
        aider = AiderInterface(model)
        template = AIDER_COMMAND_TEMPLATES["DOC_GEN"]
        
        result = aider.run_with_message_file(
            prompt_file=prompt_file,
            read_files=folder_files,
            output_files=[index_path],
            additional_flags=template["additional_flags"],
            verbose=verbose
        )
        
        if result.success:
            if verbose:
                print(f"✅ Generated INDEX: {index_path}")
            return True
        else:
            print(f"❌ Failed to generate INDEX: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating folder INDEX: {e}")
        return False


def generate_file_documentation(
    file_path: str,
    doc_path: str,
    folder_path: str,
    model,
    verbose: bool = False
) -> bool:
    """Generate detailed documentation for individual file."""
    try:
        # Load file detailed template
        template_content = load_prompt("doc_gen_file_detailed_prompt")
        
        # Fill template variables like folder README does
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1]
        
        # Get related files in the same folder (siblings)
        try:
            folder_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            related_files = [f for f in folder_files if f != filename][:5]  # Limit to 5 related files
            related_files_str = ", ".join(related_files) if related_files else "None"
        except:
            related_files_str = "None"
        
        filled_template = template_content.format(
            file_path=file_path,
            file_extension=file_extension,
            file_contents="File content will be read by Aider for context",
            related_files=related_files_str,
            folder_context=f"Part of {folder_path} directory"
        )
        
        # Create prompt file with filled template
        prompt_file = f".tmp/doc_gen_file_{filename.replace('.', '_')}.md"
        with open(prompt_file, 'w') as f:
            f.write(filled_template)
        
        if verbose:
            print(f"📄 Generating file doc: {doc_path}")
        
        aider = AiderInterface(model)
        template = AIDER_COMMAND_TEMPLATES["DOC_GEN"]
        
        result = aider.run_with_message_file(
            prompt_file=prompt_file,
            read_files=[file_path],
            output_files=[doc_path],
            additional_flags=template["additional_flags"],
            verbose=verbose
        )
        
        if result.success:
            if verbose:
                print(f"✅ Generated file doc: {doc_path}")
            return True
        else:
            print(f"❌ Failed to generate file doc: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating file documentation: {e}")
        return False


# ===== DOC-GEN CORE FUNCTIONS =====

def get_default_filters() -> Dict[str, Any]:
    """
    Get default filters by merging all presets.
    
    Returns:
        Dict with merged extensions and excludes from all presets
        
    Examples:
        >>> filters = get_default_filters()
        >>> print(len(filters["extensions"]))
        11  # All extensions from python + javascript + generic
    """
    all_extensions = []
    all_excludes = []
    
    for preset_name, preset_config in DOC_GEN_PRESETS.items():
        all_extensions.extend(preset_config["extensions"])
        all_excludes.extend(preset_config["exclude"])
    
    # Remove duplicates while preserving order
    unique_extensions = list(dict.fromkeys(all_extensions))
    unique_excludes = list(dict.fromkeys(all_excludes))
    
    return {
        "extensions": unique_extensions,
        "exclude": unique_excludes,
        "description": "All presets (python + javascript + generic)"
    }


def get_preset_filters(preset_name: Optional[str]) -> Dict[str, Any]:
    """
    Get filters for specific preset or default merge.
    
    Args:
        preset_name: Name of preset or None for default merge
        
    Returns:
        Dict with extensions and excludes for the preset
        
    Examples:
        >>> filters = get_preset_filters("python")
        >>> print(filters["extensions"])
        ['.py', '.pyi', '.yaml', '.toml', '.md', '.txt', ...]  # python + generic
    """
    if preset_name is None:
        return get_default_filters()
    
    if preset_name not in DOC_GEN_PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}. Valid presets: {list(DOC_GEN_PRESETS.keys())}")
    
    # Always include generic preset
    preset_config = DOC_GEN_PRESETS[preset_name].copy()
    generic_config = DOC_GEN_PRESETS["generic"]
    
    # Merge with generic
    merged_extensions = preset_config["extensions"] + generic_config["extensions"]
    merged_excludes = preset_config["exclude"] + generic_config["exclude"]
    
    # Remove duplicates while preserving order
    unique_extensions = list(dict.fromkeys(merged_extensions))
    unique_excludes = list(dict.fromkeys(merged_excludes))
    
    return {
        "extensions": unique_extensions,
        "exclude": unique_excludes,
        "description": f"{preset_name} + generic files"
    }


def detect_doc_gen_files(
    files: List[str], 
    preset: Optional[str] = None,
    custom_extensions: Optional[List[str]] = None,
    custom_excludes: Optional[List[str]] = None
) -> List[str]:
    """
    Filter files based on doc-gen criteria.
    
    Args:
        files: List of file paths to filter
        preset: Preset name or None for default
        custom_extensions: Custom extensions to override preset
        custom_excludes: Custom excludes to override preset
        
    Returns:
        Filtered list of relevant files
        
    Examples:
        >>> files = ["src/main.py", "node_modules/lib.js", "README.md"]
        >>> filtered = detect_doc_gen_files(files, preset="python")
        >>> print(filtered)
        ['src/main.py', 'README.md']  # node_modules excluded
    """
    if not files:
        return []
    
    # Get filters from preset or custom
    if custom_extensions:
        extensions = custom_extensions
    else:
        filters = get_preset_filters(preset)
        extensions = filters["extensions"]
    
    if custom_excludes:
        excludes = custom_excludes
    else:
        filters = get_preset_filters(preset) if not custom_extensions else {"exclude": []}
        excludes = filters["exclude"]
    
    relevant_files = []
    
    for file_path in files:
        if not file_path:
            continue
        
        # Check if file exists
        if not os.path.exists(file_path):
            continue
        
        # Check extensions
        if not any(file_path.endswith(ext) for ext in extensions):
            continue
        
        # Check excludes (patterns in path)
        if any(exclude_pattern in file_path for exclude_pattern in excludes):
            continue
        
        relevant_files.append(file_path)
    
    return relevant_files


def determine_output_strategy(docs_dir: str) -> Tuple[str, bool]:
    """
    Determine output strategy based on docs_dir parameter.
    
    Args:
        docs_dir: Documentation directory path
        
    Returns:
        Tuple of (strategy_name, is_inline)
        
    Examples:
        >>> strategy, inline = determine_output_strategy("docs/")
        >>> print(strategy, inline)
        ('separated', False)
        
        >>> strategy, inline = determine_output_strategy("./docs/")
        >>> print(strategy, inline) 
        ('inline', True)
    """
    # Normalize path
    normalized = os.path.normpath(docs_dir)
    
    # Check for inline indicators
    if normalized.startswith("./") or normalized.startswith("../"):
        return ("inline", True)
    
    # Default to separated
    return ("separated", False)


def map_output_paths(
    files: List[str],
    mode: str,
    docs_dir: str,
    strip_prefixes: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Map input files to output documentation paths.
    
    Args:
        files: List of input file paths
        mode: Documentation mode ('simple' or 'detailed')
        docs_dir: Documentation directory
        strip_prefixes: List of prefixes to remove from paths
        
    Returns:
        Dict mapping folder paths to their documentation info
        
    Examples:
        >>> files = ["src/utils/helpers.py", "src/utils/db.py"]
        >>> mapping = map_output_paths(files, "detailed", "docs/", ["src/"])
        >>> print(mapping["utils"])
        {
            'folder_path': 'src/utils',
            'files': ['src/utils/helpers.py', 'src/utils/db.py'],
            'readme_path': 'docs/utils/README.md',
            'index_path': 'docs/utils/docs/INDEX.md',
            'file_docs': {'helpers.py': 'docs/utils/docs/helpers.md', ...}
        }
    """
    if not files:
        return {}
    
    strategy, is_inline = determine_output_strategy(docs_dir)
    strip_prefixes = strip_prefixes or DOC_GEN_DEFAULTS["strip_prefixes"]
    
    # Group files by folder
    folder_groups = {}
    for file_path in files:
        folder = os.path.dirname(file_path)
        if folder not in folder_groups:
            folder_groups[folder] = []
        folder_groups[folder].append(file_path)
    
    # Map each folder to its documentation structure
    output_mapping = {}
    
    for folder_path, folder_files in folder_groups.items():
        # Strip prefixes from folder path for output
        clean_folder = folder_path
        for prefix in strip_prefixes:
            if clean_folder.startswith(prefix):
                clean_folder = clean_folder[len(prefix):]
                break
        
        # Remove leading slash if present
        clean_folder = clean_folder.lstrip("/")
        
        if is_inline:
            # Inline strategy: src/utils/docs/
            readme_path = os.path.join(folder_path, "README.md")
            docs_subdir = os.path.join(folder_path, "docs")
            index_path = os.path.join(docs_subdir, "INDEX.md")
        else:
            # Separated strategy: docs/src/utils/
            output_folder = os.path.join(docs_dir, clean_folder) if clean_folder else docs_dir
            readme_path = os.path.join(output_folder, "README.md")
            docs_subdir = output_folder
            index_path = None  # No separate INDEX.md in separated mode
        
        # Map individual file documentation
        file_docs = {}
        if mode == "detailed":
            for file_path in folder_files:
                filename = os.path.basename(file_path)
                base_name = os.path.splitext(filename)[0]
                doc_filename = f"{base_name}.md"
                
                if is_inline:
                    doc_path = os.path.join(docs_subdir, doc_filename)
                else:
                    doc_path = os.path.join(docs_subdir, doc_filename)
                
                file_docs[filename] = doc_path
        
        output_mapping[clean_folder or "."] = {
            "folder_path": folder_path,
            "files": folder_files,
            "readme_path": readme_path,
            "index_path": index_path,
            "file_docs": file_docs,
            "strategy": strategy
        }
    
    return output_mapping


def run_doc_gen(
    mode: str,
    git_mode: Optional[str] = None,
    path: Optional[str] = None,
    shallow: bool = False,
    docs_dir: str = "docs/",
    strip_prefix: Optional[str] = None,
    preset: Optional[str] = None,
    ext: Optional[str] = None,
    exclude: Optional[str] = None,
    since_commit: Optional[str] = None,
    model_name: Optional[str] = None,
    verbose: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Generate documentation for files using doc-gen.
    
    Args:
        mode: Documentation mode ('simple' or 'detailed')
        git_mode: Git detection mode ('local', 'pipeline', or None for auto-detect)
        path: Specific directory/file path to process
        shallow: Process only immediate directory (no recursion)
        docs_dir: Output directory for documentation
        strip_prefix: Comma-separated prefixes to remove from paths
        preset: File preset to use ('python', 'javascript', or None for all)
        ext: Comma-separated custom extensions (overrides preset)
        exclude: Comma-separated custom exclusions (overrides preset)
        since_commit: For pipeline mode - compare since this commit
        model_name: AI model to use
        verbose: Enable verbose output
        dry_run: Preview mode - analyze but don't generate files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = CodexConfig()
        verbose = verbose or config.get_verbose()
        
        if verbose:
            print(f"🚀 Starting Doc-Gen documentation generation...")
            print(f"📋 Mode: {mode}")
            if path:
                print(f"🎯 Path parameter received: {path}")
        
        # Validate mode
        if mode not in DOC_GEN_CLI_CHOICES["modes"]:
            print(f"❌ Invalid mode: {mode}")
            valid_modes = DOC_GEN_CLI_CHOICES["modes"]
            print(f"   Valid modes: {', '.join(valid_modes)}")
            return False
        
        # Check Git availability
        if not GIT_AVAILABLE and not path:
            print("❌ Error: Git module not available")
            print("   Doc-Gen requires Git for file detection, or use --path for specific directories")
            return False
        
        # Parse custom arguments
        custom_extensions = None
        if ext:
            custom_extensions = [e.strip() for e in ext.split(",") if e.strip()]
        
        custom_excludes = None
        if exclude:
            custom_excludes = [e.strip() for e in exclude.split(",") if e.strip()]
        
        strip_prefixes = DOC_GEN_DEFAULTS["strip_prefixes"]
        if strip_prefix:
            strip_prefixes = [p.strip() for p in strip_prefix.split(",") if p.strip()]
        
        # Get files based on path or git mode using classes (not convenience functions)
        detector = FileDetector()
        
        if path:
            all_files = detector.get_files_for_path(path, shallow=shallow)
            git_mode = "path"
            if verbose:
                print(f"🎯 Processing specific path: {path}")
                print(f"📊 Found {len(all_files)} files to analyze (ignoring Git status)")
                shallow_desc = "non-recursive" if shallow else "recursive"
                print(f"📁 Path mode: {shallow_desc} scan")
        else:
            # Auto-detect git mode if not specified
            if git_mode is None:
                git_mode = detector.auto_detect_mode()
                if verbose:
                    print(f"🔍 Auto-detected Git mode: {git_mode}")
            
            # Get files based on git mode
            all_files = detector.get_files_for_mode(git_mode, since_commit)
            
            if verbose:
                print(f"📊 Found {len(all_files)} files to analyze from Git {git_mode} mode")
        
        if not all_files:
            if path:
                print(f"📭 No files found in path: {path}")
            else:
                print("📭 No files found to process")
            return True
        
        # Filter files using doc-gen criteria
        relevant_files = detect_doc_gen_files(
            all_files,
            preset=preset,
            custom_extensions=custom_extensions,
            custom_excludes=custom_excludes
        )
        
        if verbose:
            # Show filtering results
            filters = get_preset_filters(preset) if not custom_extensions else {"description": "custom"}
            filter_desc = filters.get("description", "custom filters")
            
            print(f"🔍 File filtering:")
            print(f"   • Filter: {filter_desc}")
            print(f"   • Total files found: {len(all_files)}")
            print(f"   • Relevant files: {len(relevant_files)}")
            
            if custom_extensions:
                print(f"   • Custom extensions: {', '.join(custom_extensions)}")
            if custom_excludes:
                print(f"   • Custom exclusions: {', '.join(custom_excludes)}")
        
        if not relevant_files:
            filter_info = f"preset '{preset}'" if preset else "default filters"
            if custom_extensions:
                filter_info = f"extensions {', '.join(custom_extensions)}"
            print(f"📭 No relevant files found for {filter_info}")
            return True
        
        # Validate file count
        max_files = DOC_GEN_VALIDATION["max_files_per_run"]
        if len(relevant_files) > max_files:
            print(f"⚠️ Too many files to process: {len(relevant_files)} > {max_files}")
            print(f"   Consider using --path to process specific directories")
            print(f"   or --preset to filter to specific file types")
            return False
        
        # Map output paths
        output_mapping = map_output_paths(
            relevant_files,
            mode,
            docs_dir,
            strip_prefixes
        )
        
        if verbose:
            strategy_name = determine_output_strategy(docs_dir)[0]
            print(f"🗂️ Output mapping:")
            print(f"   • Strategy: {strategy_name}")
            print(f"   • Docs directory: {docs_dir}")
            print(f"   • Strip prefixes: {', '.join(strip_prefixes)}")
            print(f"   • Folders to document: {len(output_mapping)}")
        
        # Select model
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
        
        # Get token limit
        token_limit = get_effective_token_limit("CLAUDE_4_SONNET")
        
        # Setup .tmp directory
        os.makedirs(".tmp", exist_ok=True)
        
        # Clean .tmp directory before starting
        if os.path.exists(".tmp"):
            shutil.rmtree(".tmp")
        os.makedirs(".tmp", exist_ok=True)
        
        if verbose:
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📊 Token limit: {token_limit:,}")
        
        # Dry run mode
        if dry_run:
            print("🔍 DRY RUN MODE - Preview only, NO AI calls (no costs)")
            print(f"📄 Mode: {mode} documentation")
            print(f"📄 Git mode: {git_mode}")
            print(f"📄 Output directory: {docs_dir}")
            print(f"🤖 Would use model: {model.name}")
            print(f"💰 AI costs: $0.00 (dry run - no API calls made)")
            print(f"📁 Working directory: {os.getcwd()}")
            
            # Show files being processed
            filter_desc = get_preset_filters(preset).get("description", "custom") if not custom_extensions else "custom"
            print(f"\n📋 Files to process ({len(relevant_files)} files, {filter_desc}):")
            for file_path in relevant_files:
                exists = "✅" if os.path.exists(file_path) else "❌"
                print(f"  {exists} {file_path}")
            
            # Show output mapping
            print(f"\n🗂️ Documentation structure ({mode} mode):")
            strategy_name = determine_output_strategy(docs_dir)[0]
            print(f"   Strategy: {strategy_name}")
            
            for folder_key, folder_info in output_mapping.items():
                folder_path = folder_info["folder_path"]
                files_count = len(folder_info["files"])
                print(f"\n  📁 {folder_path} ({files_count} files):")
                print(f"     📝 README: {folder_info['readme_path']}")
                
                if folder_info["index_path"]:
                    print(f"     📋 INDEX: {folder_info['index_path']}")
                
                if mode == "detailed" and folder_info["file_docs"]:
                    print(f"     📄 File docs ({len(folder_info['file_docs'])}):")
                    for filename, doc_path in folder_info["file_docs"].items():
                        print(f"        • {filename} → {doc_path}")
            
            if verbose:
                # Show which templates would be used
                print(f"\n📋 Templates that would be used:")
                print(f"   • Folder README: {DOC_GEN_TEMPLATES['folder_readme']}")
                if any(info["index_path"] for info in output_mapping.values()):
                    print(f"   • Folder INDEX: {DOC_GEN_TEMPLATES['folder_index']}")
                if mode == "detailed":
                    print(f"   • File detailed: {DOC_GEN_TEMPLATES['file_detailed']}")
                
                # Show prompt content preview for each folder
                print(f"\n📋 Prompt previews and commands:")
                for folder_key, folder_info in output_mapping.items():
                    folder_path = folder_info["folder_path"]
                    folder_files = folder_info["files"]
                    strategy = folder_info["strategy"]
                    
                    print(f"\n  📁 {folder_path}:")
                    
                    # Load and fill template to show preview
                    try:
                        template_content = load_prompt("doc_gen_folder_readme_prompt")
                        file_index_content = "\n".join([f"- **{os.path.basename(f)}**: [Description will be generated based on file content]" for f in folder_files])
                        
                        filled_template = template_content.format(
                            folder_path=folder_path,
                            docs_strategy=strategy,
                            folder_files=", ".join([os.path.basename(f) for f in folder_files]),
                            file_contents="Files will be read by Aider for context",
                            file_index_content=file_index_content
                        )
                        
                        print(f"    📋 Prompt content preview (first 300 chars):")
                        print("    " + "─" * 60)
                        preview = filled_template[:300].replace('\n', '\n    ')
                        print(f"    {preview}{'...' if len(filled_template) > 300 else ''}")
                        print("    " + "─" * 60)
                        
                        # Show aider command that would be executed
                        try:
                            from constants.ai import build_aider_command, get_model_name_mapping
                            
                            model_map = get_model_name_mapping()
                            model_key = model_map.get(model.name, "CLAUDE_4_SONNET")
                            
                            prompt_file = f".tmp/doc_gen_folder_readme_{folder_path.replace('/', '_')}.md"
                            context_files_str = " ".join(folder_files)
                            readme_path = folder_info["readme_path"]
                            
                            aider_command = build_aider_command(
                                "DOC_GEN",
                                model_key,
                                context_files=context_files_str,
                                prompt_file=prompt_file,
                                output_file=readme_path
                            )
                            
                            print(f"    🔧 Aider command that would be executed:")
                            print("    " + "─" * 60)
                            print(f"    {aider_command}")
                            print("    " + "─" * 60)
                            
                        except Exception:
                            print(f"    🔧 Aider command: ⚠️ Preview not available")
                        
                    except Exception:
                        print(f"    📋 Prompt preview: ⚠️ Not available")
            
            print("\n✅ Dry run completed - no files generated, no AI costs incurred")
            return True
        
        # Generate documentation using AI
        if verbose:
            print(f"🤖 Starting AI documentation generation...")
        
        success_count = 0
        total_folders = len(output_mapping)
        
        for folder_key, folder_info in output_mapping.items():
            folder_path = folder_info["folder_path"]
            folder_files = folder_info["files"]
            readme_path = folder_info["readme_path"]
            index_path = folder_info["index_path"]
            file_docs = folder_info["file_docs"]
            strategy = folder_info["strategy"]
            
            if verbose:
                print(f"\n📁 Processing folder: {folder_path} ({len(folder_files)} files)")
                print(f"🎯 Original changed files that triggered this documentation:")
                for file_path in folder_files:
                    print(f"   • {file_path}")
                
                print(f"📝 Output files for writing:")
                print(f"   • README: {readme_path}")
                if index_path:
                    print(f"   • INDEX: {index_path}")
                if mode == "detailed" and file_docs:
                    print(f"   • File docs ({len(file_docs)}):")
                    for filename, doc_path in file_docs.items():
                        print(f"        • {filename} → {doc_path}")
            
            # Create output directories
            os.makedirs(os.path.dirname(readme_path), exist_ok=True)
            if index_path:
                os.makedirs(os.path.dirname(index_path), exist_ok=True)
            for doc_path in file_docs.values():
                os.makedirs(os.path.dirname(doc_path), exist_ok=True)
            
            # Check token limits before generation
            if verbose:
                try:
                    template_content = load_prompt("doc_gen_folder_readme_prompt")
                    file_index_content = "\n".join([f"- **{os.path.basename(f)}**: [Description will be generated based on file content]" for f in folder_files])
                    
                    filled_template = template_content.format(
                        folder_path=folder_path,
                        docs_strategy=strategy,
                        folder_files=", ".join([os.path.basename(f) for f in folder_files]),
                        file_contents="Files will be read by Aider for context",
                        file_index_content=file_index_content
                    )
                    
                    prompt_tokens = count_tokens(filled_template)
                    total_context_tokens = 0
                    for ctx_file in folder_files:
                        try:
                            with open(ctx_file, 'r') as f:
                                content = f.read()
                            total_context_tokens += count_tokens(content)
                        except:
                            continue
                    
                    estimated_input_tokens = prompt_tokens + total_context_tokens
                    
                    if estimated_input_tokens > token_limit:
                        print(f"⚠️ {folder_path} files exceed token limit ({estimated_input_tokens:,} > {token_limit:,})")
                        print("   Consider processing fewer files or using a different approach")
                        continue
                        
                except Exception:
                    pass  # Continue if token check fails
            
            # Generate folder README.md
            try:
                folder_readme_success = generate_folder_readme(
                    folder_path, folder_files, readme_path, strategy, model, verbose
                )
                if not folder_readme_success:
                    print(f"❌ Failed to generate README for {folder_path}")
                    continue
            except Exception as e:
                print(f"❌ Error generating README for {folder_path}: {e}")
                continue
            
            # Generate INDEX.md (only for inline strategy)
            if index_path:
                try:
                    index_success = generate_folder_index(
                        folder_path, folder_files, file_docs, index_path, model, verbose
                    )
                    if not index_success:
                        print(f"❌ Failed to generate INDEX for {folder_path}")
                        continue
                except Exception as e:
                    print(f"❌ Error generating INDEX for {folder_path}: {e}")
                    continue
            
            # Generate individual file docs (only for detailed mode)
            if mode == "detailed":
                file_success_count = 0
                for filename, doc_path in file_docs.items():
                    file_path = next((f for f in folder_files if os.path.basename(f) == filename), None)
                    if not file_path:
                        continue
                    
                    try:
                        file_success = generate_file_documentation(
                            file_path, doc_path, folder_path, model, verbose
                        )
                        if file_success:
                            file_success_count += 1
                        else:
                            print(f"❌ Failed to generate docs for {filename}")
                    except Exception as e:
                        print(f"❌ Error generating docs for {filename}: {e}")
                
                if verbose:
                    print(f"📄 Generated {file_success_count}/{len(file_docs)} file docs")
            
            success_count += 1
            if verbose:
                print(f"✅ Completed folder: {folder_path}")
        
        # Move Aider history files to .tmp for pipeline artifacts (following changelog/doc-ui pattern)
        aider_files = [".aider.chat.history.md", ".aider.input.history"]
        for aider_file in aider_files:
            if os.path.exists(aider_file):
                dest_file = f".tmp/{aider_file}"
                shutil.move(aider_file, dest_file)
                if verbose:
                    print(f"📦 Moved Aider history to artifacts: {aider_file} → {dest_file}")
        
        # Final results
        if success_count == total_folders:
            print(f"✅ Documentation generation completed successfully!")
            print(f"📁 Generated docs for {success_count}/{total_folders} folders")
            print(f"📂 Output directory: {docs_dir}")
            return True
        elif success_count > 0:
            print(f"⚠️ Partial success: {success_count}/{total_folders} folders processed")
            print(f"📂 Output directory: {docs_dir}")
            return True
        else:
            print("❌ No documentation was generated")
            return False
        
    except Exception as e:
        print(f"❌ Error in doc-gen: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def add_doc_gen_arguments(parser):
    """
    Add doc-gen specific arguments to argument parser.
    Following doc-ui pattern for consistency.
    
    Args:
        parser: ArgumentParser instance
    """
    # Required argument
    parser.add_argument(
        '--mode',
        choices=DOC_GEN_CLI_CHOICES["modes"],
        required=True,
        help='Documentation mode: simple (README per folder) or detailed (README + individual docs)'
    )
    
    # Git mode arguments
    parser.add_argument(
        '--local',
        action='store_const',
        dest='git_mode',
        const='local',
        help='Force local mode (staged/modified files only)'
    )
    
    parser.add_argument(
        '--pipeline',
        action='store_const', 
        dest='git_mode',
        const='pipeline',
        help='Force pipeline mode (changed files since origin/main or --since commit)'
    )
    
    parser.add_argument(
        '--since',
        type=str,
        help='For pipeline mode: compare files changed since this commit (implies --pipeline)'
    )
    
    # Path arguments
    parser.add_argument(
        '--path',
        type=str,
        help='Process specific directory/file path instead of git changes'
    )
    
    parser.add_argument(
        '--shallow',
        action='store_true',
        help='Process only immediate directory, not recursive (only with --path)'
    )
    
    # Output control arguments
    parser.add_argument(
        '--docs-dir',
        type=str,
        default=DOC_GEN_DEFAULTS["docs_dir"],
        help='Output directory: "docs/" (separated) or "./docs/" (inline) (default: docs/)'
    )
    
    parser.add_argument(
        '--strip-prefix',
        type=str,
        help='Comma-separated prefixes to remove from paths (default: src/)'
    )
    
    # File filtering arguments
    parser.add_argument(
        '--preset',
        choices=DOC_GEN_CLI_CHOICES["presets"],
        help='File preset: python (.py,.yaml,.toml + generic) or javascript (.js,.ts,.json + generic)'
    )
    
    parser.add_argument(
        '--ext',
        type=str,
        help='Comma-separated custom extensions to include (overrides preset), e.g. .py,.js,.md'
    )
    
    parser.add_argument(
        '--exclude',
        type=str,
        help='Comma-separated patterns to exclude (overrides preset), e.g. *.pyc,node_modules'
    )
    
    # AI model argument
    parser.add_argument(
        '--model',
        type=str,
        help='AI model to use (default: claude-4-sonnet)'
    )
    
    # Debug argument
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview mode - analyze files but don\'t generate documentation (no AI costs)'
    )


def doc_gen_command(args):
    """
    CLI command handler for Doc-Gen documentation generation.
    Following doc-ui pattern for consistency.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Handle --since implying --pipeline
    git_mode = args.git_mode
    if args.since and not git_mode:
        git_mode = 'pipeline'
    
    return run_doc_gen(
        mode=args.mode,
        git_mode=git_mode,
        path=args.path,
        shallow=args.shallow,
        docs_dir=args.docs_dir,
        strip_prefix=args.strip_prefix,
        preset=args.preset,
        ext=args.ext,
        exclude=args.exclude,
        since_commit=args.since,
        model_name=args.model,
        verbose=args.verbose,
        dry_run=args.dry_run
    )


def get_doc_gen_help() -> str:
    """Get help text for doc-gen command."""
    return """
Generate AI-powered documentation for any project or programming language.

Examples:
  codex-ai doc-gen --mode simple                    # README.md per folder (auto-detect Git mode)
  codex-ai doc-gen --mode detailed                  # README.md + individual file docs
  codex-ai doc-gen --mode simple --local            # Local mode: staged/modified files
  codex-ai doc-gen --mode detailed --pipeline       # Pipeline mode: changed since origin/main
  codex-ai doc-gen --path src/ --mode detailed      # Process specific path (recursive)
  codex-ai doc-gen --path src/utils/ --shallow --mode simple  # Path + non-recursive
  codex-ai doc-gen --mode detailed --docs-dir docs/ # Separated strategy (docs/src/utils/)
  codex-ai doc-gen --mode detailed --docs-dir ./docs/  # Inline strategy (src/utils/docs/)
  codex-ai doc-gen --mode detailed --preset python  # Only Python files
  codex-ai doc-gen --mode detailed --preset javascript  # Only JS/TS files
  codex-ai doc-gen --mode detailed --ext .py,.js,.md  # Custom extensions
  codex-ai doc-gen --mode detailed --exclude *.pyc,node_modules  # Custom exclusions
  codex-ai doc-gen --mode detailed --since HEAD~5   # Pipeline: files changed in last 5 commits
  codex-ai doc-gen --mode detailed --strip-prefix src/,lib/  # Remove path prefixes
  codex-ai doc-gen --dry-run --verbose              # Preview without AI costs

Mode Detection:
  • Auto-detect: Uses 'local' if staged/modified files exist, 'pipeline' otherwise
  • Local mode: Processes staged and modified files (git status)
  • Pipeline mode: Processes files changed since specified commit or origin/main
  • Path mode: Process specific directory/file path (overrides Git mode detection)

Documentation Modes:
  • Simple: Generates README.md per folder explaining contents and structure
  • Detailed: Generates README.md per folder + individual [filename].md for each file

Output Strategies:
  • Separated (--docs-dir docs/): Creates docs/src/utils/ mirroring project structure
  • Inline (--docs-dir ./docs/): Creates src/utils/docs/ within each folder
    - Simple mode: Only README.md in each folder
    - Detailed mode: README.md + docs/INDEX.md + docs/[filename].md

File Presets:
  • Default (no --preset): python + javascript + generic extensions (comprehensive)
  • --preset python: .py, .pyi, .yaml, .toml + generic files
  • --preset javascript: .js, .ts, .jsx, .tsx, .json, .mjs + generic files
  • Custom: --ext .ext1,.ext2 for specific extensions

File Filtering:
  • Extensions: Includes files matching preset or custom extensions
  • Exclusions: Skips build dirs, node_modules, __pycache__, .git, etc.
  • Path filters: --strip-prefix removes common prefixes from output paths
  • Shallow: --shallow processes only immediate directory (no recursion)

The doc-gen command provides flexible, AI-powered documentation generation
for any codebase, with intelligent file detection and customizable output
strategies suitable for both technical documentation and project overviews.
"""
