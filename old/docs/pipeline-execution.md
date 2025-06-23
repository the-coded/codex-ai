# 🔄 Pipeline Execution Guide

This guide covers how to integrate Codex into CI/CD pipelines for automated documentation generation and project analysis.

## 🎯 Overview

Codex is designed to be cloned as `.codex/` within your project during pipeline execution, providing AI-powered analysis and documentation generation capabilities.

## 🚀 Quick Setup

### Basic Pipeline Integration
```yaml
- name: Clone Codex
  env:
    PAT: ${{ secrets.GH_PAT }}
  run: |
    git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
    source .codex/bin/start.sh

- name: Execute Analysis
  env:
    PYTHONPATH: .codex
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: python -m pkg.changelog  # or other module
```

## 📋 Complete Examples

### Automatic Changelog Generation

```yaml
name: changelog

on:
  release:
    types: [created]

permissions:
  contents: write

jobs:
  generate-changelog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history and tags

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Clone Codex
        env:
          PAT: ${{ secrets.GH_PAT }}
        run: |
          git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
          source .codex/bin/start.sh

      - name: Generate changelog
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          PYTHONPATH: .codex
        run: python -m pkg.changelog

      - name: Update release with changelog
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          release_id=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
            "https://api.github.com/repos/${{ github.repository }}/releases/tags/${{ github.event.release.tag_name }}" \
            | jq -r .id)
          
          body=$(cat .tmp/changelog.md)
          
          curl -X PATCH \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${{ github.repository }}/releases/$release_id" \
            -d "{\"body\": $(echo "$body" | jq -Rs .)}"

      - name: Upload changelog artifacts
        uses: actions/upload-artifact@v4
        with:
          name: changelog-artifacts
          path: |
            .tmp/
            .aider.chat.history.md
          include-hidden-files: true
```

### Project Analysis Pipeline

```yaml
name: project-analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Clone Codex
        env:
          PAT: ${{ secrets.GH_PAT }}
        run: |
          git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
          source .codex/bin/start.sh

      - name: Generate project analysis
        run: |
          cd .codex
          ./bin/tree_generate_all.sh

      - name: Upload analysis artifacts
        uses: actions/upload-artifact@v4
        with:
          name: project-analysis
          path: .codex/.tmp/
```

### Documentation Generation Pipeline

```yaml
name: docs-generation

on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM
  workflow_dispatch:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Clone Codex
        env:
          PAT: ${{ secrets.GH_PAT }}
        run: |
          git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
          source .codex/bin/start.sh

      - name: Generate documentation
        env:
          PYTHONPATH: .codex
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Generate project structure
          .codex/bin/tree_generate_all.sh
          
          # Process documentation templates
          python -c "
          from utils.load_template import load_template
          import json
          
          with open('.codex/.tmp/tree_project.json', 'r') as f:
              data = json.load(f)
          
          result = load_template('docs/template.md', 
              project_name='${{ github.repository }}',
              file_count=len(data)
          )
          
          with open('generated-docs.md', 'w') as f:
              f.write(result)
          "

      - name: Commit generated docs
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add generated-docs.md
          git diff --staged --quiet || git commit -m "docs: auto-generated documentation"
          git push
```

## 🔑 Required Configuration

### GitHub Secrets

#### Required Secrets
- **`GH_PAT`**: Personal Access Token with `repo` scope to clone Codex
  ```
  Settings → Secrets and variables → Actions → New repository secret
  Name: GH_PAT
  Value: ghp_xxxxxxxxxxxxxxxxxxxx
  ```

- **`ANTHROPIC_API_KEY`**: Anthropic API Key for AI integration
  ```
  Settings → Secrets and variables → Actions → New repository secret
  Name: ANTHROPIC_API_KEY
  Value: sk-ant-xxxxxxxxxxxxxxxxxxxx
  ```

#### Automatic Secrets
- **`GITHUB_TOKEN`**: Automatically provided by GitHub Actions (no setup needed)

### Environment Variables

#### Required Variables
```yaml
env:
  PYTHONPATH: .codex                                    # Allows importing Codex modules
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }} # For AI functionalities
```

#### Optional Variables
```yaml
env:
  CODEX_DEBUG: "true"          # Enable debug mode
  CODEX_OUTPUT_DIR: ".tmp"     # Custom output directory
  CODEX_LOG_LEVEL: "INFO"      # Logging level
```

## 🛠️ Pipeline Commands

### Analysis Commands
```bash
# Complete project analysis
.codex/bin/tree_generate_all.sh

# Specific analysis
.codex/bin/tree_project.sh . .codex/.tmp/project.json
.codex/bin/tree_git_changes.sh
.codex/bin/git_log_detailed.sh
```

