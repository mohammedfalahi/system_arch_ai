"""Intelligent Requirement Clarification Agent"""
from utils.bedrock_client import BedrockClient
from typing import List, Dict, Any
import json

class ClarifierAgent:
    """Asks clarifying questions for ambiguous requirements"""
    
    def __init__(self, bedrock_client: BedrockClient):
        self.client = bedrock_client
    
    def analyze_requirements(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze if requirements need clarification
        
        Returns:
            {
                'needs_clarification': bool,
                'questions': List[str],
                'ambiguities': List[str],
                'confidence': int
            }
        """
        system_prompt = """You are a requirements analyst. Analyze user input for workflow automation.

Identify if requirements are:
1. Clear and complete (can build workflow immediately)
2. Ambiguous (need clarification)

For ambiguous requirements, identify:
- Missing information
- Unclear steps
- Vague integrations

Output JSON:
{
    "needs_clarification": true/false,
    "questions": ["question 1", "question 2"],
    "ambiguities": ["what's unclear 1", "what's unclear 2"],
    "confidence": 0-100
}

Ask MAX 3 questions. Make them specific and actionable."""

        user_prompt = f"""Analyze this workflow request:

"{user_input}"

Does this need clarification? What's missing or unclear?"""

        response = self.client.call_claude(
            system_prompt=system_prompt,
            user_message=user_prompt
        )
        
        # Extract JSON from response
        try:
            # Find JSON in response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            result = json.loads(json_str)
            return result
        except:
            # Fallback: assume no clarification needed
            return {
                'needs_clarification': False,
                'questions': [],
                'ambiguities': [],
                'confidence': 100
            }
    
    def refine_requirements(self, 
                          original_input: str, 
                          questions: List[str], 
                          answers: List[str]) -> str:
        """
        Refine requirements based on Q&A
        
        Returns:
            Enhanced requirement description
        """
        qa_pairs = '\n'.join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
        
        system_prompt = """You refine workflow requirements based on clarifying questions.

Take the original requirement + Q&A and create an enhanced, detailed requirement description."""

        user_prompt = f"""Original Requirement:
{original_input}

Clarifying Q&A:
{qa_pairs}

Create enhanced requirement description:"""

        response = self.client.call_claude(
            system_prompt=system_prompt,
            user_message=user_prompt
        )
        
        return response.strip()
