"""
Entry point for running codex-ai as a module.

Usage:
    python -m codex_ai changelog
    python -m codex_ai timetrack
    python -m codex_ai doc-ui
    python -m codex_ai map-tree
"""

from cli import main

if __name__ == "__main__":
    main()
