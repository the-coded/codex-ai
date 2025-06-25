"""
Aider interface for Codex-AI.

Interface to run Aider commands using templates from constants.
"""

import os
import subprocess
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from constants.ai import build_aider_command, AIDER_BASE_FLAGS
from .model_selector import ModelInfo


@dataclass
class AiderResult:
    """Result of Aider execution."""
    success: bool
    output: str
    error: str
    command: str


class AiderInterface:
    """Aider interface using command templates from constants."""
    
    def __init__(self, model: ModelInfo, api_key: Optional[str] = None):
        """Initialize with model and API key."""
        self.model = model
        self.api_key = api_key or self._get_api_key_from_config() or os.getenv('ANTHROPIC_API_KEY')
    
    def _get_api_key_from_config(self) -> Optional[str]:
        """Get API key from global config."""
        try:
            from core.config import get_config
            config = get_config()
            if config:
                return config.get_api_key()
        except Exception:
            pass
        return None
    
    def run_changelog(self, log_file: str, prompt_file: str, output_file: str) -> AiderResult:
        """
        Run Aider for changelog generation.
        
        Args:
            log_file: Git log file path
            prompt_file: Prompt file path
            output_file: Output changelog file
            
        Returns:
            AiderResult with execution details
        """
        # Find model key for command template
        model_key = self._get_model_key()
        
        # Build command using template
        command = build_aider_command(
            "CHANGELOG",
            model_key,
            log_file=log_file,
            prompt_file=prompt_file,
            output_file=output_file
        )
        
        return self._execute_command(command)
    
    def run_uidocs_react(self, context_path: str, prompt_file: str, react_files: str) -> AiderResult:
        """
        Run Aider for React documentation.
        
        Args:
            context_path: Context documentation path
            prompt_file: Prompt file path
            react_files: React files to process
            
        Returns:
            AiderResult with execution details
        """
        model_key = self._get_model_key()
        
        command = build_aider_command(
            "uidocs_REACT",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            react_files=react_files
        )
        
        return self._execute_command(command)
    
    def run_uidocs_sass(self, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
        """
        Run Aider for Sass documentation.
        
        Args:
            context_path: Context documentation path
            prompt_file: Prompt file path
            sass_files: Sass files to process
            
        Returns:
            AiderResult with execution details
        """
        model_key = self._get_model_key()
        
        command = build_aider_command(
            "uidocs_SASS",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            sass_files=sass_files
        )
        
        return self._execute_command(command)
    
    def run_uidocs_storybook(self, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
        """
        Run Aider for Storybook documentation.
        
        Args:
            context_path: Context documentation path
            prompt_file: Prompt file path
            storybook_files: Storybook files to process
            
        Returns:
            AiderResult with execution details
        """
        model_key = self._get_model_key()
        
        command = build_aider_command(
            "uidocs_STORYBOOK",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            storybook_files=storybook_files
        )
        
        return self._execute_command(command)
    
    def run_custom(self, prompt: str, files: List[str] = None, read_files: List[str] = None) -> AiderResult:
        """
        Run Aider with custom parameters.
        
        Args:
            prompt: The prompt text
            files: Files to modify (optional)
            read_files: Files to read for context (optional)
            
        Returns:
            AiderResult with execution details
        """
        cmd = ["aider"] + AIDER_BASE_FLAGS.copy()
        cmd.extend(["--model", self.model.name])
        cmd.extend(["--message", prompt])
        
        # Add read files for context
        if read_files:
            for read_file in read_files:
                cmd.extend(["--read", read_file])
        
        # Add files to modify
        if files:
            cmd.extend(files)
        
        command = " ".join(cmd)
        return self._execute_command(command)
    
    def _get_model_key(self) -> str:
        """Get model key for command templates."""
        # Map model names to keys
        model_map = {
            "anthropic/claude-4-sonnet-20250514": "CLAUDE_4_SONNET",
            "anthropic/claude-3-7-sonnet-latest": "CLAUDE_3_7_SONNET", 
            "anthropic/claude-3-5-sonnet-latest": "CLAUDE_3_5_SONNET"
        }
        
        return model_map.get(self.model.name, "CLAUDE_4_SONNET")
    
    def _execute_command(self, command: str) -> AiderResult:
        """Execute aider command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes
                env=self._get_env()
            )
            
            return AiderResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                command=command
            )
            
        except Exception as e:
            return AiderResult(
                success=False,
                output="",
                error=str(e),
                command=command
            )
    
    def _get_env(self) -> Dict[str, str]:
        """Get environment with API key."""
        env = os.environ.copy()
        if self.api_key:
            env['ANTHROPIC_API_KEY'] = self.api_key
        return env


# Convenience functions
def run_changelog_generation(model: ModelInfo, log_file: str, prompt_file: str, output_file: str) -> AiderResult:
    """Generate changelog using Aider."""
    interface = AiderInterface(model)
    return interface.run_changelog(log_file, prompt_file, output_file)


def run_react_documentation(model: ModelInfo, context_path: str, prompt_file: str, react_files: str) -> AiderResult:
    """Generate React documentation using Aider."""
    interface = AiderInterface(model)
    return interface.run_uidocs_react(context_path, prompt_file, react_files)


def run_sass_documentation(model: ModelInfo, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
    """Generate Sass documentation using Aider."""
    interface = AiderInterface(model)
    return interface.run_uidocs_sass(context_path, prompt_file, sass_files)


def run_storybook_documentation(model: ModelInfo, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
    """Generate Storybook documentation using Aider."""
    interface = AiderInterface(model)
    return interface.run_uidocs_storybook(context_path, prompt_file, storybook_files)
