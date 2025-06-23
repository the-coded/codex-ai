# 🤖 Aider Integration Guide

This guide covers how to use aider-chat with Codex for AI-powered development and documentation generation.

## 🎯 Overview

Aider is an AI pair programming tool that works seamlessly with Codex-generated data. By combining Codex's project analysis capabilities with Aider's AI-powered code generation, you can create powerful workflows for documentation, refactoring, and development.

## 🚀 Setup & Installation

### 1. Install Aider
```bash
# Using the Codex helper script (recommended)
python shared/require_aider-chat.py

# Or install manually
pip install aider-chat==0.60.0

# Verify installation
aider --version
```

### 2. Check Available Models
```bash
# List all available models
aider --models

# Common models you'll see:
# - claude-3-5-sonnet-20241022 (recommended for complex tasks)
# - claude-3-haiku-20240307 (faster, good for simple tasks)
# - gpt-4o (OpenAI alternative)
# - gpt-4o-mini (faster OpenAI option)
```

## 🔧 Configuration

### API Key Setup

#### Option 1: Environment Variable (Recommended)
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Or set for current session
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### Option 2: .env File
```bash
# Create .env file in your project root
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# Aider will automatically load from .env
```

#### Option 3: Command Line
```bash
# Pass API key directly (not recommended for security)
aider --api-key sk-ant-your-key-here
```

### Verify Configuration
```bash
# Test API connection
aider --model claude-3-5-sonnet-20241022 --no-git --exit

# Should show successful connection without errors
```

## 🤖 Basic Usage

### Starting Aider
```bash
# Start with default model (Claude 3.5 Sonnet)
aider

# Start with specific model
aider --model claude-3-5-sonnet-20241022

# Start with faster model for simple tasks
aider --model claude-3-haiku-20240307

# Start without git integration (useful for analysis only)
aider --no-git
```

### Essential Aider Commands
```bash
# Inside aider session:
/help           # Show all commands
/add <file>     # Add file to chat context
/drop <file>    # Remove file from context
/ls             # List files in context
/clear          # Clear chat history
/exit           # Exit aider
/undo           # Undo last change
/commit         # Commit changes
/diff           # Show pending changes
```

### Adding Files to Context
```bash
# Add specific files
/add README.md
/add src/main.py

# Add multiple files
/add *.py
/add docs/*.md

# Add Codex-generated analysis files
/add .tmp/tree_project.json
/add .tmp/git_log_detailed.txt
```

## 🔄 Integration with Codex

### Typical Workflow

#### 1. Generate Codex Analysis
```bash
# First, generate project analysis with Codex
cd codex-ai
source bin/start.sh
./bin/tree_generate_all.sh
```

#### 2. Start Aider with Context
```bash
# Start aider and add Codex outputs
aider --model claude-3-5-sonnet-20241022

# Inside aider, add analysis files
/add .tmp/tree_project.json
/add .tmp/git_log_detailed.txt
/add .tmp/tree_git_changed.json
```

#### 3. Use AI with Rich Context
Now you can ask Aider to:
- Generate documentation based on project structure
- Create changelogs from git history
- Refactor code with full project context
- Analyze architecture and suggest improvements

### Pre-configured Startup Script
```bash
# Create a helper script: start-aider-with-codex.sh
#!/bin/bash
echo "🚀 Starting Aider with Codex context..."

# Generate fresh analysis
./bin/tree_generate_all.sh

# Start aider with pre-loaded context
aider --model claude-3-5-sonnet-20241022 \
  --read .tmp/tree_project.json \
  --read .tmp/git_log_detailed.txt \
  --read .tmp/tree_git_changed.json

# Make it executable
chmod +x start-aider-with-codex.sh
```

## 💡 Practical Examples

### 1. Generate Documentation from Project Analysis
```bash
# Start aider with project context
aider --model claude-3-5-sonnet-20241022
/add .tmp/tree_project.json

# Prompt example:
"""
Based on the project structure in tree_project.json, create a comprehensive 
README.md that includes:
1. Project overview
2. Directory structure explanation
3. Key components and their purposes
4. Installation and usage instructions
"""
```

### 2. Create Intelligent Changelog
```bash
# Add git history context
/add .tmp/git_log_detailed.txt
/add .tmp/tree_git_changed.json

# Prompt example:
"""
Based on the git history and changed files, create a professional changelog 
entry for the latest release. Include:
1. New features
2. Bug fixes
3. Breaking changes
4. Technical improvements
"""
```

