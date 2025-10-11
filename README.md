# Lead Follow-up AI Agent

An AI-powered lead analysis and follow-up recommendation system that integrates with Zoho CRM and uses OpenAI GPT-4o to determine the best follow-up actions for sales agents.

## 🚀 Features

- **Intelligent Lead Analysis**: Uses OpenAI GPT-4o to analyze lead data and determine optimal follow-up strategies
- **Sales Rep Agent**: Advanced conversational AI that plans next actions and responds to customer messages
- **Multi-Channel Support**: Recommends follow-up channels (Email, Phone, WhatsApp, Instagram DM, LinkedIn)
- **Priority Scoring**: Assigns priority scores (0-10) based on lead characteristics
- **Smart Routing**: Determines whether leads should go directly to agents or be queued
- **Mock Mode**: Test the system without OpenAI API calls using intelligent mock responses
- **Flexible Input**: Multiple API endpoints supporting different input formats for easy integration
- **Robust Error Handling**: Fallback mechanisms ensure the system always returns valid responses
- **RESTful API**: Clean FastAPI endpoints for easy integration with n8n workflows

## 🏗️ Architecture

```
bcs-agents/
├── app/
│   └── main.py           # FastAPI application entry point
├── src/
│   ├── api/
│   │   └── agent.py      # API endpoints for lead analysis and sales rep actions
│   └── services/
│       └── llm_service.py # OpenAI LLM integration and mock responses
├── tests/
│   └── test_parser.py    # Unit tests for parser validation
├── start_server.py       # Server startup script
├── test_api.py          # API testing script
├── demo.py              # Demo scenarios script
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── env.example         # Environment variables template
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **AI**: OpenAI GPT-4o API with mock mode support
- **Testing**: pytest with comprehensive test coverage
- **Development**: Modern Python tooling (ruff, black, mypy)
- **Deployment**: Cloud-ready (Render, Railway, AWS Lambda)

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (optional - mock mode available for testing)
- n8n workflow (for sending lead data)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd bcs-agents
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your OpenAI API key:

```bash
OPENAI_API_KEY=yosk-proj-Kx6dpUpVQi04f6uq5L7ENDdP0g1SoMQLYxDuAhm7B1vP8HNd12b1F4hu-GD6MesDPvDpRASq63T3BlbkFJ8Tef5TiwDajvfOm0q-WDlbCsDJsIgsKmdTo5vBAciRBQ3g02GAZmoGplzHph00tIP0ysbzU9AA
```

### 3. Run the Application

```bash
python start_server.py
```

The API will be available at `http://localhost:8000`

### 4. Test the API

Visit `http://localhost:8000/docs` for interactive API documentation.

You can also run the test suite:
```bash
python test_api.py
```

Or try the demo scenarios:
```bash
python demo.py
```

## 📡 API Endpoints

### POST `/api/v1/lead` (Legacy)

Analyze lead data and get follow-up recommendations (backwards compatibility).

**Request Body:**
```json
{
  "zoho_id": "LEAD_123",
  "name": "John Doe",
  "email": "john@acme.com",
  "phone": "+1234567890",
  "source": "Website",
  "interest": "Cloud solutions",
  "due_date": "2024-03-15",
  "notes": "High potential enterprise client",
  "city": "New York",
  "country": "USA"
}
```

**Response:**
```json
{
  "zoho_id": "LEAD_123",
  "channel": "Email",
  "priority": 8,
  "to_agent": true,
  "notes": "High-value enterprise prospect, interested in cloud solutions, follow up via email today.",
  "message": "Draft message content",
  "intent": "general",
  "score": 80
}
```

### POST `/api/v1/next_action` (Sales Rep Agent)

Get the next action for a sales representative based on lead and conversation state.

**Request Body:**
```json
{
  "lead": {
    "zoho_id": "LEAD_123",
    "name": "John Doe",
    "email": "john@acme.com",
    "phone": "+1234567890",
    "city": "New York",
    "country": "USA",
    "interests": ["Cloud solutions", "AI"]
  },
  "state": {
    "intent": "general",
    "preferred_channel": "Email",
    "history": [
      {
        "role": "customer",
        "text": "I'm interested in your cloud solutions",
        "channel": "Website",
        "ts": "2024-01-15T10:30:00Z"
      }
    ],
    "last_outcome": null,
    "next_follow_up_at": null
  }
}
```

**Response:**
```json
{
  "plan_id": "uuid-here",
  "action": "send_message",
  "channel": "Email",
  "message": {
    "subject": "Quick follow-up",
    "body": "Hi John, thanks for your interest in cloud solutions...",
    "whatsapp_text": "Hi John! Thanks for asking about cloud solutions..."
  },
  "metadata": {
    "priority": 8,
    "to_agent": true,
    "ai_notes": "High-value prospect, ready for personalized outreach",
    "suggested_followup_in_hours": 48
  },
  "log": "Generated personalized email for cloud solutions inquiry",
  "store": {
    "decision_channel": "Email",
    "decision_priority": 8,
    "ai_notes": "High-value prospect, ready for personalized outreach",
    "zoho_id": "LEAD_123",
    "name": "John Doe",
    "email": "john@acme.com"
  }
}
```

