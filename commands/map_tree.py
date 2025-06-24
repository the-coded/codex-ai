"""
Map-tree command implementation for Codex-AI.

Provides CLI interface for project structure mapping and analysis.
Ports the functionality from old/bin/tree_*.sh scripts to Python.
"""

import sys
import json
from pathlib import Path
from typing import Optional, Dict, List, Any

from core.git import (
    GitTreeGenerator, ChangesTracker, GitLogAnalyzer, GitReleaseAnalyzer
)
from core import GIT_AVAILABLE
from config import CodexConfig


def run_map_tree(args, config: CodexConfig) -> int:
    """
    Run map-tree analysis command.
    
    Args:
        args: Parsed command line arguments
        config: Codex configuration object
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not GIT_AVAILABLE:
        print("❌ Error: Git module not available")
        print("   Please check your installation")
        return 1
    
    try:
        print("🗺️  Mapping project structure...")
        
        # Ensure .tmp directory exists
        tmp_dir = Path(".tmp")
        tmp_dir.mkdir(exist_ok=True)
        
        # Determine what to generate
        if args.project:
            return _generate_project_map(args, config)
        elif args.git:
            return _generate_git_maps(args, config)
        elif args.releases:
            return _generate_release_maps(args, config)
        elif args.siblings:
            return _generate_siblings_map(args, config)
        else:
            # Default to all maps if no specific option (equivalent to tree_generate_all.sh)
            return _generate_all_maps(args, config)
        
    except Exception as e:
        print(f"❌ Error running map-tree analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def _generate_all_maps(args, config: CodexConfig) -> int:
    """Generate all tree maps (equivalent to tree_generate_all.sh)."""
    print("📊 Generating all tree structures...")
    
    try:
        # Generate project structure
        result = _generate_project_map(args, config, silent=True)
        if result != 0:
            return result
        
        # Generate git changes
        result = _generate_git_maps(args, config, silent=True)
        if result != 0:
            return result
        
        # Generate release changes
        result = _generate_release_maps(args, config, silent=True)
        if result != 0:
            return result
        
        # Generate siblings
        result = _generate_siblings_map(args, config, silent=True)
        if result != 0:
            return result
        
        print("✅ All tree structures generated successfully in .tmp/:")
        print("   📁 tree_project.json (complete project structure)")
        print("   🔄 tree_git_changed.json (files changed in last commit)")
        print("   🗑️  tree_git_removed.json (files removed in last commit)")
        print("   📋 tree_git_all.json (all git changes)")
        print("   🏷️  tree_release_changed.json (files changed between releases)")
        print("   🗑️  tree_release_removed.json (files removed between releases)")
        print("   📋 tree_release_all.json (all release changes)")
        print("   👥 tree_git_siblings.json (sibling files of changed files)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating all maps: {e}")
        return 1


def _generate_project_map(args, config: CodexConfig, silent: bool = False) -> int:
    """Generate project structure map (equivalent to tree_project.sh)."""
    if not silent:
        print("🏗️  Generating project structure...")
    
    try:
        generator = GitTreeGenerator()
        
        # Get project root (current directory)
        project_root = Path.cwd()
        
        # Generate structure
        result = generator.generate_project_tree(str(project_root))
        
        if not result.success:
            raise Exception(result.error_message or "Failed to generate project tree")
        
        # Load the generated JSON file to get the structure
        with open(result.output_file, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        
        # Save to custom output if specified (validate first)
        if args.output:
            if not _save_to_custom_output(structure, args, "project_structure"):
                return 1
        
        if not silent:
            print(f"✅ Project structure saved to {result.output_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating project map: {e}")
        return 1


def _generate_git_maps(args, config: CodexConfig, silent: bool = False) -> int:
    """Generate git changes maps (equivalent to tree_git_changes.sh)."""
    if not silent:
        print("🔄 Generating git changes analysis...")
    
    try:
        tracker = ChangesTracker()
        
        # Get git changes from last commit
        changes = tracker.get_changes_since_commit("HEAD~1")
        
        # Separate changed and removed files
        changed_files = [f for f in changes if not f.is_deleted]
        removed_files = [f for f in changes if f.is_deleted]
        
        # Generate structures
        changed_structure = _create_file_structure([f.path for f in changed_files])
        removed_structure = _create_file_structure([f.path for f in removed_files])
        all_structure = _create_file_structure([f.path for f in changes])
        
        # Save files
        files_to_save = [
            (".tmp/tree_git_changed.json", changed_structure),
            (".tmp/tree_git_removed.json", removed_structure),
            (".tmp/tree_git_all.json", all_structure)
        ]
        
        for filepath, structure in files_to_save:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)
        
        if not silent:
            print("✅ Git changes saved to:")
            print("   📝 .tmp/tree_git_changed.json")
            print("   🗑️  .tmp/tree_git_removed.json")
            print("   📋 .tmp/tree_git_all.json")
        
        # Save to custom output if specified
        if args.output:
            output_data = {
                "changed": changed_structure,
                "removed": removed_structure,
                "all": all_structure
            }
            if not _save_to_custom_output(output_data, args, "git_changes"):
                return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating git maps: {e}")
        return 1


def _generate_release_maps(args, config: CodexConfig, silent: bool = False) -> int:
    """Generate release changes maps (equivalent to tree_git_release_changes.sh)."""
    if not silent:
        print("🏷️  Generating release changes analysis...")
    
    try:
        analyzer = GitReleaseAnalyzer()
        
        # Get release changes
        try:
            comparison = analyzer.analyze_current_release('simple')
            if not comparison:
                # No releases found, create empty structures
                if not silent:
                    print("⚠️  No releases found, generating empty release structures")
                changed_structure = {}
                removed_structure = {}
                all_structure = {}
            else:
                # Extract file changes from the comparison
                # We need to get the actual file changes between releases
                current_tag = comparison.current_release.tag
                if comparison.previous_release:
                    previous_ref = comparison.previous_release.tag
                else:
                    # First release - compare with first commit
                    previous_ref = analyzer.get_first_commit()
                
                # Get file changes using git diff
                changes = _get_release_file_changes(analyzer, previous_ref, current_tag)
                
                # Separate changed and removed files
                changed_files = [f for f in changes if f.get('status') != 'D']
                removed_files = [f for f in changes if f.get('status') == 'D']
                
                # Generate structures
                changed_structure = _create_file_structure([f['path'] for f in changed_files])
                removed_structure = _create_file_structure([f['path'] for f in removed_files])
                all_structure = _create_file_structure([f['path'] for f in changes])
        except Exception:
            # No releases found, create empty structures
            if not silent:
                print("⚠️  No releases found, generating empty release structures")
            changed_structure = {}
            removed_structure = {}
            all_structure = {}
        
        # Save files
        files_to_save = [
            (".tmp/tree_release_changed.json", changed_structure),
            (".tmp/tree_release_removed.json", removed_structure),
            (".tmp/tree_release_all.json", all_structure)
        ]
        
        for filepath, structure in files_to_save:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)
        
        if not silent:
            print("✅ Release changes saved to:")
            print("   📝 .tmp/tree_release_changed.json")
            print("   🗑️  .tmp/tree_release_removed.json")
            print("   📋 .tmp/tree_release_all.json")
        
        # Save to custom output if specified
        if args.output:
            output_data = {
                "changed": changed_structure,
                "removed": removed_structure,
                "all": all_structure
            }
            if not _save_to_custom_output(output_data, args, "release_changes"):
                return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating release maps: {e}")
        return 1


def _generate_siblings_map(args, config: CodexConfig, silent: bool = False) -> int:
    """Generate siblings map (equivalent to tree_git_siblings.sh)."""
    if not silent:
        print("👥 Generating sibling files analysis...")
    
    try:
        tracker = ChangesTracker()
        
        # Get changed files from last commit
        changes = tracker.get_changes_since_commit("HEAD~1")
        changed_files = [f.path for f in changes if not f.is_deleted]
        
        # Find sibling files
        siblings = _find_sibling_files(changed_files)
        
        # Generate structure
        structure = _create_file_structure(siblings)
        
        # Save file
        output_file = Path(".tmp/tree_git_siblings.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        if not silent:
            print(f"✅ Sibling files saved to {output_file}")
        
        # Save to custom output if specified
        if args.output:
            if not _save_to_custom_output(structure, args, "sibling_files"):
                return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating siblings map: {e}")
        return 1


def _create_file_structure(file_paths: List[str]) -> Dict[str, Any]:
    """
    Create nested directory structure from list of file paths.
    
    Args:
        file_paths: List of file paths
        
    Returns:
        Nested dictionary representing directory structure
    """
    structure = {}
    
    for file_path in sorted(file_paths):
        if not file_path:
            continue
            
        parts = Path(file_path).parts
        current = structure
        
        # Navigate/create directory structure
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Add file to current directory
        if len(parts) > 0:
            filename = parts[-1]
            if "files" not in current:
                current["files"] = []
            if filename not in current["files"]:
                current["files"].append(filename)
    
    # Sort files in each directory
    def sort_files(obj):
        if isinstance(obj, dict):
            if "files" in obj:
                obj["files"] = sorted(obj["files"])
            for key, value in obj.items():
                if key != "files":
                    sort_files(value)
    
    sort_files(structure)
    return structure


def _find_sibling_files(changed_files: List[str]) -> List[str]:
    """
    Find sibling files of changed files.
    
    Args:
        changed_files: List of changed file paths
        
    Returns:
        List of sibling file paths
    """
    siblings = set()
    
    for file_path in changed_files:
        file_path_obj = Path(file_path)
        parent_dir = file_path_obj.parent
        
        # Add all files in the same directory
        if parent_dir.exists():
            for sibling in parent_dir.iterdir():
                if sibling.is_file() and sibling.name != file_path_obj.name:
                    siblings.add(str(sibling))
    
    return sorted(list(siblings))


def _get_release_file_changes(analyzer: GitReleaseAnalyzer, previous_ref: str, current_ref: str) -> List[Dict[str, str]]:
    """
    Get file changes between two release references.
    
    Args:
        analyzer: GitReleaseAnalyzer instance
        previous_ref: Previous release reference
        current_ref: Current release reference
        
    Returns:
        List of file changes with status and path
    """
    try:
        # Use git diff to get file changes
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--name-status", f"{previous_ref}..{current_ref}"],
            cwd=analyzer.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        changes = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0]
                path = parts[1]
                
                # Handle renamed files
                if len(parts) > 2 and status.startswith('R'):
                    path = parts[2]  # Use new path for renamed files
                
                changes.append({
                    'status': status[0],  # First character (A, M, D, R, etc.)
                    'path': path
                })
        
        return changes
        
    except subprocess.CalledProcessError:
        return []


def _save_to_custom_output(data: Any, args, data_type: str) -> bool:
    """
    Save data to custom output file.
    
    Returns:
        True if successful, False if error occurred
    """
    output_path = Path(args.output)
    
    try:
        # Only create parent directories if they're in a writable location
        parent_dir = output_path.parent
        if parent_dir != Path("/") and not str(parent_dir).startswith("/System") and not str(parent_dir).startswith("/usr"):
            parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine format from file extension if not specified
        format_type = args.format
        if not format_type:
            suffix = output_path.suffix.lower()
            if suffix == '.json':
                format_type = 'json'
            elif suffix == '.yaml' or suffix == '.yml':
                format_type = 'yaml'
            elif suffix == '.md':
                format_type = 'markdown'
            else:
                format_type = 'json'  # Default
        
        # Generate content based on format
        if format_type == 'json':
            content = json.dumps(data, indent=2, ensure_ascii=False)
        elif format_type == 'yaml':
            import yaml
            content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        elif format_type == 'markdown':
            content = _generate_markdown_report(data, data_type)
        else:
            content = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Custom output saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving to {output_path}: {e}")
        return False


def _generate_markdown_report(data: Any, data_type: str) -> str:
    """Generate markdown report from data."""
    lines = [f"# {data_type.replace('_', ' ').title()} Report\n"]
    
    def add_structure(obj, level=0):
        indent = "  " * level
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "files":
                    if value:
                        lines.append(f"{indent}📁 **Files:**")
                        for file in value:
                            lines.append(f"{indent}  - {file}")
                else:
                    lines.append(f"{indent}📂 **{key}/**")
                    add_structure(value, level + 1)
        lines.append("")
    
    add_structure(data)
    return "\n".join(lines)


def add_map_tree_arguments(parser):
    """
    Add map-tree specific arguments to argument parser.
    
    Args:
        parser: ArgumentParser instance
    """
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all tree structures (equivalent to tree_generate_all.sh)'
    )
    
    parser.add_argument(
        '--project',
        action='store_true',
        help='Generate project structure tree (equivalent to tree_project.sh)'
    )
    
    parser.add_argument(
        '--git',
        action='store_true',
        help='Generate git changes trees (equivalent to tree_git_changes.sh)'
    )
    
    parser.add_argument(
        '--releases',
        action='store_true',
        help='Generate release changes trees (equivalent to tree_git_release_changes.sh)'
    )
    
    parser.add_argument(
        '--siblings',
        action='store_true',
        help='Generate sibling files tree (equivalent to tree_git_siblings.sh)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'markdown'],
        default='json',
        help='Output format for custom files (default: json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Save output to custom file (format auto-detected from extension)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output for debugging'
    )


# CLI integration helper
def get_map_tree_help() -> str:
    """Get help text for map-tree command."""
    return """
Map project structure and changes for AI analysis.

Examples:
  codex-ai map-tree --all                      # Generate all tree structures
  codex-ai map-tree --project                  # Project structure only
  codex-ai map-tree --git                      # Git changes only
  codex-ai map-tree --releases                 # Release changes only
  codex-ai map-tree --siblings                 # Sibling files only
  codex-ai map-tree --project -o structure.json  # Save to custom file
  codex-ai map-tree --all --format yaml        # YAML format

The map-tree command generates JSON structures that map your project
for AI analysis. It's equivalent to the old tree_*.sh scripts but
provides a unified CLI interface with multiple output formats.

Generated files in .tmp/:
  - tree_project.json (complete project structure)
  - tree_git_changed.json (files changed in last commit)
  - tree_git_removed.json (files removed in last commit)
  - tree_git_all.json (all git changes)
  - tree_release_changed.json (files changed between releases)
  - tree_release_removed.json (files removed between releases)
  - tree_release_all.json (all release changes)
  - tree_git_siblings.json (sibling files of changed files)
"""
