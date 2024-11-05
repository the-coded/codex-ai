"""
Core implementation of the changelog generator.
"""

import subprocess
import sys
import os
from typing import Literal
from utils.get_base_path import get_base_path
from utils.get_token_count import get_token_count

LogType = Literal["log", "release"]

def generate_logs() -> None:
    """
    Generate all git logs. Release logs will only be generated
    if we're in a release.
    """
    base = get_base_path()
    script_prefix = f"{base}/bin"

    # Delete existing logs to avoid false positives
    log_files = [
        ".tmp/git_log_detailed.txt",
        ".tmp/git_log_simple.txt",
        ".tmp/git_release_detailed.txt",
        ".tmp/git_release_simple.txt"
    ]
    
    print("\n🗑️  Cleaning up old logs...")
    for log_file in log_files:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"   Deleted: {log_file}")

    try:
        # Generate regular logs
        print("\n📝 Generating git logs...")
        subprocess.run([f"{script_prefix}/git_log_detailed.sh"], check=True)
        subprocess.run([f"{script_prefix}/git_log_simple.sh"], check=True)
        print("✅ Git logs generated successfully")

        # Try to generate release logs
        print("\n📝 Generating release logs...")
        subprocess.run([f"{script_prefix}/git_release_detailed.sh"], check=True)
        subprocess.run([f"{script_prefix}/git_release_simple.sh"], check=True)
        print("✅ Release logs generated successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  No release logs generated, using regular logs")

def get_paths() -> tuple[str, str]:
    """
    Get the correct paths based on the current environment.
    If release logs exist, use them. Otherwise, use regular logs.
    
    Returns:
        tuple[str, str]: Prompt path and log path
    """
    base = get_base_path()
    prompt_path = f"{base}/pkg/changelog/prompt.md"
    token_threshold = 185_000

    # Check if release logs exist
    release_detailed = ".tmp/git_release_detailed.txt"
    release_simple = ".tmp/git_release_simple.txt"
    log_detailed = ".tmp/git_log_detailed.txt"
    log_simple = ".tmp/git_log_simple.txt"

    # If release logs exist, use them
    if os.path.exists(release_detailed) or os.path.exists(release_simple):
        print("\n📦 Using release logs")
        detailed_path = release_detailed
        simple_path = release_simple
    else:
        print("\n📦 Using regular logs")
        detailed_path = log_detailed
        simple_path = log_simple

    # Check if we should use simple logs based on token count
    token_count = get_token_count(detailed_path)

    print(f"\n📊 Token count: {token_count:,}")
    print(f"📊 Threshold: {token_threshold:,} tokens")

    if token_count > token_threshold:
        print("⚠️  Using simple logs due to size limit")
        log_path = simple_path
    else:
        print("✅ Using detailed logs")
        log_path = detailed_path

    return prompt_path, log_path

def run() -> None:
    """
    Runs the aider command to generate changelog documentation.
    """
    # Generate all logs
    generate_logs()
    
    # Get paths
    prompt_path, log_path = get_paths()
    
    # Install aider right before using it
    subprocess.run(["python", "-m", "shared.require_aider"], check=True)
    
    # Build and run aider command
    command = f"""aider \\
  --subtree-only \\
  --no-git \\
  --yes \\
  --sonnet \\
  --cache-prompts \\
  --no-stream \\
  --no-check-update \\
  --read {log_path}  \\
  --message-file {prompt_path} \\
  .tmp/changelog.md"""
    
    print()
    print(f"Running command: {command}")
    print()
    
    subprocess.run(command, shell=True)
    
    print()
