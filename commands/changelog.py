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
    verbose: bool = False
) -> bool:
    """
    Generate changelog from git commits.
    
    Args:
        output_file: Output changelog file path
        since_commit: Generate changelog since this commit
        branch: Branch to analyze (default: current)
        model_name: AI model to use (default: anthropic/claude-4-sonnet-20250514)
        verbose: Enable verbose output
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if verbose:
            print("🚀 Starting changelog generation...")
        
        # Initialize git analyzer
        git_analyzer = GitLogAnalyzer()
        
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
        
        # Generate git log and check if it fits
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "git_log.txt")
            
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
                    print(f"⚠️ Detailed log too large ({tokens:,} tokens), trying simple...")
                
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
            
            # Create prompt file in temp directory too
            prompt_file = os.path.join(temp_dir, "prompt.md")
            prompt_content = get_changelog_prompt()
            
            with open(prompt_file, 'w') as f:
                f.write(prompt_content)
            
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
        verbose=args.verbose
    )
