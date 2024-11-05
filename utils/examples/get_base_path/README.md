# 🔍 get_base_path Usage Examples

This directory contains examples demonstrating how to use the `get_base_path` utility.

## 📖 Overview

The `get_base_path` utility helps manage file paths by automatically detecting the environment:
- Returns "." when running from project root
- Returns ".codex" when running from another project with .codex/

## 📁 Files

- 💻 `path_usage.py`: Python script demonstrating various use cases of get_base_path

## 🚀 Running the Example

```bash
# From the project root
python utils/examples/get_base_path/path_usage.py
```

## 💡 Basic Usage

```python
from utils.get_base_path import get_base_path

# Environment is automatically detected
base = get_base_path()
config_path = f"{base}/config.json"  # "./config.json" or ".codex/config.json"
```

## 🎯 Common Use Cases

### ⚙️ Configuration Files
```python
def load_config():
    base = get_base_path()
    return f"{base}/config/settings.json"
```

### 📝 Template Files
```python
def get_template_path(template_name):
    base = get_base_path()
    return f"{base}/templates/{template_name}"
```

### 🖼️ Asset Files
```python
def get_asset_path(asset_name):
    base = get_base_path()
    return f"{base}/assets/{asset_name}"
```

## ✨ Best Practices

1. 🎯 Let the utility detect the environment automatically
2. 📋 Keep path construction consistent across your application
3. 🔄 Use os.path.join for cross-platform compatibility
4. 📚 Document path expectations in your functions

## ⚠️ Error Handling

The function is simple and doesn't raise exceptions, but you should:
- ✅ Validate that the resulting paths exist before using them
- 🔍 Handle file not found errors appropriately
- 🛡️ Consider implementing path existence checks in your application

## 🔄 Integration Examples

### 📂 With File Operations
```python
def read_config():
    config_path = f"{get_base_path()}/config/settings.json"
    with open(config_path, 'r') as f:
        return f.read()
```

### 📝 With Template Loading
```python
def load_template(template_name):
    template_path = f"{get_base_path()}/templates/{template_name}"
    with open(template_path, 'r') as f:
        return f.read()
```

### 🖼️ With Asset Management
```python
def get_image_url(image_name):
    base = get_base_path()
    return f"{base}/assets/images/{image_name}"
