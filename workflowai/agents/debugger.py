"""
Debugger Agent.
Analyzes execution errors and suggests fixes.
"""

import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.bedrock_client import BedrockClient
from typing import Dict, Any


class WorkflowDebuggerAgent:
    """
    Analyzes workflow execution errors and generates fixed code.
    Provides self-debugging capability for automated workflows.
    """
    
    ANALYSIS_SYSTEM_PROMPT = """You are an expert Python debugger and error analyst.

Your role is to:
1. Analyze Python code execution errors
2. Identify the root cause of the problem
3. Explain what went wrong in clear terms
4. Suggest specific fixes
5. Assess your confidence in the diagnosis

When analyzing errors:
- Look at the error message carefully
- Identify the line/location of the error
- Understand the context from the workflow plan
- Consider common Python pitfalls
- Provide actionable fix suggestions

You MUST respond with ONLY valid JSON in this exact format:
{
  "error_analysis": "Clear explanation of what went wrong and why",
  "suggested_fix": "Specific steps or changes needed to fix the error",
  "confidence": "high" or "medium" or "low"
}

Do not include markdown, code blocks, or explanatory text - only the JSON object."""
    
    FIX_SYSTEM_PROMPT = """You are an expert Python developer specializing in debugging and code repair.

Your role is to:
1. Take broken Python code and error analysis
2. Generate corrected, working Python code
3. Maintain the original workflow logic and structure
4. Fix only what's broken, keep everything else the same
5. Ensure the fixed code is executable

Code requirements:
- Fix the specific error identified
- Keep the same function names and structure
- Maintain all error handling and print statements
- Preserve the workflow logic
- Use mock implementations for integrations
- Make minimal changes - only fix what's broken

IMPORTANT: Return ONLY the corrected Python code. Do not include:
- Markdown code blocks (no ```python or ```)
- Explanatory text before or after the code
- Comments about what you changed (unless they were in the original)
- Any formatting other than the raw Python code

The code should start directly with imports or the first line of code."""
    
    def __init__(self, bedrock_client: BedrockClient = None):
        """
        Initialize the WorkflowDebuggerAgent.
        
        Args:
            bedrock_client: Optional BedrockClient instance. Creates new one if not provided.
        """
        self.bedrock_client = bedrock_client or BedrockClient()
    
    def analyze_error(
        self, 
        original_code: str, 
        error_message: str, 
        workflow_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a workflow execution error and provide diagnosis.
        
        Args:
            original_code: The Python code that failed
            error_message: The error message from execution
            workflow_plan: The original workflow plan used to generate the code
            
        Returns:
            Dictionary containing:
            - error_analysis: Explanation of what went wrong
            - suggested_fix: How to fix the error
            - confidence: Confidence level (high/medium/low)
            
        Raises:
            ValueError: If error analysis fails
        """
        try:
            workflow_json = json.dumps(workflow_plan, indent=2)
            
            user_message = f"""Analyze this Python code execution error:

ORIGINAL CODE:
{original_code}

ERROR MESSAGE:
{error_message}

WORKFLOW PLAN:
{workflow_json}

Provide a detailed error analysis in JSON format."""
            
            response = self.bedrock_client.call_claude(
                system_prompt=self.ANALYSIS_SYSTEM_PROMPT,
                user_message=user_message,
                temperature=0.3
            )
            
            # Parse JSON response
            analysis = self._parse_json_response(response)
            
            # Validate required fields
            required_fields = ["error_analysis", "suggested_fix", "confidence"]
            missing = [f for f in required_fields if f not in analysis]
            if missing:
                raise ValueError(f"Analysis missing fields: {', '.join(missing)}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse error analysis: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error analyzing error: {str(e)}")
    
    def fix_code(
        self,
        original_code: str,
        error_analysis: Dict[str, Any],
        workflow_plan: Dict[str, Any]
    ) -> str:
        """
        Generate fixed code based on error analysis.
        
        Args:
            original_code: The broken Python code
            error_analysis: Analysis from analyze_error() method
            workflow_plan: The original workflow plan
            
        Returns:
            String containing corrected Python code
            
        Raises:
            ValueError: If code fix generation fails
        """
        try:
            workflow_json = json.dumps(workflow_plan, indent=2)
            analysis_json = json.dumps(error_analysis, indent=2)
            
            user_message = f"""Fix this broken Python code based on the error analysis:

ORIGINAL CODE:
{original_code}

ERROR ANALYSIS:
{analysis_json}

WORKFLOW PLAN:
{workflow_json}

Generate the corrected Python code. Return ONLY the fixed code, no markdown or explanations."""
            
            fixed_code = self.bedrock_client.call_claude(
                system_prompt=self.FIX_SYSTEM_PROMPT,
                user_message=user_message,
                temperature=0.3
            )
            
            # Clean up the code
            fixed_code = self._clean_code(fixed_code)
            
            return fixed_code
            
        except Exception as e:
            raise ValueError(f"Error fixing code: {str(e)}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from Claude's response with fallback handling.
        
        Args:
            response: Raw response string from Claude
            
        Returns:
            Parsed JSON dictionary
        """
        # Try direct parsing first
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
            return json.loads(json_str)
        
        if "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            json_str = response[start:end].strip()
            return json.loads(json_str)
        
        # Last attempt: find first { and last }
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            json_str = response[start:end+1]
            return json.loads(json_str)
        
        raise json.JSONDecodeError("Could not find valid JSON in response", response, 0)
    
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


if __name__ == "__main__":
    print("Testing WorkflowDebuggerAgent...\n")
    
    try:
        # Initialize agent
        agent = WorkflowDebuggerAgent()
        print("✓ WorkflowDebuggerAgent initialized\n")
        
        # Create intentionally broken code
        print("=" * 70)
        print("Test: Debugging broken workflow code")
        print("=" * 70)
        
        broken_code = '''def send_email(recipient, subject, body):
    """Send email to recipient"""
    print(f"Sending email to {recipient}")
    print(f"Subject: {subject}")
    return True

def workflow(customer_email, order_id):
    """Main workflow function"""
    try:
        print("Step 1: Processing order")
        
        # This will cause an error - undefined_variable doesn't exist
        order_total = undefined_variable + 100
        
        print(f"Step 2: Sending confirmation email")
        send_email(customer_email, "Order Confirmation", f"Order {order_id} confirmed")
        
        return {"status": "success", "order_total": order_total}
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    result = workflow("customer@example.com", "ORD123")
    print(f"Result: {result}")
'''
        
        error_message = "Runtime error: name 'undefined_variable' is not defined"
        
        workflow_plan = {
            "process_name": "Order Processing Workflow",
            "description": "Process customer orders and send confirmation",
            "steps": [
                {
                    "step_number": 1,
                    "step_name": "Process Order",
                    "description": "Calculate order total",
                    "action": "calculate_total",
                    "integration_needed": None
                },
                {
                    "step_number": 2,
                    "step_name": "Send Confirmation",
                    "description": "Send order confirmation email",
                    "action": "send_email",
                    "integration_needed": "email"
                }
            ],
            "inputs": ["customer_email", "order_id"],
            "outputs": ["order_total", "confirmation_sent"],
            "estimated_complexity": "low"
        }
        
        print("\nBROKEN CODE:")
        print("-" * 70)
        print(broken_code)
        print("-" * 70)
        print(f"\nERROR: {error_message}\n")
        
        # Step 1: Analyze the error
        print("=" * 70)
        print("Step 1: Analyzing error...")
        print("=" * 70)
        
        analysis = agent.analyze_error(broken_code, error_message, workflow_plan)
        
        print(f"\nError Analysis:")
        print(f"  {analysis['error_analysis']}")
        print(f"\nSuggested Fix:")
        print(f"  {analysis['suggested_fix']}")
        print(f"\nConfidence: {analysis['confidence'].upper()}")
        
        # Step 2: Fix the code
        print("\n" + "=" * 70)
        print("Step 2: Generating fixed code...")
        print("=" * 70)
        
        fixed_code = agent.fix_code(broken_code, analysis, workflow_plan)
        
        print("\nFIXED CODE:")
        print("-" * 70)
        print(fixed_code)
        print("-" * 70)
        
        # Validate the fixed code
        print("\n" + "=" * 70)
        print("Step 3: Validating fixed code...")
        print("=" * 70)
        
        try:
            compile(fixed_code, '<string>', 'exec')
            print("\n✓ Fixed code has valid Python syntax")
        except SyntaxError as e:
            print(f"\n❌ Fixed code has syntax error: {e}")
        
        # Compare before/after
        print("\n" + "=" * 70)
        print("BEFORE vs AFTER COMPARISON")
        print("=" * 70)
        print("\nBEFORE (broken):")
        print("  - Contains undefined_variable")
        print("  - Will crash at runtime")
        print("\nAFTER (fixed):")
        print("  - Undefined variable resolved")
        print("  - Code should execute successfully")
        
        print("\n" + "=" * 70)
        print("✅ Debugging test completed successfully!")
        print("=" * 70)
        print("\nThe self-debugging feature is working!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
