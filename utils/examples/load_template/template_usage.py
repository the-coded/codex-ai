"""
Example usage of the load_template utility.

This script demonstrates how to use the load_template function with different
template files and variable substitutions.
"""

from utils.load_template import load_template

def main():
    """
    Demonstrates different ways to use the load_template utility.
    """
    # Example 1: Project Status Email
    print("Example 1: Project Status Email")
    print("-" * 50)
    
    result = load_template('utils/examples/load_template/template_example.txt',
        subject="Project XYZ Status Update",
        recipient_name="John Doe",
        sender_name="Alice Smith",
        sender_title="Project Manager",
        priority="High",
        message="I hope this email finds you well. I wanted to provide you with the latest updates on Project XYZ.",
        status="On Track",
        progress="75",
        next_steps="Schedule final review meeting",
        closing_message="Please let me know if you have any questions or concerns."
    )
    print(result)
    print()

    # Example 2: Meeting Invitation
    print("Example 2: Meeting Invitation")
    print("-" * 50)
    
    result = load_template('utils/examples/load_template/template_example.txt',
        subject="Team Meeting Invitation",
        recipient_name="Sarah Johnson",
        sender_name="Bob Wilson",
        sender_title="Team Lead",
        priority="Normal",
        message="I would like to invite you to our weekly team sync meeting.",
        status="Scheduled",
        progress="0",
        next_steps="Prepare agenda items",
        closing_message="Looking forward to our discussion."
    )
    print(result)

if __name__ == "__main__":
    main()
