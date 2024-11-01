#!/bin/bash

# This script creates a JSON file containing the complete project directory structure,
# excluding certain folders like node_modules, dist, etc.

# Check if required arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_path> <output_file>"
    exit 1
fi

START_PATH="$1"
OUTPUT_FILE="$2"

# Convert relative path to absolute path
START_PATH=$(realpath "$START_PATH")

# Check if start_path is a valid directory
if [ ! -d "$START_PATH" ]; then
    echo "Error: $START_PATH is not a valid directory."
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

# List of folders to exclude
EXCLUDE_FOLDERS="dist|node_modules|venv|examples|.git|.vscode|.tmp|.github|.aider.tags.cache.v3"

# Function to create JSON structure
generate_structure() {
    local dir="$1"
    local first=true
    echo "{"
    
    # Get all directories first
    while IFS= read -r d; do
        [ -z "$d" ] && continue
        local basename=$(basename "$d")
        if ! echo "$basename" | grep -qE "^($EXCLUDE_FOLDERS)$"; then
            $first || echo ","
            first=false
            printf '"%s": ' "$basename"
            generate_structure "$d"
        fi
    done < <(find "$dir" -maxdepth 1 -type d ! -path "$dir" ! -path "*/\.*" | sort)
    
    # Get all files
    local files=()
    while IFS= read -r f; do
        [ -n "$f" ] && files+=("$(basename "$f")")
    done < <(find "$dir" -maxdepth 1 -type f ! -path "*/\.*" | sort)
    
    if [ ${#files[@]} -gt 0 ]; then
        $first || echo ","
        printf '"files": ['
        local first_file=true
        for f in "${files[@]}"; do
            $first_file || printf ","
            first_file=false
            printf '"%s"' "$f"
        done
        echo "]"
    fi
    
    echo "}"
}

# Create directory for output file if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Generate structure and format with jq
generate_structure "$START_PATH" | jq '.' > "$OUTPUT_FILE"

echo "Project tree structure saved to $OUTPUT_FILE"
