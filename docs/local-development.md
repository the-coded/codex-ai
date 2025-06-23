# 💻 Local Development Guide

This guide covers how to use Codex locally for development, testing, and manual project analysis.

## 🚀 Initial Setup

### 1. Clone Codex
```bash
# Clone as sibling repository to your projects
git clone https://github.com/the-coded/codex-ai.git
cd codex-ai
```

### 2. Setup Python Environment
```bash
# Creates and activates virtual environment automatically
source bin/start.sh
```

The `start.sh` script will:
- ✅ Check if already in a virtual environment
- 📦 Create `venv/` directory if it doesn't exist
- 🚀 Activate the virtual environment
- 💡 Provide deactivation instructions

### 3. Install Dependencies (if needed)
```bash
# Install aider-chat if required
python shared/require_aider-chat.py
```

### 4. Test Installation
```bash
# Run complete analysis to test everything works
./bin/tree_generate_all.sh

# Check generated files
ls .tmp/
```

## 🔍 Analyzing Projects

### Complete Project Analysis
```bash
# Generates all analysis files at once
./bin/tree_generate_all.sh
```

This runs the following scripts in order:
1. `tree_project.sh` - Complete project structure
2. `tree_git_changes.sh` - Git changes analysis
3. `tree_git_siblings.sh` - Related files analysis

### Specific Project Analysis
```bash
# Analyze a specific project (sibling directory)
./bin/tree_project.sh ../my-project .tmp/my-project.json

# Analyze current project structure
./bin/tree_project.sh . .tmp/current-project.json
```

### Git Analysis
```bash
# Detailed log of last commit
./bin/git_log_detailed.sh
cat .tmp/git_log_detailed.txt

# Simplified log (useful for large commits)
./bin/git_log_simple.sh
cat .tmp/git_log_simple.txt

# Analyze what files changed
./bin/tree_git_changes.sh
cat .tmp/tree_git_changed.json

# Find files related to changes (same directories)
./bin/tree_git_siblings.sh
cat .tmp/tree_git_siblings.json
```

## 🔧 Using Python Utilities

### Command Line Usage
```bash
# Execute utility modules directly
python -m utils.get_base_path
python -m utils.load_json
python -m utils.load_template
```

### Programmatic Usage
```bash
# Use utilities in Python scripts
python -c "
from utils.get_base_path import get_base_path
from utils.load_json import load_json
from utils.load_template import load_template

# Get base path (returns '.codex' if in another project)
base = get_base_path()
print(f'Base path: {base}')

# Load JSON data
data = load_json('.tmp/tree_project.json')
print(f'Project has {len(data)} items')

# Process template
result = load_template('template.md', project_name='MyProject')
print(result)
"
```

## 📊 Generated Outputs

All analysis files are saved in `.tmp/` directory:

### Project Structure Files
- **`tree_project.json`** - Complete project structure in JSON format
- **`tree_git_all.json`** - All Git changes combined
- **`tree_git_changed.json`** - Only changed files
- **`tree_git_removed.json`** - Only removed files
- **`tree_git_siblings.json`** - Files in same directories as changed files

### Git Log Files
- **`git_log_detailed.txt`** - Detailed commit information with patches
- **`git_log_simple.txt`** - Simplified commit information

## 🤖 AI Integration Examples

### Prepare Data for AI Analysis
```bash
# Generate all structured data
./bin/tree_generate_all.sh

# Use in AI prompts
echo "Analyze this project structure:"
cat .tmp/tree_project.json

echo "Recent changes:"
cat .tmp/tree_git_changed.json
```

### Template Processing
```bash
# Process documentation templates with project data
python -c "
from utils.load_template import load_template
import json

# Load project data
with open('.tmp/tree_project.json', 'r') as f:
    project_data = json.load(f)

# Process template with data
result = load_template('docs/template.md', 
    project_name='MyProject',
    file_count=len(project_data),
    last_update='2024-01-01'
)
print(result)
"
```

## 🛠️ Development Workflow

### Typical Development Session
```bash
# 1. Setup environment
cd codex-ai
source bin/start.sh

# 2. Analyze target project
./bin/tree_project.sh ../target-project .tmp/analysis.json

# 3. Check recent changes
./bin/git_log_detailed.sh

# 4. Generate complete analysis
./bin/tree_generate_all.sh

# 5. Use data for documentation/AI
cat .tmp/tree_project.json | jq '.[0:5]'  # Preview first 5 items
```

### Testing New Features
```bash
# Test individual scripts
./bin/tree_project.sh . .tmp/test.json
./bin/git_log_simple.sh

# Test utilities
python -m utils.get_base_path
python shared/require_aider-chat.py

# Verify outputs
ls -la .tmp/
```

## 🔧 Troubleshooting

### Common Issues

#### Permission Denied on Scripts
```bash
# Fix script permissions
chmod +x bin/*.sh
```

#### Python Not Found
```bash
# Check Python installation
python3 --version
# or
python --version

# Install Python 3.x if needed (macOS)
brew install python3
```

#### Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf venv/
source bin/start.sh
```

#### Missing Dependencies
```bash
# Install required dependencies
python shared/require_aider-chat.py

# Or manually install
pip install aider-chat==0.60.0
```

### Debug Mode
```bash
# Run scripts with verbose output
bash -x ./bin/tree_project.sh . .tmp/debug.json

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify utilities can be imported
python -c "from utils.get_base_path import get_base_path; print('OK')"
```

### Log Analysis
```bash
# Check for errors in generated files
grep -i error .tmp/*.txt
grep -i error .tmp/*.json

# Verify file sizes (empty files indicate issues)
ls -la .tmp/
```

## 💡 Tips and Best Practices

### Performance
- Use `tree_generate_all.sh` for complete analysis
- Use specific scripts for targeted analysis
- Clean `.tmp/` directory periodically: `rm -rf .tmp/*`

### Project Analysis
- Run analysis from project root for best results
- Use relative paths when analyzing sibling projects
- Check `.tmp/` outputs before using in AI prompts

### Development
- Always activate virtual environment: `source bin/start.sh`
- Test changes with small projects first
- Keep utilities focused and reusable

### AI Integration
- Combine multiple `.tmp/*.json` files for comprehensive analysis
- Use `jq` for JSON processing: `cat .tmp/tree_project.json | jq '.[] | select(.type=="file")'`
- Process large outputs in chunks for AI context limits

## 🤖 AI Integration with Aider

For AI-powered development and documentation generation, Codex integrates seamlessly with aider-chat:

```bash
# Quick start with Aider
python shared/require_aider-chat.py  # Install aider
export ANTHROPIC_API_KEY="your-key"  # Set API key
aider --model claude-3-5-sonnet-20241022  # Start aider

# Use Codex analysis with Aider
./bin/tree_generate_all.sh  # Generate analysis
aider --read .tmp/tree_project.json  # Load context
```

For complete Aider setup, configuration, and advanced workflows:
- **🤖 [Aider Integration Guide](aider-integration.md)** - Complete guide for using aider-chat with Codex

## 🔗 Related Documentation

- [📖 Scripts Documentation](../bin/README.md) - Detailed bash scripts reference
- [📖 Utilities Documentation](../utils/README.md) - Python utilities reference
- [📖 Shared Scripts Documentation](../shared/README.md) - Shared scripts reference
- [🔄 Pipeline Execution Guide](pipeline-execution.md) - CI/CD integration guide
- [🤖 Aider Integration Guide](aider-integration.md) - AI-powered development with aider-chat
