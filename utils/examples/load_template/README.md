# 📝 load_template Usage Examples

This directory contains examples demonstrating how to use the `load_template` utility.

## 📖 Overview

The `load_template` utility provides functionality to load template files and substitute variables, making it easy to generate dynamic content from template files.

## 📁 Files

- 📋 `template_example.txt`: Example template file showing variable substitution
- 💻 `template_usage.py`: Python script demonstrating how to use the template

## 🚀 Running the Example

```bash
# From the project root
python utils/examples/load_template/template_usage.py
```

## 📋 Template Format

Templates use the `${variable_name}` syntax for variable substitution. For example:

```
Subject: ${subject}
To: ${recipient_name}
From: ${sender_name}
```

## 💡 Basic Usage

```python
from utils.load_template import load_template

# Load and process template
result = load_template('template.txt',
    subject="Hello",
    recipient_name="John",
    sender_name="Alice"
)
print(result)
```

## 🔄 Variable Substitution

The `load_template` function accepts keyword arguments that match the variables in your template:

```python
result = load_template('email_template.txt',
    subject="Project Update",
    recipient_name="John Doe",
    sender_name="Alice Smith",
    priority="High",
    message="Important update...",
    status="In Progress",
    progress="50",
    next_steps="Review needed",
    closing_message="Thank you",
    sender_title="Manager"
)
```

## ⚠️ Error Handling

The function will raise:
- 📂 `FileNotFoundError`: If the template file doesn't exist
- 🔑 `KeyError`: If a required template variable is missing
- ❌ `ValueError`: If the template format is invalid

```python
try:
    result = load_template('template.txt', name="John")
except FileNotFoundError:
    print("Template file not found")
except KeyError as e:
    print(f"Missing template variable: {e}")
except ValueError as e:
    print(f"Invalid template format: {e}")
```

## 🎯 Common Use Cases

### 📧 Email Templates
```python
def send_welcome_email(user_name):
    content = load_template('templates/welcome.txt',
        name=user_name,
        date=datetime.now().strftime("%Y-%m-%d")
    )
    send_email(content)
```

### 📊 Report Generation
```python
def generate_report(data):
    return load_template('templates/report.txt',
        title=data['title'],
        content=data['content'],
        author=data['author']
    )
```

### ⚙️ Configuration Files
```python
def create_config(settings):
    return load_template('templates/config.txt',
        host=settings['host'],
        port=settings['port'],
        username=settings['user']
    )
```

## ✨ Best Practices

1. 📁 Keep templates in a dedicated directory
2. 🏷️ Use descriptive variable names
3. 📚 Document required variables
4. 🔍 Handle missing variables gracefully
5. ✅ Validate template content
6. 📋 Use consistent naming conventions
7. 🎯 Keep templates simple and focused

## 🔄 Integration Examples

### 📧 With Email System
```python
def send_notification(user, event):
    content = load_template('notifications/event.txt',
        user_name=user.name,
        event_name=event.name,
        event_date=event.date
    )
    send_email(user.email, content)
```

### 📊 With Report Generator
```python
def create_monthly_report(data):
    return load_template('reports/monthly.txt',
        month=data['month'],
        metrics=data['metrics'],
        summary=data['summary']
    )
```

### 📄 With Document Generation
```python
def generate_contract(client):
    return load_template('contracts/standard.txt',
        client_name=client.name,
        start_date=client.start_date,
        terms=client.terms
    )
