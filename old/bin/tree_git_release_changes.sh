#!/bin/bash

# This script creates JSON files containing:
# 1. Files changed between the current and previous Git release
# 2. Files removed between the current and previous Git release
# 3. Combined list of all changes

# Use provided paths or defaults
OUTPUT_CHANGED="${1:-.tmp/tree_release_changed.json}"
OUTPUT_REMOVED="${2:-.tmp/tree_release_removed.json}"
OUTPUT_ALL="${3:-.tmp/tree_release_all.json}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Please install jq using your package manager:"
    echo "  For macOS: brew install jq"
    echo "  For Ubuntu/Debian: sudo apt-get install jq"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Notice: Not in a git repository. Skipping release tree generation."
    exit 0
fi

# Try to get current tag
if ! current_tag=$(git describe --tags --abbrev=0 2>/dev/null); then
    echo "Notice: No tags/releases found in the repository. Skipping release tree generation."
    echo "To track release changes, create a release using:"
    echo "  git tag v1.0.0 (or desired version)"
    echo "  git push origin v1.0.0"
    exit 0
fi

# Get the first commit of the repository
first_commit=$(git rev-list --max-parents=0 HEAD)

# Try to get previous tag
if ! previous_tag=$(git describe --tags --abbrev=0 "$current_tag^" 2>/dev/null); then
    echo "Notice: This is the first release ($current_tag). Will compare with first commit."
    previous_tag=$first_commit
fi

# Function to get git changes between releases
get_git_changes() {
    local type="$1"  # can be "changed" or "removed"
    
    # Get the changes between releases
    local git_output
    git_output=$(git diff --name-status "$previous_tag..$current_tag" 2>/dev/null) || return
    
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

echo "Analyzing changes between releases: ${previous_tag} -> ${current_tag}"

# Get changed and removed files
changed_files=()
while IFS= read -r line; do
    [ -n "$line" ] && changed_files+=("$line")
done < <(get_git_changes "changed")

removed_files=()
while IFS= read -r line; do
    [ -n "$line" ] && removed_files+=("$line")
done < <(get_git_changes "removed")

# Only generate files if we have changes
if [ ${#changed_files[@]} -gt 0 ] || [ ${#removed_files[@]} -gt 0 ]; then
    # Generate and save structures
    create_structure "$OUTPUT_CHANGED" "${changed_files[@]}"
    create_structure "$OUTPUT_REMOVED" "${removed_files[@]}"
    create_structure "$OUTPUT_ALL" "${changed_files[@]}" "${removed_files[@]}"

    echo "Release changes saved to:"
    echo "  - Changed files: $OUTPUT_CHANGED"
    echo "  - Removed files: $OUTPUT_REMOVED"
    echo "  - All changes: $OUTPUT_ALL"
else
    echo "Notice: No changes found between releases. Skipping tree generation."
fi
