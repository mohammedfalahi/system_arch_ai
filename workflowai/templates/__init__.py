"""
Templates package for WorkflowAI.
Contains pre-built workflow templates for common use cases.
"""

import os

def get_all_templates():
    """
    Get all available workflow templates.
    
    Returns:
        Dictionary mapping template names to their source code
    """
    templates = {}
    
    # Get the directory where this file is located
    template_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define template files
    template_files = {
        "Employee Onboarding": "employee_onboarding.py",
        "Customer Support": "customer_support.py",
        "Invoice Processing": "invoice_processing.py"
    }
    
    # Read each template file
    for template_name, filename in template_files.items():
        filepath = os.path.join(template_dir, filename)
        try:
            with open(filepath, 'r') as f:
                templates[template_name] = f.read()
        except FileNotFoundError:
            templates[template_name] = f"# Template file {filename} not found"
    
    return templates

def get_template_descriptions():
    """
    Get descriptions of all available templates.
    
    Returns:
        Dictionary mapping template names to their descriptions
    """
    return {
        "Employee Onboarding": "Automates employee onboarding with welcome emails, account creation, mentor assignment, and meeting scheduling",
        "Customer Support": "Routes customer support tickets by urgency, assigns to team members, and sends notifications",
        "Invoice Processing": "Processes invoices with validation, approval workflows, and accounting system updates"
    }
