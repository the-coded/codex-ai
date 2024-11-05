"""
Core implementation of the changelog generator.
"""

import subprocess
import sys
from typing import Literal
from utils.get_base_path import get_base_path
from utils.get_token_count import get_token_count

LogType = Literal["log", "release"]

def generate_logs(type: LogType = "log") -> None:
    """
    Generate git logs using the appropriate scripts.
    
    Args:
        type (LogType): Type of logs to generate, either "log" or "release" (default: "log")
            - "log": Generate regular git logs
            - "release": Generate release logs
    """
    base = get_base_path()
    script_prefix = f"{base}/bin"

    try:
        if type == "log":
            print("\n📝 Generating git logs...")
            subprocess.run([f"{script_prefix}/git_log_detailed.sh"], check=True)
            subprocess.run([f"{script_prefix}/git_log_simple.sh"], check=True)
            print("✅ Git logs generated successfully")
        else:  # release
            print("\n📝 Generating release logs...")
            subprocess.run([f"{script_prefix}/git_release_detailed.sh"], check=True)
            subprocess.run([f"{script_prefix}/git_release_simple.sh"], check=True)
            print("✅ Release logs generated successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating {'release' if type == 'release' else ''} logs: {e}")
        sys.exit(1)

def get_paths(type: LogType = "log") -> tuple[str, str]:
    """
    Get the correct paths based on the current environment.
    
    Args:
        type (LogType): Type of logs to use, either "log" or "release" (default: "log")
            - "log": Use regular git logs
            - "release": Use release logs
    
    Returns:
        tuple[str, str]: Prompt path and log path
    """
    base = get_base_path()
    prompt_path = f"{base}/pkg/changelog/prompt.md"
    token_threshold = 185_000
    detailed_path = f".tmp/git_{type}_detailed.txt"
    simple_path = f".tmp/git_{type}_simple.txt"

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

def run(type: LogType = "log") -> None:
    """
    Runs the aider command to generate changelog documentation.
    
    Args:
        type (LogType): Type of logs to generate, either "log" or "release" (default: "log")
            - "log": Generate regular git logs
            - "release": Generate release logs
    """
    # Generate logs first
    generate_logs(type)
    
    # Get paths
    prompt_path, log_path = get_paths(type)
    
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
