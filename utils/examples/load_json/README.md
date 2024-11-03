# 📄 load_json Usage Examples

This directory contains examples demonstrating how to use the `load_json` utility.

## 📖 Overview

The `load_json` utility provides a simple way to load and validate JSON files, with proper error handling for common scenarios like missing files or invalid JSON.

## 📁 Files

- 💻 `json_usage.py`: Python script demonstrating various use cases of load_json

## 🚀 Running the Example

```bash
# From the project root
python utils/examples/load_json/json_usage.py
```

## 💡 Basic Usage

```python
from utils.load_json import load_json

# Simple JSON loading
data = load_json('config.json')
print(data['name'])

# Project structure loading
project = load_json('.tmp/tree_project.json')
if 'react' in project:
    process_react_files(project['react'])
```

## ⚠️ Error Handling

```python
try:
    data = load_json('config.json')
except FileNotFoundError:
    print("Config file not found")
except json.JSONDecodeError:
    print("Invalid JSON format")
except Exception as e:
    print(f"Error loading JSON: {e}")
```

## 🎯 Common Use Cases

### ⚙️ Loading Configuration
```python
def get_config():
    try:
        return load_json('config.json')
    except FileNotFoundError:
        return {'default': True}
```

### 📋 Processing Project Structure
```python
def process_project():
    structure = load_json('.tmp/tree_project.json')
    if 'react' in structure:
        process_react(structure['react'])
    if 'sass' in structure:
        process_sass(structure['sass'])
```

### ✅ Validating JSON Content
```python
def validate_config():
    config = load_json('config.json')
    required = ['name', 'version', 'dependencies']
    return all(key in config for key in required)
```

## ✨ Best Practices

1. 🔍 Always use try/except when loading JSON files
2. 🎯 Handle specific exceptions appropriately
3. ✅ Validate JSON structure after loading
4. 💬 Provide meaningful error messages
5. 🔄 Use default values when appropriate

## 🔄 Integration Examples

### ⚙️ With Configuration Management
```python
def load_config(env='prod'):
    try:
        return load_json(f'config.{env}.json')
    except FileNotFoundError:
        return load_json('config.default.json')
```

### 📋 With Project Processing
```python
def analyze_project():
    try:
        structure = load_json('.tmp/tree_project.json')
        components = find_components(structure)
        return generate_report(components)
    except Exception as e:
        return f"Error analyzing project: {e}"
```

### ✅ With Data Validation
```python
def is_valid_project(project_path):
    try:
        data = load_json(project_path)
        return 'react' in data or 'sass' in data
    except:
        return False
