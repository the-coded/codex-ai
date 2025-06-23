"""
Changelog generation module.

For programmatic usage:
    from pkg.changelog import run
    run()  # Will use release logs if available, otherwise regular logs

Note: The module automatically detects:
- Environment: Project root or another project with .codex/
- Log type: Release logs if available, otherwise regular logs
"""

from .run import run, get_paths

__all__ = ['run', 'get_paths']
