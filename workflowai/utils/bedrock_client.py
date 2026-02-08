"""
AWS Bedrock Client Utility.
Provides interface for interacting with AWS Bedrock Claude models.
"""

import boto3
import json
import os
from typing import List, Dict, Optional
from botocore.exceptions import ClientError, NoCredentialsError

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class BedrockClient:
    """Client for interacting with AWS Bedrock Claude models."""
    
    def __init__(self, region_name: str = None):
        """
        Initialize Bedrock client.
        
        Args:
            region_name: AWS region for Bedrock service
            
        Raises:
            NoCredentialsError: If AWS credentials are not configured
        """
        # Try Streamlit secrets first, then environment variables
        aws_access_key = None
        aws_secret_key = None
        region = None
        
        if HAS_STREAMLIT:
            try:
                aws_access_key = st.secrets.get("AWS_ACCESS_KEY_ID")
                aws_secret_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
                region = st.secrets.get("AWS_DEFAULT_REGION", region_name or "us-east-1")
            except:
                pass
        
        # Fallback to environment variables
        if not aws_access_key:
            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            region = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        
        try:
            if aws_access_key and aws_secret_key:
                self.bedrock = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Use default credentials (IAM role, AWS CLI config)
                self.bedrock = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=region or "us-east-1"
                )
            self.model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
        except NoCredentialsError:
            raise NoCredentialsError(
                "AWS credentials not found. Configure credentials via IAM role, "
                "environment variables, or Streamlit secrets."
            )
    
    def call_claude(
        self, 
        system_prompt: str, 
        user_message: str, 
        temperature: float = 0.7
    ) -> str:
        """
        Invoke Claude model with a single user message.
        
        Args:
            system_prompt: System instructions for Claude
            user_message: User's message/prompt
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Text response from Claude
            
        Raises:
            ClientError: If Bedrock API call fails
        """
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "system": system_prompt,
                "temperature": temperature,
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response["body"].read())
            return result["content"][0]["text"]
            
        except ClientError as e:
            raise ClientError(
                {"Error": {"Code": e.response["Error"]["Code"], 
                          "Message": f"Bedrock API error: {e.response['Error']['Message']}"}},
                "invoke_model"
            )
    
    def call_claude_with_history(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """
        Invoke Claude model with conversation history.
        
        Args:
            system_prompt: System instructions for Claude
            messages: List of message dicts with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello"}, 
                              {"role": "assistant", "content": "Hi!"}]
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Text response from Claude
            
        Raises:
            ClientError: If Bedrock API call fails
        """
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "system": system_prompt,
                "temperature": temperature,
                "messages": messages
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response["body"].read())
            return result["content"][0]["text"]
            
        except ClientError as e:
            raise ClientError(
                {"Error": {"Code": e.response["Error"]["Code"],
                          "Message": f"Bedrock API error: {e.response['Error']['Message']}"}},
                "invoke_model"
            )


if __name__ == "__main__":
    print("Testing BedrockClient...")
    
    try:
        # Initialize client
        client = BedrockClient()
        print("✓ BedrockClient initialized successfully")
        
        # Test 1: Simple call
        print("\nTest 1: Simple greeting")
        response = client.call_claude(
            system_prompt="You are a helpful assistant.",
            user_message="Say hello in one sentence.",
            temperature=0.7
        )
        print(f"Response: {response}")
        
        # Test 2: Multi-turn conversation
        print("\nTest 2: Multi-turn conversation")
        messages = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "2+2 equals 4."},
            {"role": "user", "content": "Now multiply that by 3."}
        ]
        response = client.call_claude_with_history(
            system_prompt="You are a math tutor.",
            messages=messages,
            temperature=0.3
        )
        print(f"Response: {response}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        print("Make sure AWS credentials are configured correctly.")
