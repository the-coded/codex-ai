
# FULL LOG

# Run our log_full.sh script
```bash
./.nexus/scripts/log_full.sh
```


### Count characters in .tmp/commit_full_log.txt
```bash
echo "Character count for commit_full_log.txt: $(wc -m < .tmp/commit_full_log.txt)"
```


# LIST OF CHANGES LOG


## Run our log_changes.sh script
```bash
./.nexus/scripts/log_changes.sh
```



### Count characters in .tmp/commit_changes_log.txt
```bash
echo "Character count for commit_changes_log.txt: $(wc -m < .tmp/commit_changes_log.txt)"
```


# AIDER


## aider
```bash
aider \
  --subtree-only \
  --no-git \
  --yes \
  --sonnet \
  --cache-prompts \
  --no-stream \
  --read .nexus/project/changelog/template.md \
  --message-file .nexus/project/changelog/prompt-instructions.md \
  .tmp/commit_full_log.txt
```


