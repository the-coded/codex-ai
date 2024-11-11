#!/bin/bash

mkdir -p .tmp

# Function to output to both console and file
output_to_file() {
    tee -a .tmp/git_release_detailed.txt > /dev/null
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
> .tmp/git_release_detailed.txt

# Get all tags sorted by version date
all_tags=($(git tag --sort=-creatordate))

# Find the current tag's index
current_index=-1
for i in "${!all_tags[@]}"; do
    if [[ "${all_tags[$i]}" = "$current_tag" ]]; then
        current_index=$i
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
fi

# Function to log commit details
log_commit() {
    local commit_hash=$1
    echo "" | output_to_file
    echo "Commit: $commit_hash" | output_to_file
    git show --pretty=format:"Author: %an%nDate: %ad%nMessage: %s%n%nBody:%n%b" --patch $commit_hash | output_to_file
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
for commit in $(git rev-list --reverse $previous_tag..$current_tag); do
    # Check if the commit is a merge commit
    if [ $(git rev-list --parents -n 1 $commit | wc -w) -gt 2 ]; then
        echo "Merge Commit: $commit" | output_to_file
        log_commit $commit

        # Get the parents of the merge commit
        parents=($(git rev-list --parents -n 1 $commit | cut -d' ' -f2-))
        
        # Find the non-main parent (assuming the first parent is from the main branch)
        non_main_parent=${parents[1]}

        echo "Commits introduced by this merge:" | output_to_file
        
        # Log all commits from the non-main parent up to the merge commit
        for merge_commit in $(git rev-list --reverse $non_main_parent..$commit); do
            log_commit $merge_commit
        done
    else
        log_commit $commit
    fi
done

# Show the full diff between releases
info "Generating full diff..."
if ! git diff $previous_tag..$current_tag | output_to_file; then
    info "Error generating diff between $previous_tag and $current_tag"
fi

echo "=========================================" | output_to_file

# If the file is empty or only contains the separator, remove it
if [ ! -s .tmp/git_release_detailed.txt ] || [ "$(cat .tmp/git_release_detailed.txt)" = "=========================================" ]; then
    rm .tmp/git_release_detailed.txt
fi

info "✅ Release log generated successfully"
