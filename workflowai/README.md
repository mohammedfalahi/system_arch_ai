# 🤖 WorkflowAI - AI-Powered Business Workflow Generator

An intelligent system that converts natural language business requirements into production-ready Python workflow code using **AWS Bedrock Claude Opus 4.5**. Built for non-technical users who need to automate repetitive business processes without coding expertise.

![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![Claude Opus 4.5](https://img.shields.io/badge/Claude-Opus%204.5-purple)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 Problem Statement

Business teams waste 15+ hours per week on repetitive tasks but can't automate them because they lack coding skills. Existing automation tools require technical expertise or are too rigid for custom business needs.

## ✨ Key Features

### **Four-Agent AI Architecture (Powered by Claude Opus 4.5)**
- **🧠 Workflow Reasoner Agent**: Analyzes business requirements and designs structured workflow plans
- **💻 Code Generator Agent**: Generates clean, executable Python code with real integrations
- **⚡ Executor Agent**: Safely runs generated workflows in sandboxed environment
- **🔧 Self-Debugger Agent**: Automatically detects errors, analyzes root causes, and regenerates fixed code

### **Production-Ready Integrations**
- **Slack Integration**: Real Slack API integration for team notifications
- **Email Integration**: Real SMTP email sending (Gmail, Office365, custom SMTP)
- **Sandboxed Execution**: Safe code execution with restricted globals and timeout enforcement

### **Self-Debugging Capability**
- Automatically detects execution errors
- AI-powered root cause analysis using Claude Opus 4.5
- Regenerates fixed code automatically
- Re-executes until successful (up to 2 attempts)
- Shows before/after code comparison

### **Natural Language Interface**
- Describe your process in plain English
- No technical knowledge required
- Conversational workflow generation
- Real-time code generation and execution
- Export workflows as Python files or complete packages

### **Pre-built Templates**
- ✅ Employee Onboarding Automation
- 🎫 Customer Support Ticket Routing
- 💰 Invoice Processing Workflow
- Export and customize any generated workflow

## 🏗️ Architecture

### Multi-Agent Workflow
```
User Input (Natural Language)
    ↓
Streamlit UI (app.py)
    ↓
Workflow Reasoner Agent → AWS Bedrock (Claude Opus 4.5)
    ↓
Structured Workflow Plan (JSON)
    ↓
Code Generator Agent → AWS Bedrock (Claude Opus 4.5)
    ↓
Python Code with Real Integrations
    ↓
Executor Agent (Sandboxed Environment)
    ↓
Success? → Display Results
    ↓ (if error)
Debugger Agent → AWS Bedrock (Claude Opus 4.5)
    ↓
Fixed Code → Re-execute (max 2 attempts)
```

### Agent Details

#### 1. Workflow Reasoner Agent (`agents/workflow_reasoner.py`)
- **Purpose**: Analyzes natural language requirements
- **Output**: Structured JSON workflow plan with steps, inputs, outputs
- **Model**: Claude Opus 4.5 (`us.anthropic.claude-opus-4-5-20250514-v1:0`)
- **Temperature**: 0.5 (balanced creativity and consistency)

#### 2. Code Generator Agent (`agents/code_generator.py`)
- **Purpose**: Converts workflow plans to executable Python code
- **Features**: 
  - Uses real integration classes (Slack, Email)
  - Extracts actual values from user input (no placeholders)
  - Includes error handling and progress tracking
  - Generates self-contained, executable code
- **Model**: Claude Opus 4.5
- **Temperature**: 0.3 (high consistency)

#### 3. Executor Agent (`agents/executor.py`)
- **Purpose**: Safely executes generated code
- **Security**:
  - Restricted global namespace (no file system access)
  - Limited built-in functions
  - 30-second timeout enforcement
  - Input validation to prevent injection
- **Output**: Captures stdout, stderr, execution time, and errors

#### 4. Self-Debugger Agent (`agents/debugger.py`)
- **Purpose**: Automatically fixes code errors
- **Process**:
  1. Analyzes error messages and stack traces
  2. Identifies root cause with confidence level
  3. Suggests fixes with rationale
  4. Regenerates corrected code
  5. Re-executes automatically
- **Model**: Claude Opus 4.5
- **Max Attempts**: 2 automatic debugging cycles

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Interactive web UI framework
- **AWS Bedrock**: AI model hosting and inference
- **Claude Opus 4.5**: Advanced reasoning and code generation

### AWS Services
- **AWS Bedrock Runtime**: Model invocation API
- **Model**: `us.anthropic.claude-opus-4-5-20250514-v1:0`
- **Region**: us-east-1 (configurable)
- **Authentication**: IAM credentials, environment variables, or AWS CLI

### Python Dependencies
```
streamlit          # Web UI framework
boto3              # AWS SDK for Bedrock API
python-dotenv      # Environment variable management
slack-sdk          # Slack API client (for real integration)
```

### Integrations
- **Slack API**: Real-time team notifications via Slack SDK
- **SMTP Email**: Production email sending (Gmail, Office365, custom SMTP)
- **In-memory Data**: Dict/list for workflow data storage

## 📋 Requirements

- Python 3.8 or higher
- AWS Account with Bedrock access
- Claude Opus 4.5 model enabled in AWS Bedrock
- AWS credentials configured (IAM role, environment variables, or AWS CLI)
- (Optional) Slack Bot Token for Slack integration
- (Optional) SMTP credentials for email integration

## 🚀 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/workflowai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

**Option A: AWS CLI**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your region (e.g., us-east-1)
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

**Option C: IAM Role (Recommended for EC2/ECS)**
- Attach an IAM role with Bedrock permissions to your instance

### 4. Enable Claude Opus 4.5 in AWS Bedrock
1. Open AWS Bedrock console
2. Navigate to Model access
3. Request access to Claude Opus 4.5 (`us.anthropic.claude-opus-4-5-20250514-v1:0`)
4. Wait for approval (usually instant)

### 5. (Optional) Configure Integrations
Create a `.env` file in the `workflowai` directory:

```bash
# Slack Integration (optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

# Email Integration (optional)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
```

### 6. Run the Application
```bash
streamlit run app.py
```

Access the web interface at `http://localhost:8501`

## 🎮 Usage

### Basic Workflow Generation

1. **Start the application**: `streamlit run app.py`
2. **Describe your workflow** in plain English in the text area
3. **Click "Generate Workflow"**
4. **View results** in four tabs:
   - 📋 Workflow Plan: Structured breakdown of steps
   - 💻 Generated Code: Executable Python code
   - ⚡ Execution Results: Output and any errors
   - 📅 History: Previous workflows

### Example Prompts

#### Employee Onboarding
```
I need to automate employee onboarding. Send a welcome email to 
mohammed.falahi.nt@gmail.com, post a message in the #new-channel 
Slack channel announcing John Smith is joining on Monday, and 
send an HR notification to dailyusegadjects.store@gmail.com.
```

#### Customer Support Automation
```
Automate customer support ticket routing. Read new tickets, 
categorize them by urgency (high/medium/low), assign to the 
right team member based on category, and send Slack notifications 
to the assigned person in #support-team channel.
```

#### Invoice Processing
```
Create a workflow to process invoices. Extract data from invoice 
records, validate amounts are under $10,000, check if manager 
approval is needed for amounts over $5,000, send approval emails 
to manager@company.com, and update the accounting system.
```

### Using Pre-built Templates

1. Open the sidebar
2. Select a template from the dropdown:
   - Employee Onboarding
   - Customer Support Ticket Routing
   - Invoice Processing
3. Click "Generate Workflow"
4. Customize the generated code as needed

### Exporting Workflows

- **Download Code**: Click "📥 Download" to save Python file
- **Export Package**: Click "📦 Export All" to download:
  - `generated_workflow.py` - Executable code
  - `workflow_plan.json` - Structured plan
  - `README.txt` - Documentation and usage instructions

## 🔒 Security

### Code Execution Safety
- **Sandboxed Environment**: Restricted global namespace
- **No File System Access**: Cannot read/write files
- **Limited Built-ins**: Only safe functions available
- **Timeout Enforcement**: 30-second execution limit
- **Input Validation**: Syntax checking before execution

### Credential Management
- **No Hardcoded Secrets**: All credentials via environment variables
- **AWS IAM**: Uses IAM roles and credentials
- **Environment Variables**: Sensitive data in `.env` file
- **Integration Flags**: `use_mock=False` for production APIs

### Integration Security
- **Slack**: OAuth token-based authentication
- **Email**: SMTP with TLS encryption
- **AWS**: IAM credential-based access

## 💰 Cost Estimation

### AWS Bedrock Pricing (Claude Opus 4.5)
- **Input tokens**: ~$15 per 1M tokens
- **Output tokens**: ~$75 per 1M tokens
- **Typical workflow generation**: 3,000-6,000 tokens total
- **Estimated cost per workflow**: $0.15-$0.30
- **Self-debugging**: Adds $0.10-$0.20 per attempt

### Monthly Cost Examples
- **10 workflows/day**: ~$45-90/month
- **50 workflows/day**: ~$225-450/month
- **100 workflows/day**: ~$450-900/month

### ROI Calculation
For a 50-person company automating 5 processes:
- **Time saved**: 75 hours/week
- **Annual cost savings**: ~$150,000 (at $40/hour)
- **AWS Bedrock cost**: ~$1,350/year (assuming 15 workflows/day)
- **Net savings**: ~$148,650/year

## 📊 Features Breakdown

### Workflow Reasoning
- Natural language understanding
- Step extraction and sequencing
- Input/output identification
- Complexity estimation
- Integration detection

### Code Generation
- Production-ready Python code
- Real integration usage (Slack, Email)
- Actual value extraction from user input
- Error handling and logging
- Progress tracking with print statements
- Self-contained and executable

### Execution & Debugging
- Safe sandboxed execution
- Real-time output capture
- Automatic error detection
- AI-powered error analysis
- Code regeneration with fixes
- Before/after comparison
- Manual editing fallback

### User Interface
- Clean, intuitive Streamlit UI
- Real-time progress indicators
- Tabbed results view
- Code syntax highlighting
- Export functionality
- Analytics dashboard
- Conversation history

## 🎯 Use Cases

### Human Resources
- Employee onboarding/offboarding
- Performance review scheduling
- Benefits enrollment automation
- Training assignment workflows

### Customer Support
- Ticket routing and assignment
- Response automation
- Escalation workflows
- Customer feedback processing

### Finance & Accounting
- Invoice processing and approval
- Expense report validation
- Payment scheduling
- Financial report generation

### Sales & Marketing
- Lead qualification
- Follow-up automation
- Campaign execution
- Data entry and CRM updates

### Operations
- Inventory updates
- Order processing
- Scheduling automation
- Report distribution

## 📁 Project Structure

```
workflowai/
├── agents/
│   ├── workflow_reasoner.py    # Analyzes requirements, creates plans
│   ├── code_generator.py       # Generates Python code from plans
│   ├── executor.py             # Executes workflows safely
│   └── debugger.py             # Self-debugging capability
├── integrations/
│   ├── email_integration.py    # Real SMTP email integration
│   └── slack_integration.py    # Real Slack API integration
├── templates/
│   ├── employee_onboarding.py  # Pre-built HR template
│   ├── customer_support.py     # Pre-built support template
│   └── invoice_processing.py   # Pre-built finance template
├── utils/
│   └── bedrock_client.py       # AWS Bedrock client wrapper
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md                   # This file
```

## 🧪 Testing

### Test Individual Components

```bash
# Test Bedrock Client
python utils/bedrock_client.py

# Test Workflow Reasoner
python agents/workflow_reasoner.py

# Test Code Generator
python agents/code_generator.py

# Test Executor
python agents/executor.py

# Test Debugger
python agents/debugger.py
```

### Test Integrations

```bash
# Test Slack Integration
python test_slack_real.py

# Test Email Integration
python integrations/email_integration.py
```

### Test Templates

```bash
# Test Employee Onboarding
python templates/employee_onboarding.py

# Test Customer Support
python templates/customer_support.py

# Test Invoice Processing
python templates/invoice_processing.py
```

## 🚧 Limitations

- **Execution timeout**: 30 seconds per workflow
- **Best for**: 3-10 step workflows
- **Complexity**: Medium complexity workflows work best
- **AWS Region**: Requires Bedrock access in supported regions
- **Model Access**: Requires Claude Opus 4.5 enabled in Bedrock

## 🔮 Future Enhancements

- [ ] Additional integration connectors (Salesforce, Jira, Google Workspace)
- [ ] Workflow scheduling and monitoring
- [ ] Multi-user collaboration
- [ ] Workflow marketplace and sharing
- [ ] Visual workflow builder (drag-and-drop)
- [ ] Enterprise SSO integration
- [ ] Workflow versioning and rollback
- [ ] Performance metrics and optimization
- [ ] Custom integration builder
- [ ] API endpoint for programmatic access

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- New integration connectors
- Pre-built workflow templates
- UI/UX improvements
- Documentation enhancements
- Bug fixes and optimizations

## 📄 License

MIT License - feel free to use and modify for your needs.

## 🙏 Acknowledgments

Built with:
- **AWS Bedrock** - Claude Opus 4.5 model hosting
- **Anthropic Claude Opus 4.5** - Advanced AI reasoning and code generation
- **Streamlit** - Interactive web application framework
- **Python** - Core programming language
- **Slack SDK** - Real Slack integration
- **SMTP** - Email delivery

---

**Powered by Claude Opus 4.5 on AWS Bedrock** | **Multi-Agent AI Architecture** | **Production-Ready Integrations**

🚀 **Ready to automate your business workflows? Start the app and describe your process!**

For questions or issues, please open a GitHub issue.
