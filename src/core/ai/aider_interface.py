"""
Aider interface for Codex-AI.

Interface to run Aider commands using templates from constants.
"""

import os
import re
import subprocess
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from constants.ai import build_aider_command, AIDER_BASE_FLAGS, get_model_name_mapping
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
    
    def run_doc_ui_react(self, context_path: str, prompt_file: str, react_files: str) -> AiderResult:
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
            "DOC_UI_REACT",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            react_files=react_files
        )
        
        return self._execute_command(command)
    
    def run_doc_ui_sass(self, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
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
            "DOC_UI_SASS",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            sass_files=sass_files
        )
        
        return self._execute_command(command)
    
    def run_doc_ui_storybook(self, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
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
            "DOC_UI_STORYBOOK",
            model_key,
            context_path=context_path,
            prompt_file=prompt_file,
            storybook_files=storybook_files
        )
        
        return self._execute_command(command)
    
    def run_with_message_file(
        self, 
        prompt_file: str, 
        read_files: List[str] = None, 
        output_files: List[str] = None,
        additional_flags: List[List[str]] = None,
        verbose: bool = False
    ) -> AiderResult:
        """
        Generic method to run Aider with message file.
        
        @TODO Refactor existing methods (run_changelog, run_doc_ui_*) to use this generic method
        instead of duplicating command building logic. This would eliminate code duplication
        and provide a single point of maintenance for Aider execution.
        
        Args:
            prompt_file: Path to prompt file
            read_files: Files to read for context (optional)
            output_files: Files to write/modify (optional)
            additional_flags: Additional flags from template (optional)
            verbose: Enable verbose logging
            
        Returns:
            AiderResult with execution details
        """
        cmd = ["aider"] + AIDER_BASE_FLAGS.copy()
        cmd.extend(["--model", self.model.name])
        
        # Adicionar flags específicas do template
        if additional_flags:
            for flag_item in additional_flags:
                if len(flag_item) == 1:
                    cmd.append(flag_item[0])  # Flag sem valor
                elif len(flag_item) == 2:
                    cmd.extend([flag_item[0], flag_item[1]])  # Flag com valor
        
        cmd.extend(["--message-file", prompt_file])
        
        # Explícito: --read para cada arquivo de contexto
        if read_files:
            for read_file in read_files:
                cmd.extend(["--read", read_file])
        
        # Explícito: --file para cada arquivo de output  
        if output_files:
            for output_file in output_files:
                cmd.extend(["--file", output_file])
        
        command = " ".join(cmd)
        return self._execute_command(command, verbose=verbose)
    
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
        model_map = get_model_name_mapping()
        return model_map.get(self.model.name, "CLAUDE_4_SONNET")
    
    def _post_process_markdown_code_blocks(self, file_path: str) -> bool:
        """
        Convert [CODE_BLOCK] markers to standard triple backticks.
        
        This solves the issue where Aider interprets triple backticks as file delimiters
        and breaks generated markdown into multiple files.
        
        Args:
            file_path: Path to markdown file to process
            
        Returns:
            bool: True if successful, False if failed
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert [CODE_BLOCK:lang] to ```lang
            content = re.sub(r'\[CODE_BLOCK:(\w+)\]', r'```\1', content)
            
            # Convert [CODE_BLOCK] (without language) to ```
            content = content.replace('[CODE_BLOCK]', '```')
            
            # Convert [/CODE_BLOCK] to ```
            content = content.replace('[/CODE_BLOCK]', '```')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            # Non-critical error, just log and continue
            return False
    
    def _auto_process_generated_markdown(self, command: str, verbose: bool = False):
        """
        Automatically post-process all .md files mentioned in --file flags.
        
        This function extracts all .md file paths from the aider command
        and applies markdown code block post-processing to each one.
        
        Args:
            command: The aider command that was executed
            verbose: Enable verbose logging
        """
        try:
            # Extract all --file arguments from command
            file_pattern = r'--file\s+([^\s]+)'
            file_matches = re.findall(file_pattern, command)
            
            markdown_files = []
            for file_path in file_matches:
                if file_path.endswith('.md'):
                    markdown_files.append(file_path)
            
            if not markdown_files:
                return
            
            processed_count = 0
            for md_file in markdown_files:
                if self._post_process_markdown_code_blocks(md_file):
                    processed_count += 1
                    if verbose:
                        print(f"📝 Post-processed code blocks: {md_file}")
                else:
                    if verbose:
                        print(f"⚠️ Failed to post-process: {md_file}")
            
            if verbose and processed_count > 0:
                print(f"✅ Post-processed {processed_count}/{len(markdown_files)} markdown files")
                
        except Exception as e:
            if verbose:
                print(f"⚠️ Warning: Auto-processing failed: {e}")
    
    def _execute_command(self, command: str, verbose: bool = False) -> AiderResult:
        """Execute aider command."""
        try:
            if verbose:
                print(f"🔧 Executing Aider command:")
                print(f"   {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes
                env=self._get_env()
            )
            
            aider_result = AiderResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                command=command
            )
            
            # SEMPRE pós-processar arquivos .md gerados automaticamente
            if aider_result.success:
                self._auto_process_generated_markdown(command, verbose)
            
            # Log Aider response in verbose mode
            if verbose:
                print(f"📤 Aider Response:")
                print("   " + "─" * 60)
                if aider_result.success:
                    if aider_result.output:
                        # Show first 1000 chars of output
                        output_preview = aider_result.output[:1000]
                        formatted_output = output_preview.replace('\n', '\n   ')
                        print(f"   ✅ SUCCESS - Output ({len(aider_result.output)} chars):")
                        print(f"   {formatted_output}")
                        if len(aider_result.output) > 1000:
                            print(f"   ... (truncated, total: {len(aider_result.output)} chars)")
                    else:
                        print("   ✅ SUCCESS - No output")
                else:
                    print(f"   ❌ FAILED - Return code: {result.returncode}")
                    if aider_result.error:
                        error_preview = aider_result.error[:500]
                        formatted_error = error_preview.replace('\n', '\n   ')
                        print(f"   Error ({len(aider_result.error)} chars):")
                        print(f"   {formatted_error}")
                        if len(aider_result.error) > 500:
                            print(f"   ... (truncated, total: {len(aider_result.error)} chars)")
                print("   " + "─" * 60)
            
            return aider_result
            
        except Exception as e:
            error_result = AiderResult(
                success=False,
                output="",
                error=str(e),
                command=command
            )
            
            if verbose:
                print(f"📤 Aider Response:")
                print("   " + "─" * 60)
                print(f"   ❌ EXCEPTION: {str(e)}")
                print("   " + "─" * 60)
            
            return error_result
    
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
    return interface.run_doc_ui_react(context_path, prompt_file, react_files)


def run_sass_documentation(model: ModelInfo, context_path: str, prompt_file: str, sass_files: str) -> AiderResult:
    """Generate Sass documentation using Aider."""
    interface = AiderInterface(model)
    return interface.run_doc_ui_sass(context_path, prompt_file, sass_files)


def run_storybook_documentation(model: ModelInfo, context_path: str, prompt_file: str, storybook_files: str) -> AiderResult:
    """Generate Storybook documentation using Aider."""
    interface = AiderInterface(model)
    return interface.run_doc_ui_storybook(context_path, prompt_file, storybook_files)


def run_doc_ui_generation(model: ModelInfo, file_type: str, files: List[str], prompt_file: str, output_dir: List[str], verbose: bool = False) -> AiderResult:
    """
    Generate documentation using Aider for specific file type.
    
    Args:
        model: AI model to use
        file_type: Type of files (react, sass, storybook)
        files: List of context files to read for input
        prompt_file: Prompt file path
        output_dir: List of output files to write/modify
        verbose: Enable verbose output for Aider response logging
        
    Returns:
        AiderResult with execution details
    """
    interface = AiderInterface(model)
    
    # Convert lists to space-separated strings (following changelog pattern)
    context_files_str = " ".join(files)  # Files to read for context
    output_files_str = " ".join(output_dir)  # Files to write/modify
    
    # Route to appropriate documentation generator with verbose logging
    if file_type == "react":
        model_key = interface._get_model_key()
        command = build_aider_command(
            "DOC_UI_REACT",
            model_key,
            context_path=context_files_str,
            prompt_file=prompt_file,
            react_files=output_files_str
        )
        return interface._execute_command(command, verbose=verbose)
    elif file_type == "sass":
        model_key = interface._get_model_key()
        command = build_aider_command(
            "DOC_UI_SASS",
            model_key,
            context_path=context_files_str,
            prompt_file=prompt_file,
            sass_files=output_files_str
        )
        return interface._execute_command(command, verbose=verbose)
    elif file_type == "storybook":
        model_key = interface._get_model_key()
        command = build_aider_command(
            "DOC_UI_STORYBOOK",
            model_key,
            context_path=context_files_str,
            prompt_file=prompt_file,
            storybook_files=output_files_str
        )
        return interface._execute_command(command, verbose=verbose)
    else:
        return AiderResult(
            success=False,
            output="",
            error=f"Unknown file type: {file_type}",
            command=""
        )
