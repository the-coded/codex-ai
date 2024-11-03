"""
Aider-chat requirement checker and installer.

This script checks if aider-chat is installed in the current virtual environment
and installs version 0.60.0 if it's not present.
"""

import subprocess
import sys
import importlib.util

def is_package_installed(package_name: str) -> bool:
    """
    Check if a package is installed in the current environment.

    Args:
        package_name (str): Name of the package to check

    Returns:
        bool: True if package is installed, False otherwise
    """
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def install_aider():
    """
    Install aider-chat version 0.60.0 using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aider-chat==0.60.0"])
        print("✅ Successfully installed aider-chat 0.60.0")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing aider-chat: {e}")
        sys.exit(1)

def main():
    """
    Main function to check and install aider-chat if needed.
    """
    if is_package_installed("aider-chat"):
        print("✅ aider-chat is already installed")
    else:
        print("📦 Installing aider-chat 0.60.0...")
        install_aider()

if __name__ == "__main__":
    main()
