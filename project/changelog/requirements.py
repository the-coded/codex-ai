"""
Requirements installation for the changelog generator.
"""

import argparse
import subprocess
import sys
from utils.get_base_path import get_base_path

def setup_environment(mode: str = "prod") -> None:
    """
    Sets up the Python environment with required packages.
    
    Args:
        mode (str): Running mode, either "prod" or "dev" (default: "prod")
            - "prod": Running from .nexus in another repository
            - "dev": Running locally from codex-ai repository
    """
    print("Setting up changelog environment...")
    
    base = get_base_path(mode)
    requirements_path = f"{base}/requirements/aider-chat.txt"
    
    try:
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], check=True)
        print("Environment setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up environment: {e}")
        raise

def main():
    """
    Parse command line arguments and setup the environment.
    """
    parser = argparse.ArgumentParser(description="Setup changelog environment")
    parser.add_argument("--mode", choices=["prod", "dev"], default="prod",
                      help="Running mode: prod (production) or dev (development)")
    args = parser.parse_args()
    
    setup_environment(args.mode)

if __name__ == "__main__":
    main()
