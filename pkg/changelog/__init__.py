"""
Changelog generation module.

For programmatic usage:
    # Generate regular git logs (default)
    from pkg.changelog import run
    run()  # equivalent to run(type="log")

    # Generate release logs
    from pkg.changelog import run
    run(type="release")

Note: The module automatically detects if it's running from:
- Project root (when developing)
- Another project with .codex/ (when used as a tool)
"""

from .run import run, get_paths

__all__ = ['run', 'get_paths']
