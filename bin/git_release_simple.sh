#!/bin/bash

mkdir -p .tmp

# Function to output to file only
output_to_file() {
    tee -a .tmp/git_release_simple.txt > /dev/null
}

# Function to show info messages
info() {
    echo "$1"
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    info "Error: Not in a git repository."
    exit 1
fi

# Try to get current tag
if ! current_tag=$(git describe --tags --abbrev=0 2>/dev/null); then
    info "Warning: No tags/releases found in the repository."
    info "To create a release, use:"
    info "  git tag v1.0.0 (or desired version)"
    info "  git push origin v1.0.0"
    exit 1
fi

# Create or truncate the output file only if we have tags
> .tmp/git_release_simple.txt

# Debug: List all tags
info "Debug: Listing all tags..."
git tag -l --sort=-v:refname | while read tag; do
    info "  $tag"
done

# Get all tags sorted by version
mapfile -t all_tags < <(git tag -l --sort=-v:refname)

# Debug: Show current tag
info "Debug: Current tag is: $current_tag"

# Find the current tag's index
current_index=-1
for i in "${!all_tags[@]}"; do
    if [[ "${all_tags[$i]}" = "$current_tag" ]]; then
        current_index=$i
        info "Debug: Found current tag at index $i"
        break
    fi
done

# Try to get previous tag
if [[ $current_index -eq -1 ]]; then
    info "Error: Current tag not found in tag list"
    exit 1
elif [[ $current_index -eq $(( ${#all_tags[@]} - 1 )) ]]; then
    info "Warning: This is the first release ($current_tag). No previous release to compare."
    info "Showing all changes up to the current release..."
    # Get the first commit of the repository
    first_commit=$(git rev-list --max-parents=0 HEAD)
    previous_tag=$first_commit
else
    previous_tag="${all_tags[$((current_index + 1))]}"
    info "Debug: Previous tag is: $previous_tag"
fi

log_commit() {
    local commit_hash=$1
    local is_merge=$2
    echo "" | output_to_file
    echo "${is_merge:+Merge }Commit: $commit_hash" | output_to_file
    git show --pretty=format:"%an - %ad%n%s%n%b" --name-status $commit_hash -- . ':(exclude)yarn.lock' ':(exclude)_old' | output_to_file
    echo "" | output_to_file
    echo "-----------------------------------------" | output_to_file
}

info "Processing changes between ${previous_tag} and ${current_tag}..."

# Check if there are any commits between tags
if ! git rev-list $previous_tag..$current_tag > /dev/null 2>&1; then
    info "No changes found between $previous_tag and $current_tag"
    exit 0
fi

# Get all commits between the two tags
info "Processing commits..."
git rev-list --reverse $previous_tag..$current_tag | while read commit; do
    if [ $(git rev-list --parents -n 1 $commit | wc -w) -gt 2 ]; then
        log_commit $commit "Merge"
        
        parent1=$(git rev-parse $commit^1)
        parent2=$(git rev-parse $commit^2)
        
        echo "New commits introduced by this merge:" | output_to_file
        echo "" | output_to_file
        
        git log --pretty=format:"%H" --reverse $parent1..$commit | while read merge_commit; do
            log_commit $merge_commit
        done
    else
        log_commit $commit
    fi
done

# Show a summary of changes between releases
info "Generating changes summary..."
if ! git diff --stat $previous_tag..$current_tag -- . ':(exclude)yarn.lock' ':(exclude)_old' | output_to_file; then
    info "Error generating changes summary between $previous_tag and $current_tag"
fi

echo "=========================================" | output_to_file

# If the file is empty or only contains the separator, remove it
if [ ! -s .tmp/git_release_simple.txt ] || [ "$(cat .tmp/git_release_simple.txt)" = "=========================================" ]; then
    rm .tmp/git_release_simple.txt
fi

info "✅ Release log generated successfully"
