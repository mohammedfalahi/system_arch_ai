"""
Code Generator Agent.
Generates executable Python code from workflow steps.
"""

import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.bedrock_client import BedrockClient
from typing import Dict, Any, Tuple, List


class CodeGeneratorAgent:
    """
    Generates executable Python code from structured workflow plans.
    Creates clean, well-documented code with error handling and progress tracking.
    """
    
    SYSTEM_PROMPT = """You are an expert Python developer specializing in workflow automation.

CRITICAL RULE - USE ACTUAL VALUES FROM USER INPUT:

When generating code, you MUST extract and use ACTUAL values from the workflow description, NOT placeholder examples.

WRONG (using placeholders):
```python
email.send_email(to='john.doe@company.com', subject='Welcome')  # ❌ Don't do this!
```

CORRECT (using actual values from user input):
```python
# If user says "Send email to sarah@example.com"
email.send_email(to='sarah@example.com', subject='Welcome')  # ✅ Use the actual email!
```

EXTRACTION RULES:
- Email addresses: Use the EXACT email from the workflow description
- Channel names: Use the EXACT channel name specified
- Names: Use the EXACT person name mentioned
- Dates: Use the EXACT date specified
- Messages: Use the EXACT message text or close paraphrase

If the workflow says:
"Send email to mohammed.falahi.nt@gmail.com with subject 'Welcome to TechCorp!' and message 'Hi John, Welcome aboard!'"

Then generate:
```python
email.send_email(
    to='mohammed.falahi.nt@gmail.com',  # ← EXACT email from input
    subject='Welcome to TechCorp!',     # ← EXACT subject from input
    body='Hi John, Welcome aboard!'     # ← EXACT message from input
)
```

EXECUTION SECTION MUST USE ACTUAL VALUES FROM USER INPUT:

When generating code with a workflow() function, the execution section (if __name__ == "__main__":) 
MUST call the function with the ACTUAL values extracted from the user's workflow description.

WRONG (placeholder values in execution):
```python
if __name__ == "__main__":
    workflow(
        employee_name="Sarah Johnson",              # ❌ Placeholder example
        employee_email="sarah.johnson@company.com", # ❌ Not from user input
        hr_email="hr@company.com"                   # ❌ Generic placeholder
    )
```

CORRECT (actual values from user input):
```python
if __name__ == "__main__":
    # Use actual values from workflow description
    workflow(
        employee_name="John Smith",                           # ✅ From user input
        employee_email="mohammed.falahi.nt@gmail.com",        # ✅ Actual email from input
        hr_email="dailyusegadjects.store@gmail.com",          # ✅ Actual email from input  
        slack_channel="new-channel",                          # ✅ Actual channel from input
        start_date="Monday"                                   # ✅ Actual date from input
    )
```

EXTRACTION INSTRUCTIONS:
- Parse the workflow_plan JSON for actual values in step descriptions
- Look for email addresses in the workflow description
- Look for channel names specified
- Look for person names mentioned
- Use those EXACT values in both function body AND execution section

NEVER use placeholders like:
❌ user@example.com
❌ john.doe@company.com
❌ hr@company.com
❌ test@example.com

Always extract actual values from the workflow_plan JSON or user input.

CRITICAL INTEGRATION RULES:
1. ALWAYS import and use real integration classes - NEVER create mock functions
2. For Slack: ALWAYS use integrations.slack_integration.SlackIntegration
3. For Email: ALWAYS use integrations.email_integration.EmailIntegration
4. NEVER write mock functions like "# Mock email sending"
5. NEVER write docstrings that say "Mock" anything
6. use_mock parameter must ALWAYS be False for production workflows

FORBIDDEN PATTERNS - NEVER GENERATE:
❌ def send_email(...): # Mock sending
❌ # Mock email sending
❌ Mock sending email using Gmail API (in docstrings)
❌ use_mock=True
❌ Creating mock functions instead of using integrations

Your role is to:
1. Take structured workflow plans and convert them into clean, executable Python code
2. Generate production-quality code with proper error handling
3. Include progress tracking with print statements
4. Use REAL integrations from the integrations module
5. Add clear comments explaining the code
6. Make the code immediately executable

Code requirements:
- Create a main workflow() function that orchestrates all steps
- Create separate functions for each workflow step
- Use try/except blocks for error handling
- Add print statements to track progress (e.g., "Step 1: Sending email...")
- Include docstrings for all functions
- Make the code self-contained and executable

CORRECT EMAIL INTEGRATION EXAMPLE:
```python
from integrations.email_integration import EmailIntegration

# Initialize with real SMTP (NOT mock)
email = EmailIntegration(use_mock=False)

# Send email using real API
result = email.send_email(
    to='recipient@example.com',
    subject='Email Subject',
    body='Email message content'
)

print(result['message'])  # Shows success/error

if result['success']:
    print(f"✅ Email sent successfully")
else:
    print(f"❌ Email failed: {result.get('error', 'unknown error')}")
```

CORRECT SLACK INTEGRATION EXAMPLE:
```python
from integrations.slack_integration import SlackIntegration

# Initialize with real API (NOT mock)
slack = SlackIntegration(use_mock=False)

# Send message using real API
result = slack.send_message(
    channel='channel-name',  # without # prefix
    text='Your message here'
)

print(result['message'])  # Shows success/error

if result['success']:
    print(f"✅ Slack message sent successfully")
else:
    print(f"❌ Slack failed: {result.get('error', 'unknown error')}")
```

SLACK RICH MESSAGE EXAMPLE:
```python
from integrations.slack_integration import SlackIntegration

slack = SlackIntegration(use_mock=False)

result = slack.send_rich_message(
    channel='channel-name',
    title='Workflow Update',
    message='Task completed successfully',
    fields={
        'Status': 'Complete',
        'Time': '2 minutes'
    }
)
print(result['message'])
```

ERROR HANDLING PATTERN:
```python
try:
    result = slack.send_message('channel-name', 'Test message')
    print(result['message'])
    
    if not result['success']:
        print(f"Warning: {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"Error sending Slack message: {e}")
```

OTHER DATA OPERATIONS:
- Database: Use in-memory dict/list for data storage
- API calls: Use print statements to show what would be called
- Calendar: Use print statements to show scheduled events

IMPORTANT: Return ONLY the Python code. Do not include:
- Markdown code blocks (no ```python or ```)
- Explanatory text before or after the code
- Any formatting other than the raw Python code

The code should start directly with imports or comments."""
    
    def __init__(self, bedrock_client: BedrockClient = None):
        """
        Initialize the CodeGeneratorAgent.
        
        Args:
            bedrock_client: Optional BedrockClient instance. Creates new one if not provided.
        """
        self.bedrock_client = bedrock_client or BedrockClient()
    
    def generate(self, workflow_plan: Dict[str, Any]) -> str:
        """
        Generate executable Python code from a workflow plan.
        
        Args:
            workflow_plan: Structured workflow plan from WorkflowReasonerAgent containing:
                - process_name: Name of the workflow
                - description: What the workflow does
                - steps: List of workflow steps with actions
                - inputs: Required inputs
                - outputs: Expected outputs
                
        Returns:
            String containing executable Python code
            
        Raises:
            ValueError: If workflow plan is invalid or code generation fails
        """
        try:
            # Format the workflow plan for Claude
            workflow_json = json.dumps(workflow_plan, indent=2)
            
            user_message = f"""Generate executable Python code for this workflow:

{workflow_json}

Remember:
- Create a workflow() function as the main entry point
- Create separate functions for each step
- Use mock implementations for integrations
- Include error handling and progress tracking
- Return ONLY the Python code, no markdown or explanations"""
            
            # Generate code with lower temperature for consistency
            code = self.bedrock_client.call_claude(
                system_prompt=self.SYSTEM_PROMPT,
                user_message=user_message,
                temperature=0.3
            )
            
            # Clean up the code (remove markdown if present)
            code = self._clean_code(code)
            
            return code
            
        except Exception as e:
            raise ValueError(f"Error generating code: {str(e)}")
    
    def _clean_code(self, code: str) -> str:
        """
        Remove markdown formatting and clean up generated code.
        
        Args:
            code: Raw code string from Claude
            
        Returns:
            Cleaned Python code
        """
        # Remove markdown code blocks
        code = re.sub(r'^```python\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'^```\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'^```.*$', '', code, flags=re.MULTILINE)
        
        # Remove leading/trailing whitespace
        code = code.strip()
        
        return code
    
    def validate_generated_code(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate that the generated code is valid Python and has required structure.
        
        Args:
            code: Python code string to validate
            
        Returns:
            Tuple of (is_valid, issues)
            - is_valid: True if code is valid, False otherwise
            - issues: List of validation issues found (empty if valid)
        """
        issues = []
        
        # Check if code is not empty
        if not code or not code.strip():
            issues.append("Generated code is empty")
            return False, issues
        
        # Check Python syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            issues.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return False, issues
        except Exception as e:
            issues.append(f"Compilation error: {str(e)}")
            return False, issues
        
        # Check for main workflow function
        if 'def workflow(' not in code:
            issues.append("Missing main workflow() function")
        
        # Check for basic structure elements
        if 'def ' not in code:
            issues.append("No functions defined in code")
        
        # Check for error handling
        if 'try:' not in code and 'except' not in code:
            issues.append("Warning: No error handling (try/except) found")
        
        # Check for progress tracking
        if 'print(' not in code:
            issues.append("Warning: No progress tracking (print statements) found")
        
        # If we have issues, return False
        is_valid = len([i for i in issues if not i.startswith('Warning:')]) == 0
        
        return is_valid, issues


if __name__ == "__main__":
    print("Testing CodeGeneratorAgent...\n")
    
    try:
        # Initialize agent
        agent = CodeGeneratorAgent()
        print("✓ CodeGeneratorAgent initialized\n")
        
        # Create a sample workflow plan
        print("=" * 70)
        print("Creating sample workflow plan...")
        print("=" * 70)
        
        sample_workflow = {
            "process_name": "Customer Support Ticket Handler",
            "description": "Automated workflow to process customer support tickets",
            "steps": [
                {
                    "step_number": 1,
                    "step_name": "Receive Ticket",
                    "description": "Receive and parse incoming support ticket",
                    "action": "parse_ticket",
                    "integration_needed": None
                },
                {
                    "step_number": 2,
                    "step_name": "Categorize Ticket",
                    "description": "Analyze ticket content and assign category",
                    "action": "categorize_ticket",
                    "integration_needed": None
                },
                {
                    "step_number": 3,
                    "step_name": "Send Acknowledgment",
                    "description": "Send automated acknowledgment email to customer",
                    "action": "send_email",
                    "integration_needed": "email"
                },
                {
                    "step_number": 4,
                    "step_name": "Assign to Agent",
                    "description": "Assign ticket to appropriate support agent",
                    "action": "assign_ticket",
                    "integration_needed": "database"
                },
                {
                    "step_number": 5,
                    "step_name": "Notify Agent",
                    "description": "Send Slack notification to assigned agent",
                    "action": "send_slack_message",
                    "integration_needed": "slack"
                }
            ],
            "inputs": ["ticket_id", "customer_email", "ticket_subject", "ticket_body"],
            "outputs": ["ticket_category", "assigned_agent", "acknowledgment_sent"],
            "estimated_complexity": "medium"
        }
        
        print(f"\nWorkflow: {sample_workflow['process_name']}")
        print(f"Steps: {len(sample_workflow['steps'])}\n")
        
        # Generate code
        print("=" * 70)
        print("Generating Python code...")
        print("=" * 70)
        print()
        
        generated_code = agent.generate(sample_workflow)
        
        # Validate the generated code
        is_valid, issues = agent.validate_generated_code(generated_code)
        
        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        print(f"Valid: {is_valid}")
        if issues:
            print("Issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found!")
        
        # Print the generated code
        print("\n" + "=" * 70)
        print("GENERATED CODE")
        print("=" * 70)
        print()
        print(generated_code)
        print()
        print("=" * 70)
        
        if is_valid:
            print("\n✅ Code generation test completed successfully!")
            print("\nThe generated code is ready to execute.")
        else:
            print("\n⚠️  Code generated but has validation issues.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
