# Utilities

This directory contains utility functions used throughout the project. These utilities provide common functionality for path handling, JSON processing, and template management.

## Available Utilities

### get_base_path
Path resolution utility that handles different execution contexts (development/production).
```python
from utils.get_base_path import get_base_path

base = get_base_path("dev")  # Returns "."
base = get_base_path("prod")  # Returns ".nexus"
```

### load_json
JSON file loading utility with error handling.
```python
from utils.load_json import load_json

data = load_json('.tmp/tree_project.json')
```

### load_template
Template processing utility with variable substitution.
```python
from utils.load_template import load_template

result = load_template('template.txt',
    name="John",
    title="Developer"
)
```

## Technical Documentation

For detailed technical documentation, implementation examples, and best practices, see:
[Utility Examples and Documentation](examples/README.md)

## Directory Structure

```
utils/
├── README.md           # This file
├── get_base_path.py   # Path resolution utility
├── load_json.py       # JSON loading utility
├── load_template.py   # Template processing utility
└── examples/          # Detailed examples and documentation
```

## Usage

These utilities are designed to be imported and used throughout the project. They provide consistent interfaces for common operations and handle error cases appropriately.

For specific implementation details, error handling, and advanced usage examples, please refer to the [examples documentation](examples/README.md).
