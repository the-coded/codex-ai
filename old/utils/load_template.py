"""
Template processing utility with variable substitution.

This module provides functionality to load template files and substitute
variables using Python's string formatting.

Example usage:
    from utils.load_template import load_template

    # Load and process a template
    result = load_template('template.txt',
        name="John",
        title="Developer"
    )
"""

import sys
from typing import Any, Dict

def load_template(template_path: str, **kwargs: Any) -> str:
    """
    Load and process a template file with variable substitution.
    
    Args:
        template_path (str): Path to the template file
        **kwargs: Key-value pairs for variable substitution
    
    Returns:
        str: Processed template with variables substituted
    
    Raises:
        FileNotFoundError: If the template file doesn't exist
        KeyError: If a required template variable is missing
        IOError: If there's an error reading the file
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        return template.format(**kwargs)
    except FileNotFoundError:
        print(f"❌ Error: Template file not found: {template_path}")
        raise
    except KeyError as e:
        print(f"❌ Error: Missing template variable: {e}")
        raise
    except IOError as e:
        print(f"❌ Error reading template {template_path}: {e}")
        raise
    except Exception as e:
        print(f"❌ Error processing template: {e}")
        raise

def main():
    """
    Main function to demonstrate template processing.
    Called when running as a module: python -m utils.load_template
    """
    if len(sys.argv) < 2:
        print("❌ Error: Template file path required")
        print("💡 Usage: python -m utils.load_template <template_file> [var1=value1 var2=value2 ...]")
        print("📝 Example: python -m utils.load_template template.txt name=John title=Developer")
        sys.exit(1)

    template_path = sys.argv[1]
    variables = {}
    
    # Parse variable assignments from command line
    for arg in sys.argv[2:]:
        try:
            key, value = arg.split('=', 1)
            variables[key] = value
        except ValueError:
            print(f"❌ Error: Invalid variable assignment: {arg}")
            print("💡 Format should be: key=value")
            sys.exit(1)

    try:
        result = load_template(template_path, **variables)
        print("✅ Successfully processed template")
        print("\n📄 Result:")
        print(result)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
