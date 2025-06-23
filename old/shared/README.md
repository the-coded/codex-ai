# 🔄 Shared Scripts

This directory contains shared scripts used across the project for various common tasks.

## 📦 Available Scripts

### require_aider-chat.py
Checks and installs aider-chat dependency:
- ✅ Verifies if aider-chat is installed in current venv
- 📥 Installs aider-chat 0.60.0 if not present
- ⚠️ Handles installation errors appropriately

Usage:
```bash
python shared/require_aider-chat.py
```

## 🚀 Running Scripts

Scripts in this directory can be run directly using Python:
```bash
python shared/<script_name>.py
```

## 📁 Directory Structure

```
shared/
├── README.md              # This documentation
└── require_aider-chat.py  # Aider-chat requirement checker
```

## ✨ Best Practices

When adding new shared scripts:
1. 📝 Create focused, single-purpose scripts
2. ⚠️ Include proper error handling
3. 📖 Add documentation in this README
4. ✅ Verify virtual environment compatibility
5. 🔄 Test in both development and production modes
