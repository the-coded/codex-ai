# file_tree Module

This module contains scripts for generating and managing file tree structures for the project.

## Scripts

### gen_all_trees.py

Generates JSON structure files for different project directories and Git changes.

**Usage:**
```
python .nexus/src/general/file_tree/gen_all_trees.py
```

**Example:**
```
python .nexus/src/general/file_tree/gen_all_trees.py
```

### gen_dir_tree.py

Generates a JSON file containing the directory and file structure of a specified directory.

**Usage:**
```
python .nexus/src/general/file_tree/gen_dir_tree.py <start_path> <output_file>
```

**Example:**
```
python .nexus/src/general/file_tree/gen_dir_tree.py ./ .tmp/project_structure.json
```

### gen_git_tree.py

Creates JSON files containing the structure of files changed and removed in the last Git commit.

**Usage:**
```
python .nexus/src/general/file_tree/gen_git_tree.py [output_changed_files] [output_removed_files] [output_diff]
```

**Examples:**
```
# Using default output paths
python .nexus/src/general/file_tree/gen_git_tree.py

# Specifying custom output paths
python .nexus/src/general/file_tree/gen_git_tree.py .tmp/changed.json .tmp/removed.json .tmp/diff.json
```

### gen_related_tree.py

Generates a JSON file containing the structure of related files based on the last Git commit changes.

**Usage:**
```
python .nexus/src/general/file_tree/gen_related_tree.py
```

**Example:**
```
python .nexus/src/general/file_tree/gen_related_tree.py
```

Note: This script reads from .tmp/git-changed_structure.json and .tmp/project_structure.json, and saves the output to .tmp/git-related_structure.json.

For more detailed information about each script, please refer to their respective files.
