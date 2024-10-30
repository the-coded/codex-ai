"""
requirements.py

This file handles the installation of required packages for the changelog command.
"""

import subprocess
import sys

def setup_environment() -> None:
    """
    Sets up the Python environment with required packages.
    """
    print("Setting up changelog environment...")
    
    try:
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements/aider-chat.txt"], check=True)
        print("Environment setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up environment: {e}")
        raise

if __name__ == "__main__":
    setup_environment()
