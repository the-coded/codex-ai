# 📝 Changelog Generator

This module runs aider to generate formatted changelogs. The changelog command can be used in two modes:
- **🔧 dev**: Running directly from the codex repository
- **🚀 prod**: Running from .codex/pkg when codex is cloned as .codex in another repository

## 📋 Usage Patterns

### 💻 Command-line Usage (via __main__.py)

Development mode (in codex repository):
```bash
# Generate regular git logs (default)
python -m pkg.changelog --mode dev

# Generate release logs
python -m pkg.changelog --mode dev --type release
```

Production mode (in repository with .codex):
```bash
# Add .codex to PYTHONPATH first
PYTHONPATH=/path/to/project/.codex python -m pkg.changelog
# or
export PYTHONPATH=/path/to/project/.codex

# Generate regular git logs (default)
python -m pkg.changelog
# Generate release logs
python -m pkg.changelog --type release
```

### 🔧 Programmatic Usage (via __init__.py)

Development mode (in codex repository):
```python
from pkg.changelog import run

# Generate regular git logs (default)
run(mode="dev")

# Generate release logs
run(mode="dev", type="release")
```

Production mode (in repository with .codex):
```python
from .codex.pkg.changelog import run

# Generate regular git logs (default)
run()  # equivalent to run(mode="prod", type="log")

# Generate release logs
run(type="release")  # equivalent to run(mode="prod", type="release")
```

## 🚀 Complete Workflows

### 🔧 Development Mode

When working directly in the codex repository:

```bash
# 1. Activate virtual environment (only needed once)
source bin/start.sh --mode dev

# 2. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 3. Add project root to PYTHONPATH
export PYTHONPATH=$PWD

# 4. Generate changelog (choose one):
python -m pkg.changelog --mode dev  # Command-line usage (regular logs)
python -m pkg.changelog --mode dev --type release  # Command-line usage (release logs)
# or
python3 -c "from pkg.changelog import run; run(mode='dev')"  # Programmatic usage (regular logs)
python3 -c "from pkg.changelog import run; run(mode='dev', type='release')"  # Programmatic usage (release logs)
```

### 🚀 Production Mode

When using codex as a tool in another repository:

```bash
# 1. Clone codex as .codex
git clone https://github.com/your-org/codex.git .codex

# 2. Activate virtual environment (only needed once)
source .codex/bin/start.sh

# 3. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 4. Add .codex to PYTHONPATH
export PYTHONPATH=$PWD/.codex

# 5. Generate changelog (choose one):
python -m pkg.changelog  # Command-line usage (regular logs)
python -m pkg.changelog --type release  # Command-line usage (release logs)
# or
python3 -c "from pkg.changelog import run; run()"  # Programmatic usage (regular logs)
python3 -c "from pkg.changelog import run; run(type='release')"  # Programmatic usage (release logs)

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

### 🔧 Development Mode (in codex repository)
```
pkg/
└── changelog/
    ├── __init__.py          # Handles programmatic usage exports
    ├── __main__.py         # Handles command-line interface
    ├── run.py              # Core implementation
    ├── template.md         # Template for changelog generation
    └── prompt.md          # Instructions for changelog generation

utils/
├── get_base_path.py       # Path handling for dev/prod modes
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
3. 🎯 Choose between command-line usage (via __main__.py) or programmatic usage (via __init__.py)
4. 🚀 Default mode is "prod" when no mode is specified
5. 📋 Default type is "log" when no type is specified
6. 🔄 Git logs are generated automatically based on type:
   - type="log": Regular git logs
   - type="release": Release logs
7. 🔍 Large logs are automatically simplified if they exceed 185,000 tokens
8. 🛠️ Core implementation is in run.py, using shared utilities from utils/
9. 📦 Production mode requires:
   - codex to be cloned as .codex in the target repository
   - .codex to be added to PYTHONPATH
