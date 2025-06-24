"""
CLI interface for Codex-AI.

Main entry point for the command-line interface using argparse.
Supports all commands: changelog, timetrack, docs, analyze.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from config import CodexConfig, set_config
from constants.project import get_version


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog='codex-ai',
        description='🚀 Codex-AI - AI-powered development toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codex-ai changelog                     # Generate changelog
  codex-ai changelog --output changelog.md --dry-run
  codex-ai timetrack --report           # Time analysis with report
  codex-ai timetrack --author "John" --since "2024-01-01"
  codex-ai uidocs                       # Generate documentation (auto-detects types)
  codex-ai uidocs --output-dir ./documentation
  codex-ai analyze --git               # Git analysis
  codex-ai analyze --project --output analysis.json

Environment Variables:
  ANTHROPIC_API_KEY                     # Required for AI features
  CODEX_DEFAULT_MODEL                   # Default AI model
  CODEX_OUTPUT_FORMAT                   # Default output format
  CODEX_VERBOSE                         # Enable verbose output

Configuration:
  Use 'codex-ai config --api-key YOUR_KEY' to save settings globally.
  Or set ANTHROPIC_API_KEY environment variable.
        """
    )
    
    # Global arguments
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file (YAML or JSON)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--output-format',
        choices=['json', 'yaml', 'markdown', 'html', 'text'],
        help='Output format (default: markdown)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (overrides env var)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {get_version()}'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='<command>'
    )
    
    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Manage global configuration settings'
    )
    config_parser.add_argument(
        '--api-key',
        type=str,
        help='Set Anthropic API key'
    )
    config_parser.add_argument(
        '--model',
        type=str,
        choices=['claude_4_sonnet', 'claude_3_7_sonnet', 'claude_3_5_sonnet'],
        help='Set default AI model'
    )
    config_parser.add_argument(
        '--output-format',
        type=str,
        choices=['json', 'yaml', 'markdown', 'html', 'text'],
        help='Set default output format'
    )
    config_parser.add_argument(
        '--output-dir',
        type=str,
        help='Set default output directory'
    )
    config_parser.add_argument(
        '--verbose',
        type=str,
        choices=['true', 'false'],
        help='Set verbose mode (true/false)'
    )
    config_parser.add_argument(
        '--fallback-models',
        type=str,
        help='Set fallback models (comma-separated)'
    )
    config_parser.add_argument(
        '--git-timeout',
        type=int,
        help='Set Git command timeout in seconds'
    )
    config_parser.add_argument(
        '--ai-timeout',
        type=int,
        help='Set AI command timeout in seconds'
    )
    config_parser.add_argument(
        '--ai-retry-attempts',
        type=int,
        help='Set AI retry attempts'
    )
    config_parser.add_argument(
        '--list',
        action='store_true',
        help='Show current configuration settings'
    )
    config_parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset configuration to defaults'
    )
    
    # Changelog command
    changelog_parser = subparsers.add_parser(
        'changelog',
        help='Generate AI-powered changelog from Git history'
    )
    changelog_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: .tmp/changelog.md)'
    )
    changelog_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without executing'
    )
    changelog_parser.add_argument(
        '--since',
        type=str,
        help='Generate changelog since date (YYYY-MM-DD), tag, or commit hash'
    )
    changelog_parser.add_argument(
        '--model',
        type=str,
        help='AI model to use (overrides config)'
    )
    changelog_parser.add_argument(
        '--template',
        type=str,
        help='Custom template file path'
    )
    
    # Timetrack command
    timetrack_parser = subparsers.add_parser(
        'timetrack',
        help='Analyze development time from Git commits'
    )
    timetrack_parser.add_argument(
        '--report',
        action='store_true',
        help='Generate detailed report'
    )
    timetrack_parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'html', 'csv'],
        default='markdown',
        help='Report format (default: markdown)'
    )
    timetrack_parser.add_argument(
        '--author',
        type=str,
        help='Filter commits by author'
    )
    timetrack_parser.add_argument(
        '--since',
        type=str,
        help='Analyze commits since date (YYYY-MM-DD)'
    )
    timetrack_parser.add_argument(
        '--until',
        type=str,
        help='Analyze commits until date (YYYY-MM-DD)'
    )
    timetrack_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path'
    )
    
    # uidocs command (intelligent documentation generation)
    uidocs_parser = subparsers.add_parser(
        'uidocs',
        help='Generate uidocs documentation (React, Sass, Storybook) - automatically detects types'
    )
    uidocs_parser.add_argument(
        '--json-path',
        type=str,
        default='.tmp/tree_project.json',
        help='Path to project structure JSON file (default: .tmp/tree_project.json)'
    )
    uidocs_parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='./docs',
        help='Output directory (default: ./docs)'
    )
    uidocs_parser.add_argument(
        '--model',
        type=str,
        help='AI model to use (overrides config)'
    )
    uidocs_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be generated without executing'
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze project structure and Git history'
    )
    analyze_parser.add_argument(
        '--git',
        action='store_true',
        help='Analyze Git history and changes'
    )
    analyze_parser.add_argument(
        '--project',
        action='store_true',
        help='Analyze project structure'
    )
    analyze_parser.add_argument(
        '--complexity',
        action='store_true',
        help='Analyze code complexity'
    )
    analyze_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path'
    )
    analyze_parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'markdown', 'html'],
        default='json',
        help='Output format (default: json)'
    )
    
    return parser