### 3. Code Refactoring with Context
```bash
# Add specific files and project context
/add src/main.py
/add .tmp/tree_project.json

# Prompt example:
"""
Analyze main.py in the context of the overall project structure. 
Suggest refactoring improvements for:
1. Code organization
2. Performance optimizations
3. Better error handling
4. Consistency with project patterns
"""
```

### 4. Architecture Analysis
```bash
# Add multiple analysis files
/add .tmp/tree_project.json
/add .tmp/tree_git_siblings.json

# Prompt example:
"""
Analyze the project architecture and provide:
1. Current architecture overview
2. Potential issues or code smells
3. Suggestions for improvement
4. Best practices recommendations
"""
```

## 🛠️ Advanced Usage

### Model Selection Strategy

#### For Complex Tasks (Documentation, Architecture)
```bash
aider --model claude-3-5-sonnet-20241022
# Best for: Complex analysis, documentation generation, architecture decisions
```

#### For Quick Tasks (Simple fixes, formatting)
```bash
aider --model claude-3-haiku-20240307
# Best for: Quick fixes, formatting, simple refactoring
```

#### For OpenAI Users
```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-openai-key"

# Use GPT-4
aider --model gpt-4o
```

### Batch Processing
```bash
# Process multiple files with same prompt
aider --model claude-3-5-sonnet-20241022 \
  --message "Add comprehensive docstrings to all functions" \
  src/*.py
```

### Configuration File
```bash
# Create ~/.aider.conf.yml
model: claude-3-5-sonnet-20241022
no-git: false
auto-commits: true
show-diffs: true

# Aider will use these settings by default
```

### Integration with Git
```bash
# Aider can automatically commit changes
aider --auto-commits

# Review changes before committing
aider --show-diffs

# Work on specific branch
git checkout feature-branch
aider
```

## 🔧 Troubleshooting

### Common Issues

#### API Key Not Found
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# If empty, set it:
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Or check .env file
cat .env | grep ANTHROPIC_API_KEY
```

#### Model Not Available
```bash
# List available models
aider --models

# Use a different model if your preferred one isn't available
aider --model claude-3-haiku-20240307
```

#### Connection Issues
```bash
# Test API connection
curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

#### File Context Issues
```bash
# Check what files are in context
/ls

# Remove problematic files
/drop problematic-file.txt

# Clear all context and start fresh
/clear
```

### Debug Mode
```bash
# Run aider with verbose output
aider --verbose

# Check aider logs
tail -f ~/.aider/aider.log
```

## 💡 Best Practices

### Context Management
- **Start Small**: Begin with essential files, add more as needed
- **Use .tmp/ Files**: Leverage Codex analysis for rich context
- **Regular Cleanup**: Use `/clear` to reset context when switching tasks
- **File Relevance**: Only add files relevant to current task

### Prompt Engineering
- **Be Specific**: Clear, detailed prompts get better results
- **Provide Context**: Reference the analysis files you've added
- **Iterative Approach**: Break complex tasks into smaller steps
- **Review Changes**: Always review generated code before committing

### Performance Optimization
- **Model Selection**: Use Haiku for simple tasks, Sonnet for complex ones
- **Batch Similar Tasks**: Process related files together
- **Context Size**: Monitor context size, remove unnecessary files

### Security
- **API Key Safety**: Never commit API keys to version control
- **Code Review**: Always review AI-generated code
- **Backup**: Commit your work before major AI-assisted changes

## 🔗 Integration Workflows

### Codex → Aider → Documentation
```bash
# 1. Generate analysis
./bin/tree_generate_all.sh

# 2. Start aider with context
aider --read .tmp/tree_project.json

# 3. Generate docs
# Prompt: "Create API documentation based on project structure"
```

### Codex → Aider → Refactoring
```bash
# 1. Analyze changes
./bin/tree_git_changes.sh

# 2. Start aider with change context
aider --read .tmp/tree_git_changed.json --read src/main.py

# 3. Refactor with context
# Prompt: "Refactor based on recent changes and project patterns"
```

### Codex → Aider → Testing
```bash
# 1. Generate project structure
./bin/tree_project.sh . .tmp/current.json

# 2. Add test context
aider --read .tmp/current.json --read src/*.py

# 3. Generate tests
# Prompt: "Create comprehensive tests for all modules"
```

## 🔗 Related Documentation

- [📖 Local Development Guide](local-development.md) - General local development setup
- [📖 Scripts Documentation](../bin/README.md) - Codex analysis scripts
- [📖 Utilities Documentation](../utils/README.md) - Python utilities
- [🔄 Pipeline Execution Guide](pipeline-execution.md) - CI/CD integration
