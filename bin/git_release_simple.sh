#!/bin/bash

mkdir -p .tmp

# Create or truncate the output file
> .tmp/git_release_simple.txt

# Function to output to both console and file
output() {
    echo "$1" | tee -a .tmp/git_release_simple.txt
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    output "Error: Not in a git repository."
    exit 1
fi

# Try to get current tag
if ! current_tag=$(git describe --tags --abbrev=0 2>/dev/null); then
    output "Warning: No tags/releases found in the repository."
    output "To create a release, use:"
    output "  git tag v1.0.0 (or desired version)"
    output "  git push origin v1.0.0"
    exit 1
fi

# Try to get previous tag
if ! previous_tag=$(git describe --tags --abbrev=0 "$current_tag^" 2>/dev/null); then
    output "Warning: This is the first release ($current_tag). No previous release to compare."
    output "Showing all changes up to the current release:"
    # Get the first commit of the repository
    first_commit=$(git rev-list --max-parents=0 HEAD)
    previous_tag=$first_commit
fi

log_commit() {
    local commit_hash=$1
    local is_merge=$2
    output ""
    output "${is_merge:+Merge }Commit: $commit_hash"
    git show --pretty=format:"%an - %ad%n%s%n%b" --name-status $commit_hash -- . ':(exclude)yarn.lock' ':(exclude)_old' | tee -a .tmp/git_release_simple.txt
    output ""
    output "-----------------------------------------"
}

output "Comparing: ${previous_tag} -> ${current_tag}"
output ""

# Check if there are any commits between tags
if ! git rev-list $previous_tag..$current_tag > /dev/null 2>&1; then
    output "No changes found between $previous_tag and $current_tag"
    exit 0
fi

# Get all commits between the two tags
git rev-list --reverse $previous_tag..$current_tag | while read commit; do
    if [ $(git rev-list --parents -n 1 $commit | wc -w) -gt 2 ]; then
        log_commit $commit "Merge"
        
        parent1=$(git rev-parse $commit^1)
        parent2=$(git rev-parse $commit^2)
        
        output "New commits introduced by this merge:"
        output ""
        
        git log --pretty=format:"%H" --reverse $parent1..$commit | while read merge_commit; do
            log_commit $merge_commit
        done
    else
        log_commit $commit
    fi
done

# Show a summary of changes between releases
output "Summary of changes between releases:"
if ! git diff --stat $previous_tag..$current_tag -- . ':(exclude)yarn.lock' ':(exclude)_old' | tee -a .tmp/git_release_simple.txt; then
    output "Error generating changes summary between $previous_tag and $current_tag"
fi

output "========================================="

# If the file is empty or only contains the separator, remove it
if [ ! -s .tmp/git_release_simple.txt ] || [ "$(cat .tmp/git_release_simple.txt)" = "=========================================" ]; then
    rm .tmp/git_release_simple.txt
fi
