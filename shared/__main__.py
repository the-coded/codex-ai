"""
Command-line interface for shared utilities.

Usage:
    python -m shared.<module_name>
    
Available modules:
    - require_aider: Install and verify aider-chat package
"""

import sys
from importlib import import_module

AVAILABLE_MODULES = {
    'require_aider': 'Install and verify aider-chat package'
}

def print_usage():
    """Print usage information."""
    print("\n🔍 Usage:")
    print("  python -m shared.<module_name>")
    print("\n📦 Available modules:")
    for module, description in AVAILABLE_MODULES.items():
        print(f"  - {module}: {description}")
    print()

def main():
    """
    Main entry point for shared utilities.
    Dynamically loads and executes the requested module.
    """
    # If no arguments, assume we're being called as 'python -m shared.require_aider'
    if len(sys.argv) == 1:
        module_name = 'require_aider'
    # If one argument, it's either the module name or 'shared.require_aider'
    elif len(sys.argv) == 2:
        module_name = sys.argv[1].replace('shared.', '')
    else:
        print("❌ Error: Too many arguments")
        print_usage()
        sys.exit(1)
    
    if module_name not in AVAILABLE_MODULES:
        print(f"❌ Error: Unknown module '{module_name}'")
        print_usage()
        sys.exit(1)
    
    try:
        # Import and run the module
        module = import_module(f'.{module_name}', package='shared')
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
