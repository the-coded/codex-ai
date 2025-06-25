"""
Changelog command implementation.

Generates changelog from git commits using AI with simplified model selection.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from core.git.log_analyzer import GitLogAnalyzer
from core.ai.model_selector import get_default_model, get_model_by_name
from core.ai.token_manager import count_tokens
from core.ai.prompt_processor import get_changelog_prompt
from core.ai.aider_interface import run_changelog_generation
from constants.ai import get_effective_token_limit


def run_changelog(
    output_file: str = "CHANGELOG.md",
    since_commit: Optional[str] = None,
    branch: Optional[str] = None,
    model_name: Optional[str] = None,
    verbose: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Generate changelog from git commits.
    
    Args:
        output_file: Output changelog file path
        since_commit: Generate changelog since this commit
        branch: Branch to analyze (default: current)
        model_name: AI model to use (default: anthropic/claude-4-sonnet-20250514)
        verbose: Enable verbose output
        dry_run: Preview mode - analyze but don't generate files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if verbose:
            print("🚀 Starting changelog generation...")
        
        # Initialize git analyzer
        git_analyzer = GitLogAnalyzer()
        
        # Auto-detect latest tag if no since_commit specified
        if since_commit is None:
            latest_tag = git_analyzer.get_latest_tag()
            if latest_tag:
                since_commit = latest_tag
                print(f"📍 Auto-using since last tag: {latest_tag}")
            else:
                print("📍 No tags found - analyzing all history")
        
        # Get commit count for info
        if verbose:
            print("📊 Analyzing git history...")
        
        commit_count = git_analyzer.get_commit_count(since_commit, branch)
        if verbose:
            print(f"📈 Found {commit_count} commits to analyze")
        
        # Select model (default to Claude-4)
        if model_name:
            model = get_model_by_name(model_name)
            if not model:
                print(f"❌ Unknown model: {model_name}")
                return False
            if verbose:
                print(f"🤖 Using specified model: {model.name}")
        else:
            # Use Claude-4 as default
            model = get_default_model()
            if verbose:
                print(f"🤖 Using default model: {model.name}")
        
        # Get effective token limit with safety margin
        token_limit = get_effective_token_limit("CLAUDE_4_SONNET")
        
        # Generate git log using .tmp/ directly (like old system that worked)
        os.makedirs(".tmp", exist_ok=True)
        log_file = ".tmp/git_log.txt"
        
        # Clean any existing output file and Aider history to avoid conflicts
        if os.path.exists(output_file):
            os.remove(output_file)
            if verbose:
                print(f"🗑️ Cleaned existing output file: {output_file}")
        
        # Clean Aider history files that can inflate token count
        aider_files = [".aider.chat.history.md", ".aider.input.history"]
        for aider_file in aider_files:
            if os.path.exists(aider_file):
                os.remove(aider_file)
                if verbose:
                    print(f"🗑️ Cleaned Aider history: {aider_file}")
        
        # Try detailed first
        if verbose:
            print("📋 Generating detailed git log...")
        
        success = git_analyzer.generate_detailed_log(log_file, since_commit, branch)
        if not success:
            print("❌ Failed to generate git log")
            return False
        
        # Count tokens using our utility
        with open(log_file, 'r') as f:
            log_content = f.read()
        tokens = count_tokens(log_content)
        
        if verbose:
            print(f"📊 Detailed log tokens: {tokens:,}")
        
        # Check if detailed log fits in model
        if tokens > token_limit:
            if verbose:
                print(f"⚠️ Detailed log too large ({tokens:,} tokens), trying medium...")
            
            # Try medium log
            success = git_analyzer.generate_medium_log(log_file, since_commit, branch)
            if not success:
                print("❌ Failed to generate medium git log")
                return False
            
            with open(log_file, 'r') as f:
                log_content = f.read()
            tokens = count_tokens(log_content)
            
            if verbose:
                print(f"📊 Medium log tokens: {tokens:,}")
            
            # If medium is still too large, try simple
            if tokens > token_limit:
                if verbose:
                    print(f"⚠️ Medium log too large ({tokens:,} tokens), trying simple...")
                
                # Try simple log
                success = git_analyzer.generate_simple_log(log_file, since_commit, branch)
                if not success:
                    print("❌ Failed to generate simple git log")
                    return False
                
                with open(log_file, 'r') as f:
                    log_content = f.read()
                tokens = count_tokens(log_content)
                
                if verbose:
                    print(f"📊 Simple log tokens: {tokens:,}")
                
                if tokens > token_limit:
                    print(f"❌ Even simple log too large ({tokens:,} tokens)")
                    return False
        
        # Create prompt file in .tmp/ too (like old system)
        prompt_file = ".tmp/prompt.md"
        prompt_content = get_changelog_prompt()
        
        with open(prompt_file, 'w') as f:
            f.write(prompt_content)
        
        # Dry run mode - show preview and stop before AI generation
        if dry_run:
            print("🔍 DRY RUN MODE - Preview only, NO AI calls (no costs)")
            print(f"📄 Would generate: {output_file}")
            print(f"📊 Git log tokens: {tokens:,}")
            print(f"📊 Token limit: {token_limit:,}")
            print(f"🤖 Would use model: {model.name}")
            print(f"💰 AI costs: $0.00 (dry run - no API calls made)")
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📄 Git log file: {log_file} (exists: {os.path.exists(log_file)})")
            print(f"📄 Prompt file: {prompt_file} (exists: {os.path.exists(prompt_file)})")
            
            # Show git log preview
            if verbose and os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_preview = f.read()
                if log_preview:
                    print("\n📋 Git Log Preview (first 500 chars):")
                    print("─" * 50)
                    print(log_preview[:500] + ("..." if len(log_preview) > 500 else ""))
                    print("─" * 50)
                else:
                    print("\n⚠️  Git log is empty - no commits to analyze")
            
            print("✅ Dry run completed - no files generated, no AI costs incurred")
            return True
        
        if verbose:
            print("🤖 Running AI generation...")
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📄 Log file path: {log_file}")
            print(f"📄 Prompt file path: {prompt_file}")
            print(f"📄 Output file path: {output_file}")
            print(f"📄 Log file exists: {os.path.exists(log_file)}")
            print(f"📄 Prompt file exists: {os.path.exists(prompt_file)}")
        
        # Run Aider for changelog generation
        result = run_changelog_generation(
            model=model,
            log_file=log_file,
            prompt_file=prompt_file,
            output_file=output_file
        )
        
        if result.success:
            if verbose:
                print(f"✅ Changelog generated successfully: {output_file}")
                if result.output:
                    print("📄 AI Output:")
                    print(result.output)
            return True
        else:
            print(f"❌ Failed to generate changelog: {result.error}")
            if verbose and result.command:
                print(f"🔧 Command: {result.command}")
            return False
                
    except Exception as e:
        print(f"❌ Error generating changelog: {e}")
        return False


def changelog_command(args):
    """CLI command handler for changelog generation."""
    return run_changelog(
        output_file=args.output,
        since_commit=args.since,
        branch=args.branch,
        model_name=args.model,
        verbose=args.verbose,
        dry_run=args.dry_run
    )
