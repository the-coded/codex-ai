# 📚 Codex-AI Documentation Hub

Welcome to the comprehensive documentation for **Codex-AI** - an AI-powered development toolkit that transforms development workflows through intelligent automation. This documentation provides detailed technical information for developers, contributors, and users who want to understand the system architecture and implementation.

## 🤖 What is Codex-AI?

Codex-AI is a centralized AI-powered development toolkit that serves as the core hub of intelligent automation across development workflows. Inspired by ancient codices—volumes of knowledge meticulously compiled and preserved—Codex-AI is designed to be the modern evolution of development intelligence, bringing together AI-driven changelog generation, documentation automation, and project analysis in one organized platform.

### Key Capabilities:
- **📝 AI-Powered Changelogs**: Generate intelligent changelogs from Git history using Claude models
- **📚 Smart Documentation**: Auto-generate comprehensive documentation for React, Sass, Storybook, and generic codebases
- **📊 Project Analysis**: Deep insights into codebase structure, complexity, and development patterns
- **🔧 Flexible Configuration**: Multi-layer configuration system with environment variables, config files, and CLI options
- **🤖 Advanced AI Integration**: Leverages Claude-4, Claude-3.7, and Claude-3.5 models with intelligent fallback chains

## 🗺️ Documentation Structure

This documentation is organized into several key areas. Navigate through the folders to explore each section:

### **📁 `commands/`** - CLI Interface Documentation
The user-facing interface of Codex-AI with comprehensive command implementations:
- **changelog** - AI-generated changelogs with intelligent version detection
- **doc-ui** - Specialized documentation for React/Sass/Storybook with cross-type triggers
- **doc-gen** - Generic documentation generation for any programming language with flexible presets
- **config** - Global configuration management for API keys, models, and user preferences

All commands follow consistent architectural patterns with mode detection, file filtering, token management, and AI generation capabilities.

### **📁 `core/`** - Core Architecture Documentation
The foundational systems that power all Codex-AI functionality:

**`core/ai/`** - Advanced AI integration layer:
- Multi-tier token counting (Anthropic API → tiktoken → fallback ratios)
- Cost-optimized model selection with automatic fallback chains
- High-level AI coding assistant integration through Aider
- Template-based prompt loading system with multiple fallback strategies

**`core/git/`** - Comprehensive Git operations:
- Intelligent file change detection and mode switching
- Git history analysis with automatic range detection
- Project structure analysis and visualization
- Conventional commit parsing and categorization
- Release and tag analysis for version detection

**`core/config/`** - Configuration management:
- XDG-compliant configuration storage
- Hierarchical configuration with multiple sources (CLI → ENV → Config → Defaults)
- Secure API key handling with validation

### **📁 `constants/`** - Configuration System Documentation
Centralized configuration hub serving as the single source of truth:
- **AI constants** - Model configurations, token strategies, and Aider command templates
- **Git constants** - Command templates, conventional commit patterns, and repository analysis
- **Output constants** - Formatting standards, colors, emojis, and report templates  
- **Project constants** - Metadata loader from pyproject.toml with version compatibility

## 🛠️ Development Resources

### **📁 `development/`** - Comprehensive Development Documentation
Centralized hub for all development-related guides and resources:
- **Local Environment Setup** - Development environment configuration and troubleshooting
- **AI Token Optimization** - Advanced token management strategies and performance techniques
- **Modern Python Packaging** - Poetry migration guides and dependency management
- **Package Publishing** - Complete PyPI publishing workflow and CI/CD integration
- **Development Philosophy** - Best practices and architectural decision rationale

All development documentation has been consolidated into the `development/` folder for better organization and discoverability.

## 🏗️ Architecture Overview

Codex-AI follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Commands Layer                       │
│              (User Interface & Orchestration)               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     Core Business Logic                     │
│         AI Integration • Git Operations • Configuration     │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
┌─────────────▼─────────────┐   ┌─────────▼─────────────┐
│      Constants System     │   │    Template System    │
│   (Single Source of Truth)│   │   (AI Prompts & Configs)│ 
└───────────────────────────┘   └───────────────────────┘
```

### Design Principles:
- **Single Source of Truth**: All configurations centralized in constants module
- **Template-Based Operations**: Parameterized templates for Git and AI operations
- **Fallback Strategies**: Automatic fallback mechanisms for robust error handling
- **Configuration Hierarchy**: Clear precedence order (CLI → ENV → Config → Defaults)
- **Consistent Patterns**: All commands follow the same architectural pattern

## 🚀 Getting Started

For users new to Codex-AI:
1. Start with the main project README.md in the root directory for installation and quick start
2. Explore the `commands/` documentation for detailed CLI usage
3. Review `local-developing.md` for development setup
4. Dive into `core/` modules for architectural understanding

For contributors and advanced users:
1. Study the `core/` architecture documentation
2. Review `constants/` for configuration details
3. Explore `token-management.md` for AI optimization techniques
4. Check `_old/` for migration guides and historical context

## 💡 Key Features Highlight

### **Intelligent Token Management**
- Multi-tier token counting with automatic fallback
- Safety margins and limit validation to prevent API errors
- Dynamic model selection based on content size and cost optimization

### **Git Integration Excellence**  
- Auto-detection between local (git status) and pipeline (git diff) modes
- Intelligent range detection for changelogs with tag discovery
- Conventional commit parsing with emoji mapping

### **AI-Powered Generation**
- Advanced prompt engineering with template-based system
- Multiple Claude model support with automatic fallback chains
- Cost-effective model selection (Claude-3.5 → 3.7 → 4)

### **Cross-Language Documentation**
- React/Sass/Storybook specialized documentation with cross-type triggers
- Generic documentation generation for any programming language
- Intelligent file detection and sibling analysis

## 📈 Project Status

This documentation reflects the current stable version of Codex-AI with:
- ✅ Complete CLI interface with all core commands
- ✅ Robust AI integration with Claude model support
- ✅ Comprehensive Git operations and analysis
- ✅ Flexible configuration system
- ✅ Extensive test coverage and quality assurance

---

**Navigate through the folders above to explore detailed documentation for each component. Each section contains comprehensive guides, API references, and practical examples for working with Codex-AI.**