### Python Module Execution
```bash
# Set PYTHONPATH first
export PYTHONPATH=.codex

# Execute modules
python -m pkg.changelog
python -m utils.get_base_path
python -m utils.load_json
```

### Utility Usage
```bash
# From within .codex directory
cd .codex
python -m utils.get_base_path    # Returns "." (project root context)
python shared/require_aider-chat.py
```

## 📊 Pipeline Outputs

### Generated Files Location
All outputs are generated in `.codex/.tmp/`:

```
.codex/.tmp/
├── tree_project.json          # Complete project structure
├── tree_git_changed.json      # Changed files
├── tree_git_siblings.json     # Related files
├── git_log_detailed.txt       # Detailed Git log
├── changelog.md               # Generated changelog (if using pkg.changelog)
└── ...                        # Other module outputs
```

### Artifact Upload Examples
```yaml
- name: Upload analysis results
  uses: actions/upload-artifact@v4
  with:
    name: codex-analysis
    path: |
      .codex/.tmp/
      .aider.chat.history.md
    include-hidden-files: true
    retention-days: 30
```

## 🔧 Troubleshooting

### Common Pipeline Issues

#### Permission Denied
```yaml
# Issue: PAT doesn't have repo permissions
# Solution: Verify PAT has 'repo' scope
- name: Clone Codex
  env:
    PAT: ${{ secrets.GH_PAT }}
  run: |
    # Test PAT permissions first
    curl -H "Authorization: token $PAT" https://api.github.com/user
    git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
```

#### Module Not Found
```yaml
# Issue: Python can't find Codex modules
# Solution: Set PYTHONPATH correctly
- name: Execute Codex module
  env:
    PYTHONPATH: .codex  # Must point to cloned directory
  run: python -m pkg.changelog
```

#### Python Environment Issues
```yaml
# Issue: Python/pip not available
# Solution: Use setup-python action
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
    cache: 'pip'  # Optional: cache pip dependencies
```

#### Virtual Environment Issues
```yaml
# Issue: Virtual environment creation fails
# Solution: Ensure proper permissions and Python setup
- name: Setup Codex environment
  run: |
    cd .codex
    # Check Python availability
    python3 --version || python --version
    # Setup with verbose output
    bash -x bin/start.sh
```

### Debug Mode

#### Enable Debug Output
```yaml
- name: Debug Codex execution
  env:
    CODEX_DEBUG: "true"
    PYTHONPATH: .codex
  run: |
    # Run with debug information
    set -x
    cd .codex
    ./bin/tree_generate_all.sh
    
    # Check outputs
    ls -la .tmp/
    
    # Verify Python modules
    python -c "import sys; print('Python path:', sys.path)"
    python -c "from utils.get_base_path import get_base_path; print('Base path:', get_base_path())"
```

#### Log Analysis
```yaml
- name: Analyze logs
  if: failure()
  run: |
    # Check for errors in outputs
    find .codex/.tmp/ -name "*.txt" -exec grep -l "error\|Error\|ERROR" {} \;
    find .codex/.tmp/ -name "*.json" -exec jq 'select(.error)' {} \;
    
    # Check file sizes (empty files indicate issues)
    ls -la .codex/.tmp/
```

## 💡 Best Practices

### Performance Optimization
```yaml
# Cache Python dependencies
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
    cache: 'pip'

# Cache Codex clone (if repository doesn't change often)
- name: Cache Codex
  uses: actions/cache@v3
  with:
    path: .codex
    key: codex-${{ hashFiles('.codex/**') }}
```

### Security
```yaml
# Use specific PAT with minimal permissions
# Rotate secrets regularly
# Don't log sensitive information
- name: Execute with security
  env:
    PAT: ${{ secrets.GH_PAT }}
  run: |
    # Don't echo sensitive variables
    set +x
    git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex
    set -x
```

### Error Handling
```yaml
- name: Execute with error handling
  run: |
    set -e  # Exit on error
    
    # Clone with retry
    for i in {1..3}; do
      git clone https://x-access-token:${PAT}@github.com/the-coded/codex-ai.git .codex && break
      echo "Clone attempt $i failed, retrying..."
      sleep 5
    done
    
    # Verify clone success
    test -d .codex || exit 1
    
    # Execute with error checking
    cd .codex
    source bin/start.sh
    ./bin/tree_generate_all.sh
    
    # Verify outputs
    test -f .tmp/tree_project.json || exit 1
```

## 🔗 Related Documentation

- [📖 Scripts Documentation](../bin/README.md) - Detailed bash scripts reference
- [📖 Utilities Documentation](../utils/README.md) - Python utilities reference
- [📖 Shared Scripts Documentation](../shared/README.md) - Shared scripts reference
- [💻 Local Development Guide](local-development.md) - Local development setup
