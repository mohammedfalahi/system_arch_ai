"""
Workflow Reasoner Agent.
Analyzes user requirements and breaks down workflows into logical steps.
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.bedrock_client import BedrockClient
from integrations.api_catalog import APICatalog
from typing import Dict, Any


class WorkflowReasonerAgent:
    """
    Analyzes business process descriptions and generates structured workflow plans.
    Acts as a business process analyst to convert requirements into actionable steps.
    """
    
    SYSTEM_PROMPT = """You are an expert business process analyst and workflow architect.

Your role is to:
1. Analyze business process descriptions from users
2. Break down complex processes into clear, sequential, executable steps
3. Identify required integrations (email, Slack, databases, APIs, etc.)
4. Structure the workflow in a way that can be automated with code

When analyzing a process:
- Think step-by-step about what needs to happen
- Identify dependencies between steps
- Specify what integrations or tools are needed
- Consider inputs required and outputs produced
- Assess complexity realistically

You MUST respond with ONLY valid JSON in this exact format:
{
  "process_name": "Short descriptive name",
  "description": "Clear description of what this workflow does",
  "steps": [
    {
      "step_number": 1,
      "step_name": "Short step name",
      "description": "Detailed description of what happens in this step",
      "action": "Specific action to perform (e.g., 'send_email', 'create_user', 'query_database')",
      "integration_needed": "Name of integration/service needed (e.g., 'email', 'slack', 'database') or null"
    }
  ],
  "inputs": ["List of required inputs from user"],
  "outputs": ["List of outputs/results produced"],
  "estimated_complexity": "low" or "medium" or "high"
}

Do not include any explanatory text, markdown formatting, or code blocks - only the JSON object."""
    
    def __init__(self, bedrock_client: BedrockClient = None):
        """
        Initialize the WorkflowReasonerAgent.
        
        Args:
            bedrock_client: Optional BedrockClient instance. Creates new one if not provided.
        """
        self.bedrock_client = bedrock_client or BedrockClient()
        self.api_catalog = APICatalog()
    
    def analyze(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze a business process description and generate a structured workflow plan.
        
        Args:
            user_input: Natural language description of the business process to automate
            
        Returns:
            Dictionary containing structured workflow plan with:
            - process_name: Name of the workflow
            - description: What the workflow does
            - steps: List of sequential steps with actions and integrations
            - inputs: Required inputs
            - outputs: Expected outputs
            - estimated_complexity: Complexity level (low/medium/high)
            
        Raises:
            ValueError: If the response cannot be parsed as valid JSON
        """
        try:
            # Discover relevant APIs
            discovered_apis = self.api_catalog.get_apis_for_workflow(user_input)
            
            # Build API context
            api_context = ""
            if discovered_apis:
                api_context = "\n\nAvailable APIs discovered for this workflow:\n"
                for action, apis in discovered_apis.items():
                    api_context += f"\nFor '{action}':\n"
                    for api in apis:
                        api_context += f"  - {api.provider}: {api.description}\n"
            
            # Call Claude to analyze the workflow
            response = self.bedrock_client.call_claude(
                system_prompt=self.SYSTEM_PROMPT,
                user_message=f"Analyze this business process and create a structured workflow plan:\n\n{user_input}{api_context}",
                temperature=0.3  # Lower temperature for more consistent structured output
            )
            
            # Parse JSON response
            workflow_plan = self._parse_json_response(response)
            
            # Validate required fields
            self._validate_workflow_plan(workflow_plan)
            
            return workflow_plan
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse workflow plan as JSON: {str(e)}\nResponse: {response[:200]}")
        except Exception as e:
            raise ValueError(f"Error analyzing workflow: {str(e)}")
    
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
    
    def _validate_workflow_plan(self, plan: Dict[str, Any]) -> None:
        """
        Validate that the workflow plan has all required fields.
        
        Args:
            plan: Workflow plan dictionary to validate
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["process_name", "description", "steps", "inputs", "outputs", "estimated_complexity"]
        missing_fields = [field for field in required_fields if field not in plan]
        
        if missing_fields:
            raise ValueError(f"Workflow plan missing required fields: {', '.join(missing_fields)}")
        
        if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
            raise ValueError("Workflow plan must have at least one step")
        
        # Validate each step has required fields
        step_required = ["step_number", "step_name", "description", "action"]
        for i, step in enumerate(plan["steps"]):
            missing = [field for field in step_required if field not in step]
            if missing:
                raise ValueError(f"Step {i+1} missing required fields: {', '.join(missing)}")


if __name__ == "__main__":
    print("Testing WorkflowReasonerAgent...\n")
    
    try:
        # Initialize agent
        agent = WorkflowReasonerAgent()
        print("✓ WorkflowReasonerAgent initialized\n")
        
        # Test: Employee onboarding workflow
        print("=" * 70)
        print("Test: Analyzing employee onboarding workflow")
        print("=" * 70)
        
        test_prompt = """I need to automate employee onboarding - send welcome email, 
create Slack account, assign mentor, schedule first week meetings"""
        
        print(f"\nInput: {test_prompt}\n")
        print("Analyzing workflow...\n")
        
        result = agent.analyze(test_prompt)
        
        # Pretty print the result
        print("\n" + "=" * 70)
        print("WORKFLOW ANALYSIS RESULT")
        print("=" * 70)
        print(f"\nProcess Name: {result['process_name']}")
        print(f"Description: {result['description']}")
        print(f"Complexity: {result['estimated_complexity'].upper()}")
        
        print(f"\nInputs Required:")
        for inp in result['inputs']:
            print(f"  - {inp}")
        
        print(f"\nWorkflow Steps:")
        for step in result['steps']:
            print(f"\n  Step {step['step_number']}: {step['step_name']}")
            print(f"    Description: {step['description']}")
            print(f"    Action: {step['action']}")
            if step.get('integration_needed'):
                print(f"    Integration: {step['integration_needed']}")
        
        print(f"\nExpected Outputs:")
        for out in result['outputs']:
            print(f"  - {out}")
        
        print("\n" + "=" * 70)
        print("\n✅ Test completed successfully!")
        print("\nFull JSON output:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
