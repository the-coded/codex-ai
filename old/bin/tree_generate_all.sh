#!/bin/bash

# This script generates all JSON tree structures:
# 1. Complete project tree
# 2. Git changes (changed, removed, and all changes)
# 3. Git release changes (changed, removed, and all changes between releases)
# 4. Sibling files of changed files

# Function to run a command and capture its output
run_command() {
    local command="$1"
    if output=$(bash -c "$command" 2>&1); then
        echo ""
        echo "Command executed successfully: $command"
        [ -n "$output" ] && echo "" && echo "$output" && echo "" && echo "----------------------------------------"
    else
        echo "Error executing command: $command"
        echo "Error: $output"
        exit 1
    fi
}

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# List of commands to generate JSON structures
commands=(
    "$SCRIPT_DIR/tree_project.sh ./ .tmp/tree_project.json"
    "$SCRIPT_DIR/tree_git_changes.sh"
    "$SCRIPT_DIR/tree_git_release_changes.sh"
    "$SCRIPT_DIR/tree_git_siblings.sh"
)

# Execute each command
for command in "${commands[@]}"; do
    run_command "$command"
done

echo ""
echo "All tree structures were generated successfully in .tmp/:"
echo "  - tree_project.json (complete project structure)"
echo "  - tree_git_changed.json (files changed in last commit)"
echo "  - tree_git_removed.json (files removed in last commit)"
echo "  - tree_git_all.json (all git changes)"
echo "  - tree_release_changed.json (files changed between releases, if releases exist)"
echo "  - tree_release_removed.json (files removed between releases, if releases exist)"
echo "  - tree_release_all.json (all release changes, if releases exist)"
echo "  - tree_git_siblings.json (sibling files of changed files)"
echo ""
