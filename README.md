<div align="center">

# 🤖 Codex-AI

<img src="assets/codex.png" alt="Codex-AI Logo" width="50%">  

[![PyPI version](https://badge.fury.io/py/codex-ai.svg)](https://pypi.org/project/codex-ai/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🔭 Overview

**Codex-AI** is a centralized AI-powered development toolkit that serves as the core hub of intelligent automation across development workflows. Inspired by ancient codices—volumes of knowledge meticulously compiled and preserved—Codex-AI is designed to be the modern evolution of development intelligence, bringing together AI-driven changelog generation and documentation automation in one organized platform.

Just as ancient codices preserved humanity's knowledge through generations, our Codex-AI aims to preserve and evolve development insights through intelligent automation and AI-powered analysis.

## 📋 Table of Contents
- [🔭 Overview](#-overview)
- [🌟 Introduction](#-introduction)
- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎯 Usage](#-usage)
- [🔧 Environment Variables](#-environment-variables)
- [🤖 AI Models & Token Management](#-ai-models--token-management)
- [📁 Project Structure](#-project-structure)
- [🔄 Migration from Legacy Version](#-migration-from-legacy-version)
- [🧪 Development](#-development)
- [📋 Examples](#-examples)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🆘 Support](#-support)
- [🏷️ Version History](#️-version-history)

## 🌟 Introduction

Codex-AI is more than just a development toolkit; it is a **strategic intelligence repository** that transforms development workflows through AI-powered automation. With Codex-AI, you can harness the power of Claude models to generate intelligent changelogs, analyze development patterns, create comprehensive documentation, and gain deep insights into your codebase—all within a centralized framework that adapts to complex project environments.

### ✨ Key Highlights:
- **🏛️ Centralized Intelligence**: Generate, analyze, and organize development insights through AI-powered automation in one unified platform.
- **🤖 Advanced AI Integration**: Leverages Claude-4, Claude-3.7, and Claude-3.5 models with intelligent fallback chains for robust automation.
- **🔄 Universal Compatibility**: Works seamlessly across languages, frameworks, and development workflows, making it a universal tool for modern development teams.
- **📊 Deep Analytics**: Transforms raw Git data into actionable insights through intelligent analysis and complexity metrics.

## 🚀 Quick Start

```bash
# Install from PyPI
pip install codex-ai

# Set API key
codex-ai config --api-key sk-ant-your-key-here

# Generate AI-powered changelog
codex-ai changelog

# Generate documentation (auto-detects types)
codex-ai doc-ui
```

## ✨ Features

- **📝 Smart Changelogs**: AI-generated from Git history using Claude models
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

### Development Dependencies (Optional)
```bash
# Basic installation (required dependencies only)
pip install -e .

# Enhanced installation with optional dependencies
pip install -e ".[all]"          # All optional dependencies
pip install -e ".[performance]"  # ujson, orjson for better performance
pip install -e ".[rich]"         # rich, colorama for enhanced CLI output
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

**🎯 Smart Tag Detection**: By default, `codex-ai changelog` automatically detects the latest Git tag and generates changelog since that tag. This provides optimal token usage and focuses on changes since the last release.

```bash
# Basic changelog (auto-detects latest tag)
codex-ai changelog
# 📍 Auto-using since last tag: v1.0.0

# Custom output file
codex-ai changelog --output CHANGELOG.md

# Override auto-detection with specific date or tag
codex-ai changelog --since "2024-01-01"
codex-ai changelog --since "v1.0.0"
codex-ai changelog --since "HEAD~10"

# Dry run (preview only, no AI costs)
codex-ai changelog --dry-run

# Custom AI model
codex-ai changelog --model claude_3_7_sonnet
```

**💡 Tag Detection Behavior**:
- **With tags**: Automatically uses latest tag as starting point (optimal token usage)
- **Without tags**: Analyzes entire Git history (first release scenario)
- **Manual override**: Use `--since` to specify custom starting point

### 📚 Doc-UI Documentation Generation

```bash
# Auto-detect and generate all documentation types
codex-ai doc-ui

# Process specific path  
codex-ai doc-ui --path react/src/components/Button

# Generate only React documentation
codex-ai doc-ui --doc react

# Pipeline mode with specific commit
codex-ai doc-ui --mode pipeline

# Preview without costs
codex-ai doc-ui --dry-run --verbose

# Custom AI model and output directory
codex-ai doc-ui --model claude_3_7_sonnet --output-dir ./docs
```

**Key Features:**
- 🤖 Intelligent file detection (React, Sass, Storybook)
- 🔄 Cross-type triggers (React + Storybook)
- 📍 Path-based processing 
- 🧠 Sibling detection
- ⚡ Incremental updates

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
    TOKEN_STRATEGY["PROMPT_OVERHEAD"]                      # 5K prompt
) * TOKEN_STRATEGY["SAFETY_MARGIN"]                       # 95% safety
# Result: 124,450 tokens available for git log
```

### Token Distribution
- **Context Window**: `AI_MODELS.max_tokens` (200K)
- **AI Response**: `AI_MODELS.max_output_tokens` (64K) 
- **Prompt + Metadata**: `TOKEN_STRATEGY.PROMPT_OVERHEAD` (5K)
- **Safety Margin**: `TOKEN_STRATEGY.SAFETY_MARGIN` (95%)
- **Available for Git Log**: 124,450 tokens

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
├── src/              # Source code (Python best practice)
│   ├── commands/     # CLI command implementations
│   ├── constants/    # Configuration constants
│   ├── core/         # Core business logic
│   │   ├── ai/       # AI model integration
│   │   ├── config/   # Configuration management
│   │   └── git/      # Git operations and analysis
│   └── templates/    # AI prompts and templates
│       └── prompts/  # AI prompt templates
├── tests/            # Test suite
├── docs/             # Documentation
└── pyproject.toml    # Modern Python packaging
```

## 🧪 Development

### Setup Development Environment

#### Quick Development Setup (Recommended)
```bash
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai
./dev-install.sh  # 🚀 Smart installer - auto-detects and removes conflicts
```

**Why use dev-install.sh?**
- 🔍 **Auto-detects** all locally installed editable packages
- 🧹 **Removes conflicts** automatically (like context-ai)
- ✅ **Installs cleanly** without dependency issues
- 🎯 **Verifies installation** and tests functionality

#### Manual Setup (Alternative)
```bash
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai
pip install -e ".[all]"  # Install with all optional dependencies for development
```

**Note**: If you encounter import errors or conflicts with other local packages, use `./dev-install.sh` instead.

### Local Development & Testing
📖 **[Local Development Guide](docs/local-developing.md)** - Complete guide for:
- Installing in development mode (`pip install -e .`)
- Verifying installation type (local vs PyPI)
- Development workflow and testing commands
- Troubleshooting common issues

### Run Tests
```bash
# Run all tests with our custom test runner
python tests/run_all.py

# Run specific category
python tests/run_all.py --category commands

# Run with verbose output
python tests/run_all.py --verbose

# Run ui-lib integration tests
python tests/run_all.py --ui-lib-integration

# Alternative: Use pytest (if available)
pytest
```

### Code Quality (TODO: Implementar)
```bash
# TODO: Implementar ferramentas de qualidade de código modernas
# Status: Configurações prontas no pyproject.toml, aguardando implementação

# 🚀 RUFF - Ferramenta all-in-one (substitui black + isort + flake8)
# pip install ruff
# ruff format .    # Auto-formatação
# ruff check .     # Linting  
# ruff check --fix .  # Auto-fix imports

# 🔍 MYPY - Verificador de tipos (padrão da indústria)  
# pip install mypy
# mypy .

# ⚡ Comando completo (quando implementado)
# ruff format . && ruff check --fix . && mypy .

# 👀 Modo watch (futuro):
# pip install watchdog
# watchmedo shell-command --patterns="*.py" --recursive --command="ruff format . && ruff check --fix . && mypy ." .
```

**Status das Ferramentas:**
- **🔧 Configurações**: ✅ Prontas no pyproject.toml (placeholder)
- **📦 Instalação**: ⏳ TODO - pip install ruff mypy  
- **🎯 Implementação**: ⏳ TODO - Configurar e testar
- **🤖 Automação**: ⏳ TODO - CI/CD integration
- **📈 Vantagens do ruff**: Usado por Pydantic, FastAPI, Pandas - ferramenta emergente de 2024

### Future Migration to Poetry (TODO: Avaliar)
📖 **[Poetry Migration Guide](docs/poetry-migration.md)** - Guia completo para migração de setuptools para Poetry, incluindo comparações detalhadas, cronograma de migração e benefícios para o developer experience moderno.

### Package Publishing Guide
📦 **[Python Publishing Guide](docs/publishing-guide.md)** - Documentação completa sobre publicação de pacotes Python no PyPI, comparando com npm para desenvolvedores Node.js. Inclui workflows, CI/CD, troubleshooting e casos práticos.

## 📋 Examples

### Complete Workflow Example
```bash
# 1. Setup
pip install codex-ai
codex-ai config --api-key sk-ant-your-key-here

# 2. Generate changelog for release
codex-ai changelog --since "v1.0.0" --output CHANGELOG.md

# 3. Generate documentation
codex-ai doc-ui --output-dir ./docs

# 4. View configuration
codex-ai config --list
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
