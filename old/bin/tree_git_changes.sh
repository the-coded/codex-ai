#!/bin/bash

# This script creates JSON files containing:
# 1. Files changed in the last Git commit
# 2. Files removed in the last Git commit
# 3. Combined list of all changes

# Use provided paths or defaults
OUTPUT_CHANGED="${1:-.tmp/tree_git_changed.json}"
OUTPUT_REMOVED="${2:-.tmp/tree_git_removed.json}"
OUTPUT_ALL="${3:-.tmp/tree_git_all.json}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Please install jq using your package manager:"
    echo "  For macOS: brew install jq"
    echo "  For Ubuntu/Debian: sudo apt-get install jq"
    exit 1
fi

# Function to get git changes
get_git_changes() {
    local type="$1"  # can be "changed" or "removed"
    
    # Get the changes from the last commit
    local git_output
    git_output=$(git show --name-status --format= HEAD 2>/dev/null) || return
    
    # Process each line
    echo "$git_output" | while IFS=$'\t' read -r status filepath extra; do
        [ -z "$status" ] || [ -z "$filepath" ] && continue
        
        # For renamed files, use the last part (new path)
        if [ -n "$extra" ]; then
            if [ "$type" = "changed" ]; then
                filepath="$extra"  # Use new path for changed files
            else
                filepath="$filepath"  # Use old path for removed files
            fi
        fi
        
        if [ "$type" = "removed" ] && [ "$status" = "D" ]; then
            echo "$filepath"
        elif [ "$type" = "changed" ] && [ "$status" != "D" ]; then
            echo "$filepath"
        fi
    done
}

# Function to create directory structure from file list
create_structure() {
    local output_file="$1"
    shift
    local result="{}"
    
    # Sort and remove duplicates
    local sorted_files=()
    while IFS= read -r line; do
        [ -n "$line" ] && sorted_files+=("$line")
    done < <(printf "%s\n" "$@" | sort -u)
    
    # Create JSON array of file entries
    local entries="[]"
    for file in "${sorted_files[@]}"; do
        [ -z "$file" ] && continue
        
        # Check if file exists (except for removed files)
        if [[ "$output_file" != *"removed"* ]] && [[ "$output_file" != *"all"* ]] && [ ! -f "$file" ]; then
            continue
        fi
        
        # Create entry with path and filename
        entries=$(echo "$entries" | jq --arg file "$file" '. + [$ARGS.named.file]')
    done
    
    # Convert entries to nested structure
    echo "$entries" | jq '
        def add_to_path(obj; path; file):
            if path == [] then
                if obj.files then
                    obj * {"files": (obj.files + [file])}
                else
                    obj * {"files": [file]}
                end
            else
                obj * {
                    (path[0]): add_to_path(
                        (obj[path[0]] // {}); 
                        path[1:];
                        file
                    )
                }
            end;

        reduce .[] as $path (
            {};
            . as $root |
            if ($path | contains("/")) then
                ($path | split("/")) as $parts |
                add_to_path(
                    $root;
                    $parts[:-1];
                    $parts[-1]
                )
            else
                add_to_path($root; []; $path)
            end
        ) | walk(if type == "array" then sort else . end)
    ' > "$output_file"
}

# Create .tmp directory if it doesn't exist
mkdir -p .tmp

# Get changed and removed files
changed_files=()
while IFS= read -r line; do
    [ -n "$line" ] && changed_files+=("$line")
done < <(get_git_changes "changed")

removed_files=()
while IFS= read -r line; do
    [ -n "$line" ] && removed_files+=("$line")
done < <(get_git_changes "removed")

# Generate and save structures
create_structure "$OUTPUT_CHANGED" "${changed_files[@]}"
create_structure "$OUTPUT_REMOVED" "${removed_files[@]}"
create_structure "$OUTPUT_ALL" "${changed_files[@]}" "${removed_files[@]}"

echo "Git changes saved to:"
echo "  - Changed files: $OUTPUT_CHANGED"
echo "  - Removed files: $OUTPUT_REMOVED"
echo "  - All changes: $OUTPUT_ALL"
