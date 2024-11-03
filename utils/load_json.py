"""
JSON loading utility with error handling.

This module provides functionality to safely load and parse JSON files,
with comprehensive error handling and validation.

Example usage:
    from utils.load_json import load_json

    # Load and parse a JSON file
    data = load_json('config.json')
"""

import json
import sys
from typing import Any, Dict

def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path (str): Path to the JSON file to load
    
    Returns:
        Dict[str, Any]: Parsed JSON data as a dictionary
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        raise
    except IOError as e:
        print(f"❌ Error reading {file_path}: {e}")
        raise

def main():
    """
    Main function to demonstrate JSON loading.
    Called when running as a module: python -m utils.load_json
    """
    if len(sys.argv) != 2:
        print("❌ Error: JSON file path required")
        print("💡 Usage: python -m utils.load_json <json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        data = load_json(file_path)
        print("✅ Successfully loaded JSON file")
        print("\n📄 File contents:")
        print(json.dumps(data, indent=2))
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
