#!/usr/bin/env python3
"""
Example usage of Git Commit Assistant

This is a simple demonstration file to show how the Git Commit Assistant works.
You can make changes to this file, stage them with git add, and then run the
Git Commit Assistant to generate a commit message.
"""

def example_function():
    """This is an example function."""
    print("Hello, Git Commit Assistant!")
    
    # TODO: Add more functionality here
    
    return True

class ExampleClass:
    """An example class to demonstrate Git Commit Assistant."""
    
    def __init__(self, name):
        self.name = name
        self.created_at = "2025-07-21"  # Current date
    
    def greet(self):
        """Greet the user with their name."""
        return f"Hello, {self.name}!"
    
    def get_info(self):
        """Get information about the example class."""
        return {
            "name": self.name,
            "created_at": self.created_at,
            "version": "1.0.0",
            "description": "Example class for Git Commit Assistant"
        }

# New feature: Added a utility function
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

# New feature: Added a list processing function
def process_items(items):
    """Process a list of items."""
    if not items:
        return []
    
    return [item.upper() for item in items if isinstance(item, str)]

if __name__ == "__main__":
    # Example usage
    example_function()
    
    example = ExampleClass("Developer")
    print(example.greet())
    print(example.get_info())
    
    # Test new functions
    print(f"Sum: {calculate_sum(5, 3)}")
    print(f"Processed items: {process_items(['apple', 'banana', 'cherry'])}")