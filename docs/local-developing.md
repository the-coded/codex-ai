# 🔨 Local Development Guide - Codex-AI

> Complete guide for developing and testing Codex-AI locally without publishing to PyPI.

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- Git
- pip

### Install in Development Mode
```bash
# Clone the repository
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai

# Install in editable mode
pip install -e .

# Verify installation
codex-ai --help
```

## 🔍 Verify Installation Type

### Check if Local or PyPI Installation
```bash
# Method 1: Using pip show
pip show codex-ai

# Local installation output:
# Location: ~/projects/codex-ai
# Editable project location: ~/projects/codex-ai

# PyPI installation output:
# Location: /usr/local/lib/python3.x/site-packages
```

```bash
# Method 2: Using pip list
pip list | grep codex-ai

# Local installation output:
# codex-ai   1.0.0   ~/projects/codex-ai

# PyPI installation output:
# codex-ai   1.0.0
```

### Quick Visual Check
```bash
# If this works from any directory, it's properly installed
cd /tmp
codex-ai --version

# If this only works from project directory, use pip install -e .
cd /path/to/codex-ai
python cli.py --version
```

## 🛠️ Development Workflow

### 1. Initial Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install project in editable mode
pip install -e .

# Initialize configuration
codex-ai init
```

### 2. Development Cycle
```bash
# 1. Make changes to the code
vim cli.py  # or any file

# 2. Test immediately (no reinstall needed!)
codex-ai --help
codex-ai init
codex-ai uidocs --help

# 3. Run tests (when available)
pytest

# 4. Check code quality
black .
isort .
mypy .
```

### 3. Testing Different Scenarios
```bash
# Test CLI interface
codex-ai --help
codex-ai --version

# Test configuration
codex-ai init
codex-ai init --force

# Test commands (when implemented)
codex-ai changelog --dry-run
codex-ai timetrack --help
codex-ai uidocs --help
codex-ai analyze --help
```

## 🧪 Testing Commands

### Basic CLI Testing
```bash
# Help system
codex-ai --help
codex-ai changelog --help
codex-ai timetrack --help
codex-ai uidocs --help
codex-ai analyze --help

# Version and info
codex-ai --version
```

### Configuration Testing
```bash
# Initialize config files
codex-ai init

# Test with different config files
codex-ai --config custom.yaml --help
codex-ai --verbose --help
```

### Environment Testing
```bash
# Test with different environment variables
CODEX_VERBOSE=true codex-ai --help
CODEX_DEFAULT_MODEL=claude_3_5_sonnet codex-ai --help
```

### Error Handling Testing
```bash
# Test missing API key (should show helpful error)
codex-ai changelog

# Test invalid commands
codex-ai invalid-command

# Test invalid arguments
codex-ai uidocs --invalid-arg
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Command Not Found
```bash
# Problem: codex-ai: command not found
# Solution: Install in editable mode
pip install -e .

# Or check if it's in PATH
which codex-ai
```

#### 2. Import Errors
```bash
# Problem: ModuleNotFoundError
# Solution: Install dependencies
pip install -r requirements.txt

# Or reinstall in editable mode
pip uninstall codex-ai
pip install -e .
```

#### 3. Configuration Issues
```bash
# Problem: Config file not found
# Solution: Initialize configuration
codex-ai init

# Or specify config path
codex-ai --config /path/to/config.yaml
```

#### 4. Permission Errors
```bash
# Problem: Permission denied
# Solution: Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -e .
```

### Debug Mode
```bash
# Enable verbose output for debugging
codex-ai --verbose <command>

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check installed packages
pip list | grep codex
```

## 📋 Best Practices

### 1. Use Virtual Environment
```bash
# Create virtual environment
python -m venv codex-dev
source codex-dev/bin/activate

# Install in development mode
pip install -e .
```

### 2. Keep Dependencies Updated
```bash
# Update requirements
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-dev.txt
```

### 3. Test Before Committing
```bash
# Run basic tests
codex-ai --help
codex-ai init

# Check code quality
black --check .
isort --check-only .
mypy .

# Run tests (when available)
pytest
```

### 4. Clean Installation Testing
```bash
# Test clean installation
pip uninstall codex-ai
pip install -e .
codex-ai --help
```

## 🔄 Switching Between Local and PyPI

### Install Local Version
```bash
# Uninstall PyPI version (if installed)
pip uninstall codex-ai

# Install local version
pip install -e .

# Verify
pip show codex-ai | grep "Editable project location"
```

### Install PyPI Version
```bash
# Uninstall local version
pip uninstall codex-ai

# Install from PyPI
pip install codex-ai

# Verify
pip show codex-ai | grep "Location"
```

## 🚀 Advanced Development

### Testing with Different Python Versions
```bash
# Using pyenv (if installed)
pyenv install 3.8.10
pyenv install 3.9.7
pyenv install 3.10.5

# Test with each version
pyenv local 3.8.10
pip install -e .
codex-ai --help

pyenv local 3.9.7
pip install -e .
codex-ai --help
```

### Building Distribution Packages
```bash
# Build wheel and source distribution
python -m build

# Check built packages
ls dist/

# Test installation from wheel
pip install dist/codex_ai-1.0.0-py3-none-any.whl
```

### Development with Docker
```bash
# Build development image
docker build -t codex-ai-dev .

# Run in container
docker run -it codex-ai-dev codex-ai --help
```

## 📚 Additional Resources

- **Main README**: [../README.md](../README.md)
- **Configuration Guide**: [Configuration section in README](../README.md#configuration)
- **Contributing**: [Contributing section in README](../README.md#contributing)
- **Issues**: [GitHub Issues](https://github.com/the-coded/codex-ai/issues)

---

**Happy Coding! 🎉**

*Last updated: 2025-01-23*
