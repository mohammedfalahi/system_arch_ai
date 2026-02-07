# 🤖 WorkflowAI - AI-Powered Business Workflow Generator

An intelligent system that converts natural language business requirements into production-ready Python workflow code. Built for non-technical users who need to automate repetitive business processes without coding expertise.

![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 Problem Statement

Business teams waste 15+ hours per week on repetitive tasks but can't automate them because they lack coding skills. Existing automation tools require technical expertise or are too rigid for custom business needs.

## ✨ Features

### **Three-Agent AI Architecture**
- **🧠 Workflow Reasoner (AWS Bedrock Claude)**: Analyzes business requirements and designs structured workflow plans
- **💻 Code Generator (AWS Bedrock Claude)**: Generates clean, executable Python code from workflow plans
- **⚡ Executor Agent**: Safely runs generated workflows and captures results

### **Self-Debugging Capability**
- Automatically detects execution errors
- Analyzes what went wrong using AI
- Regenerates fixed code
- Re-executes until successful

### **Natural Language Interface**
- Describe your process in plain English
- No technical knowledge required
- Conversational workflow generation
- Real-time code generation and execution

### **Pre-built Templates**
- ✅ Employee Onboarding Automation
- 🎫 Customer Support Ticket Routing
- 💰 Invoice Processing Workflow
- Export and customize any generated workflow

## 🚀 How It Works

```
User describes process: "I need to automate employee onboarding"
                    ↓
Workflow Reasoner analyzes and creates structured plan
                    ↓
Code Generator produces executable Python code
                    ↓
Executor runs the workflow and shows results
                    ↓
If errors occur → Self-debugger fixes and re-runs automatically
```

## 📋 Requirements

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured (IAM role, environment variables, or AWS CLI)

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd workflowai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS credentials

**Option A: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

**Option B: AWS CLI**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your region (e.g., us-east-1)
```

**Option C: IAM Role (Recommended for EC2/ECS)**
- Attach an IAM role with Bedrock permissions to your instance

### 4. Enable Bedrock Access
- Go to AWS Bedrock console
- Enable Claude 3.5 Sonnet v2 model
- Request model access if not already enabled

## 🎮 Usage

### Start the application
```bash
streamlit run app.py
```

### Access the web interface
Open your browser to `http://localhost:8501`

### Generate a workflow
1. Describe your business process in the text input
2. Click "Generate Workflow"
3. View the workflow plan, generated code, and execution results
4. Export the code if needed

## 💡 Example Prompts

### Employee Onboarding
```
I need to automate employee onboarding. Send a welcome email, create their
Slack account, assign them a mentor, and schedule their first week of meetings.
```

### Customer Support Automation
```
Automate customer support ticket routing. Read new tickets, categorize them
by urgency, assign to the right team member, and send notifications.
```

### Invoice Processing
```
Create a workflow to process invoices. Extract data from PDFs, validate amounts,
check approval rules, send for approval, and update the accounting system.
```

## 🏗️ Architecture

```
workflowai/
├── app.py                          # Main Streamlit application
├── agents/
│   ├── workflow_reasoner.py        # Analyzes requirements, creates plans
│   ├── code_generator.py           # Generates Python code
│   ├── executor.py                 # Executes workflows safely
│   └── debugger.py                 # Self-debugging capability
├── templates/
│   ├── employee_onboarding.py      # Pre-built template
│   ├── customer_support.py         # Pre-built template
│   └── invoice_processing.py       # Pre-built template
├── utils/
│   └── bedrock_client.py           # AWS Bedrock integration
└── requirements.txt
```

## 🔒 Security

- ✅ No API keys stored in code (uses AWS IAM credentials)
- ✅ Sandboxed code execution (restricted globals, no file system access)
- ✅ Input validation to prevent code injection
- ✅ All external integrations are mocked (no real API calls in demo)

## 💰 Cost Estimation

- AWS Bedrock Claude 3.5 Sonnet pricing: ~$3 per 1M input tokens
- Typical workflow generation: 2,000-5,000 tokens
- Estimated cost per workflow: $0.01-$0.02
- Self-debugging adds minimal additional cost

## 📊 Business Impact

- **Time Saved**: 15 hours/week per automated process
- **ROI**: For a 50-person company automating 5 processes
  - Weekly time savings: 75 hours
  - Annual cost savings: ~$150,000 (at $40/hour)
- **Scalability**: One workflow → reusable template for entire organization

## 🎯 Use Cases

- **HR**: Employee onboarding, offboarding, performance reviews
- **Customer Support**: Ticket routing, response automation, escalation
- **Finance**: Invoice processing, expense approvals, reporting
- **Sales**: Lead qualification, follow-up automation, data entry
- **Operations**: Inventory updates, order processing, scheduling

## 🚧 Limitations

- Generated code uses mock integrations (not connected to real services)
- Execution timeout: 30 seconds per workflow
- Best for workflows with 3-10 steps
- Requires AWS Bedrock access in supported regions

## 🔮 Future Enhancements

- [ ] Real integration connectors (Gmail, Slack, Salesforce, etc.)
- [ ] Workflow scheduling and monitoring
- [ ] Multi-user collaboration
- [ ] Workflow marketplace and sharing
- [ ] Visual workflow builder
- [ ] Enterprise SSO integration

## 🧪 Testing

### Test Individual Components

```bash
# Test Bedrock Client
python3 utils/bedrock_client.py

# Test Workflow Reasoner
python3 agents/workflow_reasoner.py

# Test Code Generator
python3 agents/code_generator.py

# Test Executor
python3 agents/executor.py

# Test Debugger
python3 agents/debugger.py
```

### Test Templates

```bash
# Test Employee Onboarding
python3 templates/employee_onboarding.py

# Test Customer Support
python3 templates/customer_support.py

# Test Invoice Processing
python3 templates/invoice_processing.py
```

## 📄 License

MIT License - feel free to use and modify for your needs

## 🙏 Acknowledgments

Built with:
- AWS Bedrock (Claude 3.5 Sonnet v2)
- Streamlit
- Python

---

**🚀 Ready to automate your business workflows? Start the app and describe your process!**

For questions or issues, please open a GitHub issue.
