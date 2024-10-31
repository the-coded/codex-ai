"""
Command-line interface for changelog generation.

For command-line usage:
    # Development mode
    python -m pkg.changelog --mode dev

    # Production mode (default)
    python -m pkg.changelog
"""

import argparse
from .run import run

def main():
    parser = argparse.ArgumentParser(description="Generate changelog documentation")
    parser.add_argument("--mode", choices=["prod", "dev"], default="prod",
                      help="Running mode: prod (production) or dev (development)")
    args = parser.parse_args()
    run(args.mode)

if __name__ == "__main__":
    main()
