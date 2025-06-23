"""
Example usage of the get_base_path utility.

This script demonstrates how to use the get_base_path function to handle
paths correctly based on the current environment.
"""

from utils.get_base_path import get_base_path

def demonstrate_path_resolution():
    """
    Demonstrates path resolution based on environment.
    """
    # Get base path for current environment
    base = get_base_path()
    print("Current Environment:")
    print("-" * 50)
    print(f"Base path: {base}")
    print(f"Config file: {base}/config/settings.json")
    print(f"Template file: {base}/templates/email.txt")
    print(f"Assets directory: {base}/assets/images")
    print()
    print("Note: The base path will be:")
    print("  - '.' if running from project root")
    print("  - '.codex' if running from another project")

def demonstrate_practical_usage():
    """
    Demonstrates practical usage in a project context.
    """
    # Example: Loading configuration
    def load_config():
        base = get_base_path()
        config_path = f"{base}/config/settings.json"
        print(f"Would load config from: {config_path}")
        return config_path

    # Example: Resolving template paths
    def get_template_path(template_name):
        base = get_base_path()
        template_path = f"{base}/templates/{template_name}"
        print(f"Would load template from: {template_path}")
        return template_path

    print("\nPractical Usage Examples:")
    print("-" * 50)
    
    # Environment is automatically detected
    print("Loading files:")
    load_config()
    get_template_path("welcome.txt")

if __name__ == "__main__":
    demonstrate_path_resolution()
    demonstrate_practical_usage()
