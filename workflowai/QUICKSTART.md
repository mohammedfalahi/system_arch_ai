# 🚀 Quick Start Guide - WorkflowAI

Get WorkflowAI up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web UI framework
- `boto3` - AWS SDK for Python
- `python-dotenv` - Environment variable management

### 2. Configure AWS Credentials

Choose one method:

**Method A: Environment Variables (Quick)**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

**Method B: AWS CLI (Recommended)**
```bash
aws configure
```

**Method C: IAM Role (Production)**
- Attach IAM role with Bedrock permissions to your EC2/ECS instance

### 3. Verify AWS Bedrock Access

```bash
# Test the Bedrock client
python3 utils/bedrock_client.py
```

Expected output:
```
Testing BedrockClient...
✓ BedrockClient initialized successfully

Test 1: Simple greeting
Response: Hello there, it's great to meet you!

✅ All tests passed!
```

### 4. Launch the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Workflow

### Try the Employee Onboarding Example

1. Click **"Example 1"** button in the app
2. Click **"🚀 Generate Workflow"**
3. Watch the AI agents work:
   - 🧠 Workflow Reasoner analyzes requirements
   - 💻 Code Generator creates Python code
   - ⚡ Executor runs the workflow
4. View results in the tabs:
   - **Workflow Plan** - Structured breakdown
   - **Generated Code** - Python code with syntax highlighting
   - **Execution Results** - Output and logs

### Create Your Own Workflow

1. Clear the text area
2. Describe your process in plain English:
   ```
   I need to automate weekly report generation. 
   Collect data from database, create charts, 
   generate PDF report, and email to stakeholders.
   ```
3. Click **"🚀 Generate Workflow"**
4. Download the generated code with **"📥 Download"** button

## Testing Individual Components

### Test All Agents

```bash
# Workflow Reasoner
python3 agents/workflow_reasoner.py

# Code Generator
python3 agents/code_generator.py

# Executor
python3 agents/executor.py

# Debugger (Self-healing)
python3 agents/debugger.py
```

### Test Pre-built Templates

```bash
# Employee Onboarding
python3 templates/employee_onboarding.py

# Customer Support
python3 templates/customer_support.py

# Invoice Processing
python3 templates/invoice_processing.py
```

## Troubleshooting

### Issue: "AWS Bedrock Not Connected"

**Solution:**
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify Bedrock access in AWS Console
3. Ensure Claude 3.5 Sonnet v2 is enabled
4. Check region is `us-east-1` or supported region

### Issue: "Model not found" error

**Solution:**
1. Go to AWS Bedrock Console
2. Navigate to "Model access"
3. Request access to Claude 3.5 Sonnet v2
4. Wait for approval (usually instant)

### Issue: Code execution fails

**Solution:**
- The self-debugger should automatically fix it
- If not, try simplifying your workflow description
- Check the error details in "Execution Results" tab

### Issue: Streamlit won't start

**Solution:**
```bash
# Kill existing processes
pkill -f streamlit

# Try different port
streamlit run app.py --server.port 8502
```

## Next Steps

1. **Explore Templates** - Try all 3 pre-built templates
2. **Create Custom Workflows** - Describe your own processes
3. **Export Code** - Download and customize generated code
4. **Share** - Export workflows for your team

## Tips for Best Results

✅ **Be Specific** - Include details about steps and integrations
✅ **Use Examples** - "Send email to X" instead of "notify user"
✅ **List Steps** - Break down complex processes
✅ **Mention Tools** - Specify Slack, email, database, etc.

❌ **Avoid Vague** - "Do some processing" is too generic
❌ **Too Complex** - Keep workflows to 3-10 steps
❌ **Real APIs** - Generated code uses mocks (for demo)

## Example Prompts That Work Well

```
✅ "Automate new hire onboarding: send welcome email, 
   create Slack account, assign mentor, schedule meetings"

✅ "Process support tickets: fetch from queue, categorize 
   by urgency, assign to team, send notifications"

✅ "Handle invoices: validate amounts, check approval rules, 
   send to manager if over $5000, update accounting system"
```

## Support

- 📖 Full documentation in `README.md`
- 🐛 Report issues on GitHub
- 💬 Questions? Open a discussion

---

**🎉 You're ready to automate! Start describing your workflows.**
