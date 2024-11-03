# 🔍 get_base_path Usage Examples

This directory contains examples demonstrating how to use the `get_base_path` utility.

## 📖 Overview

The `get_base_path` utility helps manage file paths in different execution contexts:
- 🔧 Development mode (running directly from codex-ai)
- 🚀 Production mode (running from .nexus in another repository)

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

# Development mode
base = get_base_path("dev")  # Returns "."
config_path = f"{base}/config.json"  # "./config.json"

# Production mode
base = get_base_path("prod")  # Returns ".nexus"
config_path = f"{base}/config.json"  # ".nexus/config.json"

# Default mode (prod)
base = get_base_path()  # Returns ".nexus"
```

## 🎯 Common Use Cases

### ⚙️ Configuration Files
```python
def load_config(mode="prod"):
    base = get_base_path(mode)
    return f"{base}/config/settings.json"
```

### 📝 Template Files
```python
def get_template_path(template_name, mode="prod"):
    base = get_base_path(mode)
    return f"{base}/templates/{template_name}"
```

### 🖼️ Asset Files
```python
def get_asset_path(asset_name, mode="prod"):
    base = get_base_path(mode)
    return f"{base}/assets/{asset_name}"
```

## ✨ Best Practices

1. 🎯 Always provide a mode parameter in functions that use get_base_path
2. 🚀 Use default "prod" mode for production safety
3. 📋 Keep path construction consistent across your application
4. 🔄 Use os.path.join for cross-platform compatibility
5. 📚 Document which mode is expected in your functions

## ⚠️ Error Handling

The function is simple and doesn't raise exceptions, but you should:
- ✅ Validate that the resulting paths exist before using them
- 🔍 Handle file not found errors appropriately
- 🛡️ Consider implementing path existence checks in your application

## 🔄 Integration Examples

### 📂 With File Operations
```python
def read_config(mode="prod"):
    config_path = f"{get_base_path(mode)}/config/settings.json"
    with open(config_path, 'r') as f:
        return f.read()
```

### 📝 With Template Loading
```python
def load_template(template_name, mode="prod"):
    template_path = f"{get_base_path(mode)}/templates/{template_name}"
    with open(template_path, 'r') as f:
        return f.read()
```

### 🖼️ With Asset Management
```python
def get_image_url(image_name, mode="prod"):
    base = get_base_path(mode)
    return f"{base}/assets/images/{image_name}"
