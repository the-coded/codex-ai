"""
Entry point for running codex-ai as a module.

Usage:
    python -m codex_ai changelog
    python -m codex_ai timetrack --report
    python -m codex_ai docs --type react
    python -m codex_ai analyze --git
"""

from cli import main

if __name__ == "__main__":
    main()
