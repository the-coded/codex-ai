#!/bin/bash

mkdir -p .tmp

# Create or truncate the output file
> .tmp/git_release_detailed.txt

# Function to output to both console and file
output() {
    echo "$1" | tee -a .tmp/git_release_detailed.txt
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

# Function to log commit details
log_commit() {
    local commit_hash=$1
    output ""
    output "Commit: $commit_hash"
    git show --pretty=format:"Author: %an%nDate: %ad%nMessage: %s%n%nBody:%n%b" --patch $commit_hash | tee -a .tmp/git_release_detailed.txt
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
output "Changes found:"
for commit in $(git rev-list --reverse $previous_tag..$current_tag); do
    # Check if the commit is a merge commit
    if [ $(git rev-list --parents -n 1 $commit | wc -w) -gt 2 ]; then
        output "Merge Commit: $commit"
        log_commit $commit

        # Get the parents of the merge commit
        parents=($(git rev-list --parents -n 1 $commit | cut -d' ' -f2-))
        
        # Find the non-main parent (assuming the first parent is from the main branch)
        non_main_parent=${parents[1]}

        output "Commits introduced by this merge:"
        
        # Log all commits from the non-main parent up to the merge commit
        for merge_commit in $(git rev-list --reverse $non_main_parent..$commit); do
            log_commit $merge_commit
        done
    else
        log_commit $commit
    fi
done

# Show the full diff between releases
output "Full diff between releases:"
if ! git diff $previous_tag..$current_tag | tee -a .tmp/git_release_detailed.txt; then
    output "Error generating diff between $previous_tag and $current_tag"
fi

output "========================================="

# If the file is empty or only contains the separator, remove it
if [ ! -s .tmp/git_release_detailed.txt ] || [ "$(cat .tmp/git_release_detailed.txt)" = "=========================================" ]; then
    rm .tmp/git_release_detailed.txt
fi
