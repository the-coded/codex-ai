"""
Core implementation of the changelog generator.
"""

import subprocess
from utils.get_base_path import get_base_path

def get_paths(mode: str = "prod") -> tuple[str, str, str]:
    """
    Get the correct paths based on whether we're running in production or development mode.
    
    Args:
        mode (str): Running mode, either "prod" or "dev" (default: "prod")
            - "prod": Running from .nexus in another repository
            - "dev": Running locally from codex repository
    
    Returns:
        tuple[str, str, str]: Template path, prompt path, and log path
    """
    base = get_base_path(mode)
    prompt_path = f"{base}/pkg/changelog/prompt.md"
    log_path = ".tmp/git_log_detailed.txt"
    return prompt_path, log_path

def run(mode: str = "prod") -> None:
    """
    Runs the aider command to generate changelog documentation.
    
    Args:
        mode (str): Running mode, either "prod" or "dev" (default: "prod")
            - "prod": Running from .nexus in another repository
            - "dev": Running locally from codex repository
    """
    prompt_path, log_path = get_paths(mode)
    
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
