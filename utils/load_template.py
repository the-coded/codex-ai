"""
Template loading utility.

This module provides functionality to load and process template files with variable substitution.

Example template file (template.txt):
    Hello ${name}!
    Your age is ${age}.
    Your favorite color is ${color}.

Example usage:
    from utils.load_template import load_template

    # Load and process template with variables
    result = load_template('template.txt', 
        name='John',
        age='30',
        color='blue'
    )
    print(result)
    # Output:
    # Hello John!
    # Your age is 30.
    # Your favorite color is blue.

    # Template with optional variables
    result = load_template('welcome.txt',
        user='Alice',
        greeting='Good morning'  # Optional
    )

    # Template with conditional content
    result = load_template('email.txt',
        user='Bob',
        is_premium='true',
        premium_features='Access to exclusive content'  # Only used if is_premium='true'
    )
"""

from string import Template
from typing import Dict, Any

def load_template(filename: str, **kwargs: Any) -> str:
    """
    Load and process a template file with variable substitution.

    The function reads a template file and substitutes variables using the string.Template
    format. Variables in the template should be in the format ${variable_name}.

    Args:
        filename (str): Path to the template file
        **kwargs: Keyword arguments containing values for template variables
            - Each key should match a variable name in the template
            - Values can be any type that can be converted to string

    Returns:
        str: The processed template with all variables substituted

    Raises:
        FileNotFoundError: If the template file doesn't exist
        KeyError: If a required template variable is missing from kwargs
        ValueError: If the template format is invalid

    Examples:
        # Template file (email.txt):
        # Subject: ${subject}
        # Dear ${name},
        # ${message}
        # Best regards,
        # ${sender}

        result = load_template('email.txt',
            subject='Welcome',
            name='John Doe',
            message='Thank you for joining us.',
            sender='The Team'
        )

        # Template with conditional content (notification.txt):
        # Hello ${user}!
        # ${alert_type}: ${message}
        # ${priority_note}

        result = load_template('notification.txt',
            user='Alice',
            alert_type='Warning',
            message='Your subscription is expiring soon.',
            priority_note='Please renew within 7 days.'
        )

        # Template with formatting (report.txt):
        # Report: ${title}
        # Date: ${date}
        # Status: ${status}
        # Details: ${details}

        result = load_template('report.txt',
            title='Monthly Summary',
            date='2023-12-01',
            status='Completed',
            details='All tasks finished on schedule.'
        )
    """
    try:
        with open(filename, 'r') as file:
            template = Template(file.read())
        return template.substitute(**kwargs)
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {filename}")
    except KeyError as e:
        raise KeyError(f"Missing template variable: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid template format: {e}")
