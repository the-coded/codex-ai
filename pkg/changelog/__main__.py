"""
Command-line interface for changelog generation.

For command-line usage:
    # Generate regular git logs (default)
    python -m pkg.changelog

    # Generate release logs
    python -m pkg.changelog --type release
"""

import argparse
from .run import run

def main():
    parser = argparse.ArgumentParser(description="Generate changelog documentation")
    parser.add_argument("--type", choices=["log", "release"], default="log",
                      help="Type of logs to generate: log (regular git logs) or release (release logs)")
    args = parser.parse_args()
    run(args.type)

if __name__ == "__main__":
    main()
