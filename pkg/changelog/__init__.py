"""
Changelog generation module.

For programmatic usage:
    # Development mode with log type (default)
    from pkg.changelog import run
    run(mode="dev", type="log")

    # Development mode with release type
    from pkg.changelog import run
    run(mode="dev", type="release")

    # Production mode with log type (default)
    from .codex.pkg.changelog import run
    run()  # equivalent to run(mode="prod", type="log")

    # Production mode with release type
    from .codex.pkg.changelog import run
    run(type="release")  # equivalent to run(mode="prod", type="release")
"""

from .run import run, get_paths

__all__ = ['run', 'get_paths']
