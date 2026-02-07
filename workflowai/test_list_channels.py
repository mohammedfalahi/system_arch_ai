"""List all Slack channels to find the right one"""
from integrations.slack_integration import SlackIntegration

print("📋 Listing all Slack channels...\n")

slack = SlackIntegration(use_mock=False)

try:
    # List all channels
    result = slack.client.conversations_list(types="public_channel,private_channel")
    
    print("Available channels:")
    print("=" * 50)
    
    for channel in result['channels']:
        member_status = "✅ Bot is member" if channel.get('is_member') else "❌ Bot NOT member"
        print(f"#{channel['name']:<20} | {member_status}")
        print(f"  ID: {channel['id']}")
    
    print("=" * 50)
    print("\n💡 To invite bot to a channel:")
    print("   1. Open the channel in Slack")
    print("   2. Type: @WorkflowAI Bot")
    print("   3. Click to add the bot")
    
except Exception as e:
    print(f"❌ Error: {e}")
