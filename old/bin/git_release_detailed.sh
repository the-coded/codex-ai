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

# Define files to exclude from changelog
# These are typically auto-generated or non-essential for changelog
EXCLUDE_PATHSPEC=":(exclude)yarn.lock :(exclude)package-lock.json :(exclude)pnpm-lock.yaml :(exclude)*.pyc :(exclude)__pycache__/** :(exclude).env :(exclude)dist/** :(exclude)build/** :(exclude)*.log :(exclude).DS_Store :(exclude)coverage/** :(exclude).nyc_output/** :(exclude)*.min.js :(exclude)*.min.css :(exclude)_old/**"

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

# Get all tags sorted by creation date (newest first) in a portable way
all_tags=()
while IFS= read -r tag; do
    all_tags+=("$tag")
done < <(git tag --sort=-creatordate)

# Find the current tag's index
current_index=-1
for i in "${!all_tags[@]}"; do
    if [[ "${all_tags[$i]}" = "$current_tag" ]]; then
        current_index=$i
        break
    fi
done

# Try to get previous tag or first commit
if [[ $current_index -eq -1 ]]; then
    info "Error: Current tag not found in tag list"
    exit 1
elif [[ $current_index -eq $(( ${#all_tags[@]} - 1 )) ]]; then
    info "This is the first release ($current_tag). Comparing with first commit."
    # Get the first commit of the repository
    first_commit=$(git rev-list --max-parents=0 HEAD)
    previous_tag="$first_commit^{}"  # Add ^{} to ensure we get the commit itself
else
    previous_tag="${all_tags[$((current_index + 1))]}"
fi

# Write release information header
{
    echo "CURRENT RELEASE:"
    echo "  Tag: $current_tag"
    echo "  Date: $(git log -1 --format=%ai $current_tag)"
    echo ""
    if [ "$previous_tag" != "$first_commit^{}" ]; then
        echo "PREVIOUS RELEASE:"
        echo "  Tag: $previous_tag"
        echo "  Date: $(git log -1 --format=%ai $previous_tag)"
    else
        echo "PREVIOUS RELEASE:"
        echo "  No Previous Release, this is a First Release - Including all commits from repository start"
    fi
    echo ""
    echo "-----------------------------------------"
} | output_to_file

# Function to log commit details
log_commit() {
    local commit_hash=$1
    echo "" | output_to_file
    echo "Commit: $commit_hash" | output_to_file
    git show --pretty=format:"Author: %an <%ae>%nDate: %ad%nMessage: %s%n%nBody:%n%b" --patch $commit_hash -- . $EXCLUDE_PATHSPEC | output_to_file
    echo "" | output_to_file
    echo "-----------------------------------------" | output_to_file
}

info "Processing changes between ${previous_tag} and ${current_tag}..."

# For first release, we want to include the first commit too
if [[ "$previous_tag" == "$first_commit^{}" ]]; then
    log_commit $first_commit
fi

# Get all commits between the reference points
for commit in $(git rev-list --reverse ${previous_tag}..${current_tag}); do
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
if ! git diff ${previous_tag}..${current_tag} -- . $EXCLUDE_PATHSPEC | output_to_file; then
    info "Error generating diff between $previous_tag and $current_tag"
fi

echo "=========================================" | output_to_file

# If the file is empty or only contains the separator, remove it
if [ ! -s .tmp/git_release_detailed.txt ] || [ "$(cat .tmp/git_release_detailed.txt)" = "=========================================" ]; then
    rm .tmp/git_release_detailed.txt
fi

info "✅ Release log generated successfully"