def run_config_command(args, config: CodexConfig) -> int:
    """Run configuration management command."""
    try:
        # Import here to avoid circular imports
        from commands.config import run_config
        return run_config(args, config)
    except ImportError as e:
        print(f"❌ Config command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running config command: {e}")
        return 1


def run_changelog_command(args, config: CodexConfig) -> int:
    """Run changelog generation command."""
    try:
        # Import here to avoid circular imports
        from commands.changelog import run_changelog
        return run_changelog(args, config)
    except ImportError as e:
        print(f"❌ Changelog command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running changelog command: {e}")
        return 1


def run_timetrack_command(args, config: CodexConfig) -> int:
    """Run timetrack analysis command."""
    try:
        # Import here to avoid circular imports
        from commands.timetrack import run_timetrack
        return run_timetrack(args, config)
    except ImportError as e:
        print(f"❌ Timetrack command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running timetrack command: {e}")
        return 1


def run_uidocs_command(args, config: CodexConfig) -> int:
    """Run uidocs documentation generation command."""
    try:
        # Import here to avoid circular imports
        from commands.uidocs import run_uidocs
        return run_uidocs(args, config)
    except ImportError as e:
        print(f"❌ uidocs command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running uidocs command: {e}")
        return 1


def run_analyze_command(args, config: CodexConfig) -> int:
    """Run project analysis command."""
    try:
        # Import here to avoid circular imports
        from commands.analyze import run_analyze
        return run_analyze(args, config)
    except ImportError as e:
        print(f"❌ Analyze command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running analyze command: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Initialize configuration
    try:
        config = CodexConfig(config_path=args.config)
        set_config(config)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 0
    
    # Validate API key for AI commands
    ai_commands = ['changelog', 'uidocs']
    if args.command in ai_commands:
        api_key = config.get_api_key(cli_value=args.api_key)
        if not api_key:
            print("❌ Error: ANTHROPIC_API_KEY is required for AI features")
            print("💡 Set it with: codex-ai config --api-key YOUR_KEY")
            print("🔧 Or use --api-key argument or set ANTHROPIC_API_KEY env var")
            return 1
    
    # Route to appropriate command handler
    command_handlers = {
        'config': run_config_command,
        'changelog': run_changelog_command,
        'timetrack': run_timetrack_command,
        'uidocs': run_uidocs_command,
        'analyze': run_analyze_command,
    }
    
    handler = command_handlers.get(args.command)
    if not handler:
        print(f"❌ Unknown command: {args.command}")
        return 1
    
    try:
        return handler(args, config)
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 130
    except Exception as e:
        if config.get_verbose(cli_value=args.verbose):
            import traceback
            traceback.print_exc()
        else:
            print(f"❌ Error: {e}")
            print("💡 Use --verbose for detailed error information")
        return 1


if __name__ == "__main__":
    sys.exit(main())
