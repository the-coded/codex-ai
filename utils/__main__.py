"""
Command-line interface for utility modules.

Usage:
    python -m utils.<module_name>
    
Available modules:
    - get_base_path: Path resolution for dev/prod modes
    - load_json: JSON file loading and parsing
    - load_template: Template processing
"""

import sys
from importlib import import_module

AVAILABLE_MODULES = {
    'get_base_path': 'Path resolution for dev/prod modes',
    'load_json': 'JSON file loading and parsing',
    'load_template': 'Template processing'
}

def print_usage():
    """Print usage information."""
    print("\n🔍 Usage:")
    print("  python -m utils.<module_name>")
    print("\n📦 Available modules:")
    for module, description in AVAILABLE_MODULES.items():
        print(f"  - {module}: {description}")
    print()

def main():
    """
    Main entry point for utility modules.
    Dynamically loads and executes the requested module.
    """
    if len(sys.argv) != 2:
        print("❌ Error: Module name required")
        print_usage()
        sys.exit(1)

    module_name = sys.argv[1].replace('utils.', '')
    
    if module_name not in AVAILABLE_MODULES:
        print(f"❌ Error: Unknown module '{module_name}'")
        print_usage()
        sys.exit(1)
    
    try:
        # Import and run the module
        module = import_module(f'.{module_name}', package='utils')
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"❌ Error: Module '{module_name}' has no main() function")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error executing module '{module_name}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
