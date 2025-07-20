"""
CLI interface for Codex-AI.

Main entry point for the command-line interface using argparse.
Supports all commands: changelog, timetrack, map-tree, doc-ui.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from core.config import CodexConfig, set_config
from constants.project import get_version
from constants.ai import get_cli_model_choices


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog='codex-ai',
        description='🚀 Codex-AI - AI-powered development toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codex-ai changelog                     # Generate AI-powered changelog
  codex-ai timetrack --report           # Analyze development time
  codex-ai doc-ui                       # Generate documentation
  codex-ai config --api-key YOUR_KEY    # Configure settings

For detailed options and examples:
  codex-ai <command> --help

Configuration:
  codex-ai config --api-key YOUR_KEY        # Set API key (required for AI features)
  codex-ai config --list                    # Show current settings  
  codex-ai config --reset                   # Reset to defaults
  codex-ai config --help                    # See all configuration options
  
  Priority: CLI args > ENV vars > config file > defaults
  Config file: ~/.config/codex-ai/config.env

Environment Variables:
  ANTHROPIC_API_KEY                     # Required for AI features
  CODEX_DEFAULT_MODEL                   # Default AI model
  CODEX_OUTPUT_FORMAT                   # Default output format
  CODEX_VERBOSE                         # Enable verbose output
        """
    )
    
    # Global arguments
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
        choices=get_cli_model_choices(),
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
        help='Generate changelog since date (YYYY-MM-DD), tag, or commit hash (default: auto-detect latest tag)'
    )
    changelog_parser.add_argument(
        '--model',
        type=str,
        choices=get_cli_model_choices(),
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
    
    # Import and add timetrack arguments
    try:
        from commands.timetrack import add_timetrack_arguments
        add_timetrack_arguments(timetrack_parser)
    except ImportError:
        # Fallback to basic arguments if import fails
        timetrack_parser.add_argument(
            '--report',
            action='store_true',
            help='Generate detailed time tracking report'
        )
        timetrack_parser.add_argument(
            '--format',
            choices=['json', 'markdown', 'csv', 'html'],
            default='markdown',
            help='Output format for reports (default: markdown)'
        )
        timetrack_parser.add_argument(
            '--author',
            type=str,
            help='Filter commits by author name (partial match)'
        )
        timetrack_parser.add_argument(
            '--since',
            type=str,
            help='Filter commits since date (YYYY-MM-DD format)'
        )
        timetrack_parser.add_argument(
            '--until',
            type=str,
            help='Filter commits until date (YYYY-MM-DD format)'
        )
        timetrack_parser.add_argument(
            '--output', '-o',
            type=str,
            help='Save report to file (format auto-detected from extension)'
        )
    
    
    # Doc-UI command (intelligent documentation generation)
    doc_ui_parser = subparsers.add_parser(
        'doc-ui',
        help='Generate AI-powered documentation for React, Sass, and Storybook files'
    )
    
    # Import and add doc-ui arguments
    try:
        from commands.doc_ui import add_doc_ui_arguments
        add_doc_ui_arguments(doc_ui_parser)
    except ImportError:
        # Fallback to basic arguments if import fails
        doc_ui_parser.add_argument(
            '--mode',
            choices=['local', 'pipeline'],
            help='File detection mode (default: auto-detect)'
        )
        doc_ui_parser.add_argument(
            '--doc',
            choices=['react', 'sass', 'storybook', 'all'],
            default='all',
            help='Documentation type to generate (default: all)'
        )
        doc_ui_parser.add_argument(
            '--output-dir',
            type=str,
            default='docs',
            help='Output directory for documentation (default: docs)'
        )
        doc_ui_parser.add_argument(
            '--model',
            type=str,
            help='AI model to use (overrides config)'
        )
        doc_ui_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview mode - analyze files but don\'t generate documentation'
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
        
        # Set defaults from config
        output_file = args.output or ".tmp/changelog.md"
        verbose = config.get_verbose(cli_value=args.verbose)
        
        # Only pass model_name if explicitly specified by user
        # Let changelog auto-select if not specified
        success = run_changelog(
            output_file=output_file,
            since_commit=args.since,
            model_name=args.model,  # None if not specified
            verbose=verbose,
            dry_run=args.dry_run
        )
        
        return 0 if success else 1
        
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


def run_doc_ui_command(args, config: CodexConfig) -> int:
    """Run Doc-UI documentation generation command."""

    try:
        # Import here to avoid circular imports
        from commands.doc_ui import doc_ui_command
        
        # Set defaults from config
        verbose = config.get_verbose(cli_value=args.verbose)
        args.verbose = verbose
        
        # Call doc-ui command handler
        success = doc_ui_command(args)
        
        return 0 if success else 1
        
    except ImportError as e:
        print(f"❌ Doc-UI command not yet implemented: {e}")
        print("🚧 This feature is under development")
        return 1
    except Exception as e:
        print(f"❌ Error running doc-ui command: {e}")
        return 1




def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Initialize configuration
    try:
        config = CodexConfig()
        set_config(config)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 0
    
    # Validate API key for AI commands
    ai_commands = ['changelog', 'doc-ui']
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
        'doc-ui': run_doc_ui_command,
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
