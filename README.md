# 🤖 Codex-AI

> AI-powered development toolkit for intelligent changelog generation, time tracking, and code analysis.

[![PyPI version](https://badge.fury.io/py/codex-ai.svg)](https://pypi.org/project/codex-ai/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Install from PyPI
pip install codex-ai

# Set API key
codex-ai config --api-key sk-ant-your-key-here

# Generate AI-powered changelog
codex-ai changelog

# Analyze development time
codex-ai timetrack --report

# Generate uidocs documentation (auto-detects types)
codex-ai uidocs
```

## ✨ Features

- **📝 Smart Changelogs**: AI-generated from Git history using Claude models
- **⏱️ Time Tracking**: Intelligent commit time analysis with complexity factors
- **📚 Documentation**: Auto-generate docs for React, Sass, and Storybook
- **📊 Code Analysis**: Project insights, Git analysis, and complexity metrics
- **🔧 Flexible Configuration**: Environment variables, config files, and CLI options
- **🎯 AI Model Fallbacks**: Automatic fallback from Claude-4 → 3.7 → 3.5

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install codex-ai
```

### From Source (Development)
```bash
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai
pip install -e .
```

### Development Dependencies
```bash
pip install -r requirements-dev.txt
```

## ⚙️ Configuration

### 1. Set API Key (Required)
```bash
codex-ai config --api-key sk-ant-your-key-here
```

This saves your API key to `~/.config/codex-ai/config.env`

### 2. Configure Settings (Optional)
```bash
# Set default model
codex-ai config --model claude_3_7_sonnet

# Set output format
codex-ai config --output-format json

# Set output directory
codex-ai config --output-dir ./output

# View current settings
codex-ai config --list
```

### 3. Environment Variables (Alternative)
You can also use environment variables:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
export CODEX_DEFAULT_MODEL=claude_4_sonnet
export CODEX_OUTPUT_FORMAT=markdown
```

### 4. Configuration Hierarchy
The system uses a clear hierarchy for configuration values:

1. **CLI arguments** (highest priority)
2. **Environment variables** (CODEX_*)
3. **Global config file** (~/.config/codex-ai/config.env)
4. **Built-in defaults** (lowest priority)

This ensures predictable behavior and easy debugging of configuration issues.

## 🎯 Usage

### 📝 Changelog Generation
```bash
# Basic changelog
codex-ai changelog

# Custom output file
codex-ai changelog --output CHANGELOG.md

# Since specific date or tag
codex-ai changelog --since "2024-01-01"
codex-ai changelog --since "v1.0.0"

# Dry run (preview only)
codex-ai changelog --dry-run

# Custom AI model
codex-ai changelog --model claude_3_7_sonnet
```

### ⏱️ Time Tracking
```bash
# Basic time analysis
codex-ai timetrack

# Generate detailed report
codex-ai timetrack --report

# Filter by author
codex-ai timetrack --author "John Doe" --report

# Date range analysis
codex-ai timetrack --since "2024-01-01" --until "2024-12-31"

# Different output formats
codex-ai timetrack --report --format json
codex-ai timetrack --report --format html
codex-ai timetrack --report --format csv
```

### 📚 uidocs Documentation Generation
```bash
# Generate documentation (automatically detects React, Sass, Storybook)
codex-ai uidocs

# Custom project structure JSON file
codex-ai uidocs --json-path ./custom-structure.json

# Custom output directory
codex-ai uidocs --output-dir ./documentation

# Preview what would be generated
codex-ai uidocs --dry-run

# Custom AI model
codex-ai uidocs --model claude_3_7_sonnet
```

### 📊 Project Analysis
```bash
# Project structure mapping
codex-ai map-tree --project

# Git changes analysis
codex-ai map-tree --git

# Release changes analysis  
codex-ai map-tree --release

# Sibling files analysis
codex-ai map-tree --siblings

# Combined analysis with custom output
codex-ai map-tree --project --git --output analysis.json
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key (required) | - |
| `CODEX_DEFAULT_MODEL` | Default AI model | `claude_4_sonnet` |
| `CODEX_OUTPUT_FORMAT` | Default output format | `markdown` |
| `CODEX_OUTPUT_DIR` | Default output directory | `.tmp` |
| `CODEX_VERBOSE` | Enable verbose output | `false` |

## 🤖 AI Models & Token Management

### Intelligent Token Allocation
```python
# Using constants from constants/ai.py
effective_limit = (
    AI_MODELS["CLAUDE_4_SONNET"]["max_tokens"] -           # 200K context
    AI_MODELS["CLAUDE_4_SONNET"]["max_output_tokens"] -    # 64K response  
    TOKEN_STRATEGY["PROMPT_OVERHEAD"]                      # 15K prompt
) * TOKEN_STRATEGY["SAFETY_MARGIN"]                       # 95% safety
# Result: 114,950 tokens available for git log
```

### Token Distribution
- **Context Window**: `AI_MODELS.max_tokens` (200K)
- **AI Response**: `AI_MODELS.max_output_tokens` (64K) 
- **Prompt + Metadata**: `TOKEN_STRATEGY.PROMPT_OVERHEAD` (15K)
- **Safety Margin**: `TOKEN_STRATEGY.SAFETY_MARGIN` (95%)
- **Available for Git Log**: 114,950 tokens

### 3-Level Git Log Strategy
- **≤7 commits**: Detailed mode (full patches)
- **8-20 commits**: Medium mode (diff summary with `GIT_LOG_LIMITS`)
- **21+ commits**: Simple mode (file list only)

### Smart Fallback Chain
The system automatically cascades through modes:
1. **🥇 Detailed Mode** - Full patch analysis, maximum context
2. **🥈 Medium Mode** - Diff summaries (`MEDIUM_MAX_LINES_PER_FILE`: 50, `MEDIUM_MAX_LINE_LENGTH`: 200)
3. **🥉 Simple Mode** - File lists, always works

## 📁 Project Structure

```
codex-ai/
├── commands/           # CLI command implementations
├── core/              # Core business logic
│   ├── git/          # Git operations and analysis
│   ├── timetracker/  # Time tracking algorithms
│   ├── ai/           # AI model integration
│   └── uidocs/        # uidocs documentation (React, Sass, Storybook)
├── constants/         # Configuration constants
├── utils/            # Utility functions
├── formatters/       # Output formatting
├── templates/        # Markdown templates and prompts
├── cli.py           # Main CLI interface
├── config.py        # Configuration management
└── pyproject.toml   # Package configuration
```

## 🔄 Migration from Legacy Version

If you're migrating from the old shell script version:

1. **Install Codex-AI**: `pip install codex-ai`
2. **Set API Key**: `codex-ai config --api-key sk-ant-your-key-here`
3. **Replace Commands**:
   - `./bin/changelog.sh` → `codex-ai changelog`
   - `./pkg/timetracker/` → `codex-ai timetrack`
   - `./pkg/uidocs/` → `codex-ai uidocs`

## 🧪 Development

### Setup Development Environment
```bash
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai
pip install -r requirements-dev.txt
pip install -e .
```

### Local Development & Testing
📖 **[Local Development Guide](docs/local-developing.md)** - Complete guide for:
- Installing in development mode (`pip install -e .`)
- Verifying installation type (local vs PyPI)
- Development workflow and testing commands
- Troubleshooting common issues

### Run Tests
```bash
pytest
```

### Code Quality
```bash
black .
isort .
mypy .
flake8 .
```

## 📋 Examples

### Complete Workflow Example
```bash
# 1. Setup
pip install codex-ai
codex-ai config --api-key sk-ant-your-key-here

# 2. Generate changelog for release
codex-ai changelog --since "v1.0.0" --output CHANGELOG.md

# 3. Analyze development time for sprint
codex-ai timetrack --since "2024-01-01" --report --format html

# 4. Generate documentation
codex-ai uidocs --output-dir ./docs

# 5. Project analysis for review
codex-ai map-tree --project --git --output analysis.json
```

### Pipeline Integration (GitHub Actions)
```yaml
name: Generate Documentation
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install codex-ai
      - run: codex-ai changelog --output CHANGELOG.md
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - run: codex-ai uidocs
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/the-coded/codex-ai/issues)
- **Documentation**: [README](https://github.com/the-coded/codex-ai#readme)
- **Email**: gabriel@laplanta.com.br

## 🏷️ Version History

- **1.0.0** - Initial release with full feature parity
  - AI-powered changelog generation
  - Time tracking analysis
  - Documentation generation (React, Sass, Storybook)
  - Project analysis tools
  - Complete CLI interface

---

**Made with ❤️ by [laplanta](https://laplanta.com.br)**
