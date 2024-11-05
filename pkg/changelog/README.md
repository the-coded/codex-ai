# 📝 Changelog Generator

This module runs aider to generate formatted changelogs. The module automatically detects:
- **🔧 Environment**: When running from project root vs another project with .codex/
- **📦 Log Type**: Release logs if available, otherwise regular logs

## 📋 Usage Patterns

### 💻 Command-line Usage (via __main__.py)

```bash
# Add project root to PYTHONPATH first
export PYTHONPATH=$PWD
# or
export PYTHONPATH=$PWD/.codex

# Generate changelog
python -m pkg.changelog
```

### 🔧 Programmatic Usage (via __init__.py)

```python
from pkg.changelog import run
run()  # Will use release logs if available, otherwise regular logs
```

## 🚀 Complete Workflows

### 🔧 Development Mode

When working directly in the project root:

```bash
# 1. Activate virtual environment (only needed once)
source bin/start.sh

# 2. Add project root to PYTHONPATH
export PYTHONPATH=$PWD

# 3. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 4. Generate changelog
python -m pkg.changelog  # Command-line usage
# or
python3 -c "from pkg.changelog import run; run()"  # Programmatic usage
```

### 🚀 Production Mode

When using as a tool in another repository:

```bash
# 1. Clone codex as .codex
git clone https://github.com/your-org/codex.git .codex

# 2. Activate virtual environment (only needed once)
source .codex/bin/start.sh

# 3. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 4. Add .codex to PYTHONPATH
export PYTHONPATH=$PWD/.codex

# 5. Generate changelog
python -m pkg.changelog  # Command-line usage
# or
python3 -c "from pkg.changelog import run; run()"  # Programmatic usage

# 6. Optional: Clean up when done
rm -rf .codex
```

## ⚙️ Command Details

The generator runs the following aider command (paths shown for production mode):

```bash
aider \
  --subtree-only \
  --no-git \
  --yes \
  --sonnet \
  --cache-prompts \
  --no-stream \
  --read .codex/pkg/changelog/template.md \
  --message-file .codex/pkg/changelog/prompt.md \
  .tmp/changelog.md
```

## 📁 Directory Structure

### 🔧 Development Mode (in project root)
```
pkg/
└── changelog/
    ├── __init__.py          # Handles programmatic usage exports
    ├── __main__.py         # Handles command-line interface
    ├── run.py              # Core implementation
    ├── template.md         # Template for changelog generation
    └── prompt.md          # Instructions for changelog generation

utils/
├── get_base_path.py       # Path handling with environment detection
└── get_token_count.py     # Token counting utility
```

### 🚀 Production Mode (in another repository)
```
your-project/
└── .codex/               # Cloned codex repository
    └── pkg/
        ├── changelog/    # Same structure as development mode
        └── utils/        # Same structure as development mode
```

## 📝 Usage Notes

1. ✨ Virtual environment activation only needs to be done once
2. 🔑 The ANTHROPIC_API_KEY must be set before running pkg.changelog
3. 🔄 Git logs are generated automatically:
   - Regular logs are always generated
   - Release logs are generated if we're in a release
   - Release logs are used if available, otherwise regular logs
4. 🔍 Large logs are automatically simplified if they exceed 185,000 tokens
5. 🛠️ Core implementation is in run.py, using shared utilities
6. 🔧 Environment is automatically detected:
   - Development: When running from project root
   - Production: When running from another project with .codex/
7. 📦 Production mode requires:
   - codex to be cloned as .codex in the target repository
   - .codex to be added to PYTHONPATH
