"""
Example usage of the load_json utility.

This script demonstrates how to use the load_json function to load
and work with JSON files in different scenarios.
"""

from utils.load_json import load_json

def demonstrate_basic_usage():
    """
    Demonstrates basic JSON loading.
    """
    print("Basic JSON Loading:")
    print("-" * 50)
    
    # Load a project structure JSON
    try:
        data = load_json('.tmp/tree_project.json')
        print("Successfully loaded project structure:")
        if 'react' in data:
            print("- Found React structure")
        if 'sass' in data:
            print("- Found Sass structure")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    print()

def demonstrate_error_handling():
    """
    Demonstrates error handling scenarios.
    """
    print("Error Handling Examples:")
    print("-" * 50)
    
    # Try to load non-existent file
    try:
        data = load_json('non_existent.json')
    except FileNotFoundError as e:
        print(f"File not found error handled: {e}")
    
    # Try to load invalid JSON
    try:
        data = load_json('invalid.json')
    except Exception as e:
        print(f"JSON error handled: {e}")
    print()

def demonstrate_practical_usage():
    """
    Demonstrates practical usage scenarios.
    """
    print("Practical Usage Examples:")
    print("-" * 50)
    
    try:
        # Load project structure
        structure = load_json('.tmp/tree_project.json')
        
        # Example: Check for specific components
        if 'react' in structure and 'src' in structure['react']:
            react_src = structure['react']['src']
            if 'components' in react_src:
                print("Found React components:")
                for component_type in react_src['components']:
                    print(f"- {component_type}")
        
        # Example: Check for Sass files
        if 'sass' in structure and 'src' in structure['sass']:
            sass_src = structure['sass']['src']
            if 'components' in sass_src:
                print("\nFound Sass components:")
                for component_type in sass_src['components']:
                    print(f"- {component_type}")
    
    except Exception as e:
        print(f"Error processing JSON: {e}")

if __name__ == "__main__":
    demonstrate_basic_usage()
    demonstrate_error_handling()
    demonstrate_practical_usage()
