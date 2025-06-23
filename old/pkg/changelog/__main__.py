"""
Command-line interface for changelog generation.

For command-line usage:
    python -m pkg.changelog
"""

import argparse
from .run import run

def main():
    parser = argparse.ArgumentParser(description="Generate changelog documentation")
    args = parser.parse_args()
    run()

if __name__ == "__main__":
    main()
