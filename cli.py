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
  codex-ai docs --type react           # Generate React docs
  codex-ai docs --type sass --output-dir ./documentation
  codex-ai analyze --git               # Git analysis
  codex-ai analyze --project --output analysis.json

Environment Variables:
  ANTHROPIC_API_KEY                     # Required for AI features
  CODEX_DEFAULT_MODEL                   # Default AI model
  CODEX_OUTPUT_FORMAT                   # Default output format
  CODEX_VERBOSE                         # Enable verbose output

Configuration:
  Create .env file or codex.config.yaml for persistent settings.
  Use 'codex-ai init' to create default configuration files.
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
        version='%(prog)s 1.0.0'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='<command>'
    )
    
    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize configuration files'
    )
    init_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing configuration files'
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
        help='Generate changelog since date (YYYY-MM-DD) or tag'
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


def run_init_command(args, config: CodexConfig) -> int:
    """Initialize configuration files."""
    try:
        # Create .env file if it doesn't exist
        env_file = Path('.env')
        if not env_file.exists() or args.force:
            env_example = Path('.env.example')
            if env_example.exists():
                import shutil
                shutil.copy(env_example, env_file)
                print(f"✅ Created .env file from template")
                print("🔑 Please edit .env and add your ANTHROPIC_API_KEY")
            else:
                print("⚠️ .env.example not found, creating basic .env")
                with open('.env', 'w') as f:
                    f.write("# Codex-AI Configuration\n")
                    f.write("ANTHROPIC_API_KEY=your-key-here\n")
                    f.write("CODEX_DEFAULT_MODEL=claude_4_sonnet\n")
                    f.write("CODEX_OUTPUT_FORMAT=markdown\n")
        else:
            print("ℹ️ .env file already exists (use --force to overwrite)")
        
        # Create config file
        config_file = 'codex.config.yaml'
        if not Path(config_file).exists() or args.force:
            config.create_default_config(config_file)
        else:
            print(f"ℹ️ {config_file} already exists (use --force to overwrite)")
        
        return 0
    except Exception as e:
        print(f"❌ Error initializing configuration: {e}")
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
            print("💡 Set it in .env file or use --api-key argument")
            print("🚀 Run 'codex-ai init' to create configuration files")
            return 1
    
    # Route to appropriate command handler
    command_handlers = {
        'init': run_init_command,
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
