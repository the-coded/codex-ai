"""
Example usage of the get_base_path utility.

This script demonstrates how to use the get_base_path function to handle
paths correctly in both development and production environments.
"""

from utils.get_base_path import get_base_path

def demonstrate_path_resolution():
    """
    Demonstrates path resolution in different modes.
    """
    # Development mode examples
    dev_base = get_base_path("dev")
    print("Development Mode:")
    print("-" * 50)
    print(f"Base path: {dev_base}")
    print(f"Config file: {dev_base}/config/settings.json")
    print(f"Template file: {dev_base}/templates/email.txt")
    print(f"Assets directory: {dev_base}/assets/images")
    print()

    # Production mode examples
    prod_base = get_base_path("prod")  # or just get_base_path() as prod is default
    print("Production Mode:")
    print("-" * 50)
    print(f"Base path: {prod_base}")
    print(f"Config file: {prod_base}/config/settings.json")
    print(f"Template file: {prod_base}/templates/email.txt")
    print(f"Assets directory: {prod_base}/assets/images")
    print()

def demonstrate_practical_usage():
    """
    Demonstrates practical usage in a project context.
    """
    # Example: Loading configuration based on mode
    def load_config(mode):
        base = get_base_path(mode)
        config_path = f"{base}/config/settings.json"
        print(f"Would load config from: {config_path}")
        return config_path

    # Example: Resolving template paths based on mode
    def get_template_path(template_name, mode):
        base = get_base_path(mode)
        template_path = f"{base}/templates/{template_name}"
        print(f"Would load template from: {template_path}")
        return template_path

    print("Practical Usage Examples:")
    print("-" * 50)
    
    # Development environment
    print("In Development:")
    load_config("dev")
    get_template_path("welcome.txt", "dev")
    print()

    # Production environment
    print("In Production:")
    load_config("prod")
    get_template_path("welcome.txt", "prod")

if __name__ == "__main__":
    demonstrate_path_resolution()
    print()
    demonstrate_practical_usage()
