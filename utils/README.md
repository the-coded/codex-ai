# .nexus/utils

This directory contains utility functions used by various scripts in the .nexus folder.

## Files and Their Functions

### 1. create_tree.py
Creates a directory and file structure based on a list of file paths, excluding specified folders.

**Usage:**
```python
from create_tree import create_file_structure

files = ['dir1/file1.txt', 'dir1/subdir/file2.txt', 'dir2/file3.txt', 'node_modules/package.json']
exclude_folders = ['node_modules', 'dist', 'venv', 'examples']
structure = create_file_structure(files, exclude_folders)
print(structure)
```

### 2. get_commit_files.py
Retrieves the list of files changed in the last Git commit.

**Usage:**
```python
from get_commit_files import get_last_commit_files

changed_files = get_last_commit_files()
print("Files changed in the last commit:", changed_files)
```

### 3. git_changes.py
Obtains information about changes in the last Git commit, separating changed and removed files.

**Usage:**
```python
from git_changes import get_git_changes

changed_files, removed_files = get_git_changes()
print("Changed files:", changed_files)
print("Removed files:", removed_files)
```

### 4. list_files.py
Lists all files in a directory and its subdirectories.

**Usage:**
```python
from list_files import list_files

start_path = '/path/to/directory'
files = list_files(start_path)
for file in files:
    print(file)
```

### 5. load_json.py
Loads JSON files and returns their content as a dictionary.

**Usage:**
```python
from load_json import load_json

json_data = load_json('path/to/file.json')
print(json_data)
```

### 6. save_tree_to_json.py
Saves a file structure to a JSON file.

**Usage:**
```python
from save_tree_to_json import save_structure_to_json

structure = {
    'dir1': {
        'files': ['file1.txt'],
        'subdir': {
            'files': ['file2.txt']
        }
    },
    'dir2': {
        'files': ['file3.txt']
    }
}
save_structure_to_json(structure, 'output.json')
```

These utility functions are designed to be imported and used by other scripts in the .nexus directory. Each file contains more detailed documentation and usage examples in its docstring.