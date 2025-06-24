"""
JSON loading and manipulation utilities with comprehensive error handling.

This module provides functionality to safely load, parse, save, and manipulate JSON files,
with comprehensive error handling, validation, and integration with the project's
path resolution system.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .get_base_path import resolve_path, get_output_path


def load_json(file_path: Union[str, Path], relative_to_project: bool = True) -> Dict[str, Any]:
    """
    Load and parse a JSON file with comprehensive error handling.
    
    Args:
        file_path: Path to the JSON file to load
        relative_to_project: If True, resolve path relative to project root
    
    Returns:
        Dict[str, Any]: Parsed JSON data as a dictionary
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        IOError: If there's an error reading the file
        
    Examples:
        >>> # Load project config
        >>> config = load_json("config/settings.json")
        
        >>> # Load absolute path
        >>> data = load_json("/tmp/data.json", relative_to_project=False)
    """
    try:
        if relative_to_project:
            resolved_path = resolve_path(str(file_path))
        else:
            resolved_path = Path(file_path)
            
        with open(resolved_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except FileNotFoundError:
        print(f"❌ Error: File not found: {resolved_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {resolved_path}: {e}")
        raise
    except IOError as e:
        print(f"❌ Error reading {resolved_path}: {e}")
        raise


def save_json(data: Dict[str, Any], file_path: Union[str, Path], 
              relative_to_project: bool = True, indent: int = 2,
              ensure_dir: bool = True) -> Path:
    """
    Save data to a JSON file with formatting and error handling.
    
    Args:
        data: Data to save as JSON
        file_path: Path where to save the JSON file
        relative_to_project: If True, resolve path relative to project root
        indent: JSON indentation for pretty printing
        ensure_dir: If True, create directory if it doesn't exist
        
    Returns:
        Path: Actual path where file was saved
        
    Examples:
        >>> # Save to output directory
        >>> save_json({"key": "value"}, "output/data.json")
        
        >>> # Save with custom formatting
        >>> save_json(data, "compact.json", indent=None)
    """
    try:
        if relative_to_project:
            resolved_path = resolve_path(str(file_path))
        else:
            resolved_path = Path(file_path)
            
        if ensure_dir:
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            
        with open(resolved_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            
        return resolved_path
        
    except IOError as e:
        print(f"❌ Error writing to {resolved_path}: {e}")
        raise


def load_json_safe(file_path: Union[str, Path], default: Optional[Dict[str, Any]] = None,
                   relative_to_project: bool = True) -> Dict[str, Any]:
    """
    Load JSON file with safe fallback to default value.
    
    Args:
        file_path: Path to the JSON file to load
        default: Default value if file doesn't exist or is invalid
        relative_to_project: If True, resolve path relative to project root
        
    Returns:
        Dict[str, Any]: Parsed JSON data or default value
        
    Examples:
        >>> # Load with fallback
        >>> config = load_json_safe("config.json", {"default": "config"})
        
        >>> # Load optional file
        >>> cache = load_json_safe(".cache/data.json", {})
    """
    if default is None:
        default = {}
        
    try:
        return load_json(file_path, relative_to_project)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return default


def merge_json_files(*file_paths: Union[str, Path], 
                     relative_to_project: bool = True) -> Dict[str, Any]:
    """
    Load and merge multiple JSON files into a single dictionary.
    
    Later files override values from earlier files.
    
    Args:
        *file_paths: Paths to JSON files to merge
        relative_to_project: If True, resolve paths relative to project root
        
    Returns:
        Dict[str, Any]: Merged JSON data
        
    Examples:
        >>> # Merge config files
        >>> config = merge_json_files(
        ...     "config/base.json",
        ...     "config/local.json"
        ... )
    """
    merged = {}
    
    for file_path in file_paths:
        try:
            data = load_json(file_path, relative_to_project)
            merged.update(data)
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Warning: Could not load {file_path}: {e}")
            continue
            
    return merged


def validate_json_schema(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate that JSON data contains required keys.
    
    Args:
        data: JSON data to validate
        required_keys: List of required keys
        
    Returns:
        bool: True if all required keys are present
        
    Examples:
        >>> data = {"name": "test", "version": "1.0"}
        >>> validate_json_schema(data, ["name", "version"])
        True
    """
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        print(f"❌ Missing required keys: {missing_keys}")
        return False
        
    return True


def pretty_print_json(data: Dict[str, Any], indent: int = 2) -> str:
    """
    Format JSON data as a pretty-printed string.
    
    Args:
        data: JSON data to format
        indent: Indentation level
        
    Returns:
        str: Pretty-printed JSON string
        
    Examples:
        >>> data = {"key": "value"}
        >>> print(pretty_print_json(data))
        {
          "key": "value"
        }
    """
    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)


def minify_json(data: Dict[str, Any]) -> str:
    """
    Format JSON data as a minified string.
    
    Args:
        data: JSON data to minify
        
    Returns:
        str: Minified JSON string
        
    Examples:
        >>> data = {"key": "value"}
        >>> minify_json(data)
        '{"key":"value"}'
    """
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)


def json_to_output(data: Dict[str, Any], filename: str, 
                   output_dir: str = ".tmp", pretty: bool = True) -> Path:
    """
    Save JSON data to standardized output location.
    
    Args:
        data: JSON data to save
        filename: Output filename
        output_dir: Output directory (default: .tmp)
        pretty: If True, use pretty formatting
        
    Returns:
        Path: Path to saved file
        
    Examples:
        >>> # Save analysis results
        >>> path = json_to_output(analysis_data, "analysis.json")
        
        >>> # Save minified data
        >>> path = json_to_output(data, "compact.json", pretty=False)
    """
    output_path = get_output_path(filename, output_dir)
    
    indent = 2 if pretty else None
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        
    return output_path


def load_project_structure() -> Dict[str, Any]:
    """
    Load project structure JSON file (commonly used in the system).
    
    Returns:
        Dict[str, Any]: Project structure data
        
    Examples:
        >>> structure = load_project_structure()
        >>> files = structure.get("files", [])
    """
    return load_json_safe(".tmp/tree_project.json", {})


def load_git_changes() -> Dict[str, Any]:
    """
    Load Git changes JSON file (commonly used in the system).
    
    Returns:
        Dict[str, Any]: Git changes data
        
    Examples:
        >>> changes = load_git_changes()
        >>> changed_files = changes.get("changed", [])
    """
    return load_json_safe(".tmp/tree_git_changed.json", {})


# CLI functionality
def main():
    """
    Main function for CLI usage.
    Called when running as a module: python -m utils.load_json
    """
    if len(sys.argv) < 2:
        print("❌ Error: JSON file path required")
        print("💡 Usage: python -m utils.load_json <json_file> [output_file]")
        print("📋 Examples:")
        print("  python -m utils.load_json config.json")
        print("  python -m utils.load_json input.json output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Load JSON file
        data = load_json(input_file)
        print(f"✅ Successfully loaded JSON file: {input_file}")
        
        if output_file:
            # Save to output file (pretty formatted)
            save_json(data, output_file)
            print(f"✅ Saved formatted JSON to: {output_file}")
        else:
            # Print to console
            print("\n📄 File contents:")
            print(pretty_print_json(data))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


# Export main functions
__all__ = [
    "load_json",
    "save_json", 
    "load_json_safe",
    "merge_json_files",
    "validate_json_schema",
    "pretty_print_json",
    "minify_json",
    "json_to_output",
    "load_project_structure",
    "load_git_changes"
]


if __name__ == "__main__":
    main()