### POST `/api/v1/respond` (Sales Rep Agent)

Process incoming customer responses and determine next actions.

**Request Body:**
```json
{
  "plan_id": "uuid-here",
  "zoho_id": "LEAD_123",
  "incoming_text": "Yes, I'd like to see pricing for the enterprise plan",
  "channel": "Email",
  "timestamp": "2024-01-15T14:30:00Z",
  "state": {
    "intent": "general",
    "preferred_channel": "Email"
  }
}
```

### POST `/api/v1/next_action_flex` (Flexible Input)

Flexible endpoint that accepts various input formats for easy integration.

**Request Body:** (Flexible format - see API docs for details)

### GET `/api/v1/health`

Health check endpoint to verify system status.

### GET `/`

Root endpoint with API information.

## 🎯 Key Features

### Sales Rep Agent
The system includes an advanced conversational AI agent that can:
- Plan next actions based on lead data and conversation history
- Generate personalized messages for different channels
- Process incoming customer responses and determine follow-up actions
- Maintain conversation context and state across interactions

### Mock Mode
Test the system without OpenAI API calls by setting `MOCK_LLM=true` in your environment:
- Intelligent mock responses that respect upstream signals
- Channel selection based on lead data and preferences
- Priority scoring with business logic
- Personalized message generation

### Flexible Integration
Multiple API endpoints support different integration patterns:
- **Legacy endpoint** (`/lead`) for backwards compatibility
- **Sales rep endpoints** (`/next_action`, `/respond`) for conversational AI
- **Flexible endpoint** (`/next_action_flex`) for various input formats

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Application settings
APP_NAME=convo-agent
PORT=8001
MOCK_LLM=true  # Set to false for OpenAI API calls

# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
LLM_MODEL=gpt-4o-mini

# Brand and Knowledge Packs
BRAND_PACK_URL=https://bcs-packs.pages.dev/brand.json
KNOWLEDGE_PACK_URL=https://bcs-packs.pages.dev/knowledge.json
PACK_CACHE_TTL=600

# Sign-off Configuration
SIGNOFF_NAME=Sabrina
SIGNOFF_EMAIL="Kind regards,\nSabrina\nThe Baby Cot Shop"
SIGNOFF_WA=Sabrina

# Storage Backend
STORE_BACKEND=memory
REDIS_URL=redis://localhost:6379/0
```

### Mock Mode

Enable mock mode for testing without OpenAI API calls:

```bash
MOCK_LLM=true
```

Mock responses include:
- Intelligent channel selection based on lead data
- Priority scoring with business logic
- Personalized message generation
- Respect for upstream signals from n8n

### Agent Handoff Threshold

Control when leads are routed to agents:

```bash
AGENT_HANDOFF_THRESHOLD=6  # Default: 6 (0-10 scale)
```

## 🧪 Testing

### Unit Tests

Run the test suite:

```bash
pytest tests/
```

Run specific test file:

```bash
pytest tests/test_parser.py -v
```

### API Testing

Test the API endpoints:

```bash
python test_api.py
```

### Demo Scenarios

Try the demo with various lead scenarios:

```bash
python demo.py
```


## 📊 Data Storage

The system uses in-memory storage by default, with optional Redis support for production deployments. All decisions and conversation state are maintained in memory for fast access and can be persisted to external systems via the API responses.

## 🔒 Security Considerations

- Store API keys in environment variables
- Configure CORS appropriately for production
- Implement rate limiting for production use

## 🚀 Deployment

The application is cloud-ready and can be deployed to any platform that supports Python applications (Render, Railway, AWS Lambda, etc.). Set the required environment variables and deploy using your preferred platform.


## 🤝 Integration with n8n

### n8n Workflow Example

1. **Trigger**: Zoho CRM webhook or scheduled trigger
2. **HTTP Request**: Send lead data to your API endpoint
3. **Data Processing**: Handle the AI response
4. **Actions**: Route to agents, update CRM, send notifications

### Sample n8n HTTP Request Node

```javascript
{
  "method": "POST",
  "url": "https://your-api.railway.app/api/v1/next_action",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "lead": {
      "zoho_id": "{{$json.Lead_ID}}",
      "name": "{{$json.Contact_Name}}",
      "email": "{{$json.Email}}",
      "phone": "{{$json.Phone}}",
      "city": "{{$json.City}}",
      "country": "{{$json.Country}}",
      "interests": "{{$json.Interests}}"
    },
    "state": {
      "intent": "general",
      "preferred_channel": "{{$json.Preferred_Channel}}",
      "history": []
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure `OPENAI_API_KEY` is set in `.env` or use mock mode with `MOCK_LLM=true`
2. **Import Errors**: Ensure you're in the correct directory and virtual environment
3. **Port Already in Use**: Change the port in `.env` or stop other services using port 8000
4. **Mock Mode Issues**: Check that `MOCK_LLM=true` is set for testing without OpenAI API

### Testing Without OpenAI

Use mock mode for development and testing:

```bash
MOCK_LLM=true
python start_server.py
```

## 📝 License

This project is licensed under the MIT License.

---

**Built with ❤️ for sales teams who want to work smarter, not harder.**
