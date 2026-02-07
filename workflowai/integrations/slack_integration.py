"""Real Slack Integration for WorkflowAI"""
import os
from typing import Optional, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SlackIntegration:
    """Real Slack API integration"""
    
    def __init__(self, token: Optional[str] = None, use_mock: bool = False):
        """
        Initialize Slack client
        
        Args:
            token: Slack bot token (or set SLACK_BOT_TOKEN env var)
            use_mock: If True, use mock responses (for demo safety)
        """
        self.use_mock = use_mock
        
        if not use_mock:
            self.token = token or os.getenv('SLACK_BOT_TOKEN')
            if not self.token:
                raise ValueError("Slack token required. Set SLACK_BOT_TOKEN env var or pass token parameter.")
            self.client = WebClient(token=self.token)
        else:
            self.client = None
    
    def _get_channel_id(self, channel_name: str) -> Optional[str]:
        """Get channel ID from channel name"""
        try:
            # Remove # if present
            clean_name = channel_name.replace('#', '')
            
            # List all channels
            result = self.client.conversations_list(types="public_channel,private_channel")
            
            for channel in result['channels']:
                if channel['name'] == clean_name:
                    return channel['id']
            
            return None
        except SlackApiError:
            return None
    
    def send_message(self, channel: str, text: str, blocks: Optional[list] = None) -> Dict[str, Any]:
        """
        Send message to Slack channel
        
        Args:
            channel: Channel name (e.g., 'general' or '#general') or ID
            text: Message text
            blocks: Optional rich formatting blocks
            
        Returns:
            Response dict with status and message
        """
        if self.use_mock:
            return self._mock_send_message(channel, text)
        
        try:
            # Clean channel name
            clean_channel = channel.replace('#', '')
            
            # Try to get channel ID if it's a name
            if not clean_channel.startswith('C'):
                channel_id = self._get_channel_id(clean_channel)
                if channel_id:
                    clean_channel = channel_id
                else:
                    # Try using the name directly
                    clean_channel = f'#{clean_channel}'
            
            response = self.client.chat_postMessage(
                channel=clean_channel,
                text=text,
                blocks=blocks
            )
            
            return {
                'success': True,
                'message': f"✅ Message sent to {channel}",
                'timestamp': response['ts'],
                'channel': response['channel']
            }
            
        except SlackApiError as e:
            error_msg = e.response['error']
            
            # Provide helpful error messages
            if error_msg == 'channel_not_found':
                return {
                    'success': False,
                    'error': error_msg,
                    'message': f"❌ Channel '{channel}' not found. Try inviting the bot: In Slack, go to the channel and type '@WorkflowAI Bot'"
                }
            elif error_msg == 'not_in_channel':
                return {
                    'success': False,
                    'error': error_msg,
                    'message': f"❌ Bot not in channel '{channel}'. In Slack, type '@WorkflowAI Bot' in that channel to invite it."
                }
            else:
                return {
                    'success': False,
                    'error': error_msg,
                    'message': f"❌ Slack API error: {error_msg}"
                }
    
    def send_rich_message(self, channel: str, title: str, message: str, 
                         fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send formatted message with blocks
        
        Args:
            channel: Channel name or ID
            title: Message title
            message: Main message text
            fields: Optional key-value pairs to display
            
        Returns:
            Response dict
        """
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
        
        if fields:
            fields_text = "\n".join([f"*{k}:* {v}" for k, v in fields.items()])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": fields_text
                }
            })
        
        return self.send_message(channel, title, blocks=blocks)
    
    # Mock methods for fallback
    def _mock_send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """Mock message sending"""
        return {
            'success': True,
            'message': f"🔷 [MOCK] Message sent to {channel}: {text[:50]}...",
            'mock': True
        }


# Convenience function for workflows
def send_slack_notification(channel: str, message: str, use_mock: bool = False) -> str:
    """
    Simple helper for sending Slack notifications
    
    Usage in generated code:
        from integrations.slack_integration import send_slack_notification
        result = send_slack_notification('general', 'Hello team!')
        print(result)
    """
    slack = SlackIntegration(use_mock=use_mock)
    result = slack.send_message(channel, message)
    return result['message']