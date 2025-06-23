#!/bin/bash

# This script creates a JSON file containing all sibling files (files in the same directory)
# of files that were changed in the last Git commit.

# Input and output paths
CHANGED_FILES=".tmp/tree_git_changed.json"
PROJECT_TREE=".tmp/tree_project.json"
OUTPUT_FILE=".tmp/tree_git_siblings.json"

# Check if required files exist
if [ ! -f "$CHANGED_FILES" ] || [ ! -f "$PROJECT_TREE" ]; then
    echo "Error: Required input files not found."
    echo "Make sure both exist:"
    echo "  - $CHANGED_FILES (run tree_git_changes.sh first)"
    echo "  - $PROJECT_TREE (run tree_project.sh first)"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Please install jq using your package manager:"
    echo "  For macOS: brew install jq"
    echo "  For Ubuntu/Debian: sudo apt-get install jq"
    exit 1
fi

# Create temporary file for building the result
temp_result=$(mktemp)
echo "{}" > "$temp_result"

# Process root files if they exist in changed files
if jq -e '.files' "$CHANGED_FILES" > /dev/null 2>&1; then
    root_files=$(jq -r '.files[]?' "$PROJECT_TREE" | jq -R -s 'split("\n") | map(select(length > 0))')
    if [ "$root_files" != "[]" ]; then
        jq --argjson files "$root_files" '. + {"files": $files}' "$temp_result" > "${temp_result}.new" && mv "${temp_result}.new" "$temp_result"
    fi
fi

# Process bin directory if it exists in changed files
if jq -e '.bin' "$CHANGED_FILES" > /dev/null 2>&1; then
    bin_files=$(jq -r '.bin.files[]?' "$PROJECT_TREE" | jq -R -s 'split("\n") | map(select(length > 0))')
    if [ "$bin_files" != "[]" ]; then
        jq --argjson files "$bin_files" '. + {"bin": {"files": $files}}' "$temp_result" > "${temp_result}.new" && mv "${temp_result}.new" "$temp_result"
    fi
fi

# Process pkg/changelog if it exists in changed files
if jq -e '.pkg.changelog' "$CHANGED_FILES" > /dev/null 2>&1; then
    changelog_files=$(jq -r '.pkg.changelog.files[]?' "$PROJECT_TREE" | jq -R -s 'split("\n") | map(select(length > 0))')
    if [ "$changelog_files" != "[]" ]; then
        jq --argjson files "$changelog_files" '. + {"pkg": {"changelog": {"files": $files}}}' "$temp_result" > "${temp_result}.new" && mv "${temp_result}.new" "$temp_result"
    fi
fi

# Sort all arrays in the result and save to output file
jq 'walk(if type == "array" then sort else . end)' "$temp_result" > "$OUTPUT_FILE"

# Clean up
rm -f "$temp_result"

echo "Sibling files structure saved to $OUTPUT_FILE"
