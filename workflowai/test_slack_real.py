"""Test real Slack integration"""
from integrations.slack_integration import SlackIntegration

print("🧪 Testing Slack Integration...\n")

# First, list available channels
print("📋 Step 1: Finding available channels...")
slack = SlackIntegration(use_mock=False)

try:
    result = slack.client.conversations_list(types="public_channel")
    channels = [ch['name'] for ch in result['channels'] if ch.get('is_member')]
    
    if channels:
        print(f"✅ Found {len(channels)} channels where bot is a member:")
        for ch in channels:
            print(f"   - #{ch}")
        
        # Use the first available channel
        test_channel = channels[0]
        print(f"\n📤 Step 2: Testing with #{test_channel}...\n")
        
        # Test simple message
        result = slack.send_message(
            channel=test_channel,
            text='🚀 WorkflowAI is now connected to Slack!'
        )
        print(result['message'])
        
        # Test rich message
        result = slack.send_rich_message(
            channel=test_channel,
            title='🎉 WorkflowAI Test',
            message='This is a *formatted* message with _rich_ ~text~',
            fields={
                'Status': '✅ Connected',
                'Integration': 'Slack API',
                'Mode': 'Production'
            }
        )
        print(result['message'])
        
        print(f"\n✅ Success! Check #{test_channel} in Slack!")
        
    else:
        print("❌ Bot is not a member of any channels yet!")
        print("\n💡 To fix this:")
        print("   1. Open Slack in your browser/app")
        print("   2. Go to #general (or any channel)")
        print("   3. Type: @WorkflowAI Bot")
        print("   4. Click to add the bot to the channel")
        print("   5. Run this test again")
        
except Exception as e:
    print(f"❌ Error: {e}")