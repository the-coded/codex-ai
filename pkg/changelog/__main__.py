"""
Command-line interface for changelog generation.

For command-line usage:
    # Development mode with log type (default)
    python -m pkg.changelog --mode dev --type log

    # Development mode with release type
    python -m pkg.changelog --mode dev --type release

    # Production mode with log type (default)
    python -m pkg.changelog

    # Production mode with release type
    python -m pkg.changelog --type release
"""

import argparse
from .run import run

def main():
    parser = argparse.ArgumentParser(description="Generate changelog documentation")
    parser.add_argument("--mode", choices=["prod", "dev"], default="prod",
                      help="Running mode: prod (production) or dev (development)")
    parser.add_argument("--type", choices=["log", "release"], default="log",
                      help="Type of logs to generate: log (regular git logs) or release (release logs)")
    args = parser.parse_args()
    run(args.mode, args.type)

if __name__ == "__main__":
    main()
