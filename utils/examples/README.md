# Utility Examples

This directory contains examples demonstrating how to use various utility functions from the project.

## Available Examples

### [get_base_path](get_base_path/README.md)
Examples showing how to handle paths in development and production modes:
- Path resolution in different environments
- Integration with file operations
- Best practices for path handling

### [load_json](load_json/README.md)
Examples demonstrating JSON file handling:
- Basic JSON loading
- Error handling
- Project structure processing
- Configuration management

### [load_template](load_template/README.md)
Examples showing template processing:
- Variable substitution
- Email templates
- Project templates
- Error handling

## Running Examples

Each utility has its own example directory with:
- README.md with detailed documentation
- Python scripts demonstrating usage
- Example files where applicable

To run an example:
```bash
# From the project root
python utils/examples/<utility_name>/<example_script>.py
```

## Directory Structure

```
utils/examples/
├── README.md                   # This file
├── get_base_path/             # get_base_path examples
│   ├── README.md
│   └── path_usage.py
├── load_json/                 # load_json examples
│   ├── README.md
│   └── json_usage.py
└── load_template/             # load_template examples
    ├── README.md
    ├── template_example.txt
    └── template_usage.py
```

## Best Practices

1. Check each utility's README for specific usage guidelines
2. Review error handling in the examples
3. Understand the development vs production modes
4. Follow the patterns demonstrated in the examples
5. Use the appropriate utility for each use case

## Contributing

When adding new examples:
1. Create a dedicated directory for the utility
2. Include a comprehensive README.md
3. Provide working example scripts
4. Include sample files if needed
5. Update this main README.md
