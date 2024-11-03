# 📝 Changelog Generator

This module runs aider to generate formatted changelogs. The changelog command can be used in two modes:
- **🔧 dev**: Running directly from the codex repository
- **🚀 prod**: Running from .codex/pkg when codex is cloned as .codex in another repository

## 📋 Usage Patterns

### 💻 Command-line Usage (via __main__.py)

Development mode (in codex repository):
```bash
python -m pkg.changelog --mode dev
```

Production mode (in repository with .codex):
```bash
# Add .codex to PYTHONPATH first
PYTHONPATH=/path/to/project/.codex python -m pkg.changelog
# or
export PYTHONPATH=/path/to/project/.codex
python -m pkg.changelog
```

### 🔧 Programmatic Usage (via __init__.py)

Development mode (in codex repository):
```python
from pkg.changelog import run
run(mode="dev")
```

Production mode (in repository with .codex):
```python
import sys
sys.path.append('/path/to/project/.codex')  # Add .codex to Python path
from pkg.changelog import run
run()
```

## 🚀 Complete Workflows

### 🔧 Development Mode

When working directly in the codex repository:

```bash
# 1. Activate virtual environment (only needed once)
source bin/start.sh --mode dev

# 2. Generate git logs (needed before each changelog generation)
./bin/git_log_detailed.sh
./bin/git_log_simple.sh

# 3. Install aider-chat (only needed once)
python shared/require_aider-chat.py

# 4. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 5. Generate changelog (choose one):
python -m pkg.changelog --mode dev  # Command-line usage
# or
python3 -c "from pkg.changelog import run; run(mode='dev')"  # Programmatic usage
```

### 🚀 Production Mode

When using codex as a tool in another repository:

```bash
# 1. Clone codex as .codex
git clone https://github.com/your-org/codex.git .codex

# 2. Activate virtual environment (only needed once)
source .codex/bin/start.sh

# 3. Generate git logs (needed before each changelog generation)
./.codex/bin/git_log_detailed.sh
./.codex/bin/git_log_simple.sh

# 4. Install aider-chat (only needed once)
python .codex/shared/require_aider-chat.py

# 5. Set your Anthropic API key (required for changelog generation)
export ANTHROPIC_API_KEY=your_api_key_here

# 6. Add .codex to PYTHONPATH
export PYTHONPATH=$PWD/.codex

# 7. Generate changelog (choose one):
python -m pkg.changelog  # Command-line usage
# or
python3 -c "from pkg.changelog import run; run()"  # Programmatic usage

# 8. Optional: Clean up when done
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
  .tmp/commit_full_log.txt
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
└── file_tree/
    └── gen_all_trees.py   # Generates file trees used by changelog
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

1. ✨ Virtual environment activation and aider-chat installation only need to be done once
2. 🔄 Git logs must be generated before each changelog generation
3. 🔑 The ANTHROPIC_API_KEY must be set before running pkg.changelog
4. 🎯 Choose between command-line usage (via __main__.py) or programmatic usage (via __init__.py)
5. 🚀 Default mode is "prod" when no mode is specified
6. 🛠️ Core implementation is in run.py, using shared utilities from utils/get_base_path.py
7. 🔧 Path handling for dev/prod modes is centralized in utils/get_base_path.py
8. 📦 Production mode requires:
   - codex to be cloned as .codex in the target repository
   - .codex to be added to PYTHONPATH
