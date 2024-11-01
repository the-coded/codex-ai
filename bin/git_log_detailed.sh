#!/bin/bash

mkdir -p .tmp
last_commit_hash=$(git rev-parse HEAD)

# Function to log commit details
log_commit() {
    local commit_hash=$1
    echo ""
    echo "Commit: $commit_hash"
    git show --pretty=format:"Author: %an%nDate: %ad%nMessage: %s%n%nBody:%n%b" --patch $commit_hash
    echo ""
    echo "-----------------------------------------"
}

# Check if the commit is a merge commit
if [ $(git rev-list --parents -n 1 $last_commit_hash | wc -w) -gt 2 ]; then
    {
        echo "Merge Commit: $last_commit_hash"
        log_commit $last_commit_hash

        # Get the parents of the merge commit
        parents=($(git rev-list --parents -n 1 $last_commit_hash | cut -d' ' -f2-))
        
        # Find the non-main parent (assuming the first parent is from the main branch)
        non_main_parent=${parents[1]}

        echo "Commits introduced by this merge:"
        
        # Log all commits from the non-main parent up to the merge commit
        for commit in $(git rev-list --reverse $non_main_parent..$last_commit_hash); do
            log_commit $commit
        done
    } > .tmp/git_log_detailed.txt
else
    {
        echo "Regular Commit: $last_commit_hash"
        log_commit $last_commit_hash
    } > .tmp/git_log_detailed.txt
fi

echo "=========================================" >> .tmp/git_log_detailed.txt
