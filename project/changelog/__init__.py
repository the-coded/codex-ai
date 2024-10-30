"""
Changelog generation module.

For programmatic usage:
    # Development mode
    from project.changelog import run
    run(mode="dev")

    # Production mode (default)
    from .nexus.project.changelog import run
    run()
"""

from .run import run, get_paths

__all__ = ['run', 'get_paths']
