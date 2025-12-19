# Pydantic AI E-commerce Support Agent

A demo project showcasing **Pydantic AI** with tool calling, **OpenRouter** as the LLM provider, and a minimal agentic workflow with state tracking.

## Features

- **Pydantic AI Agent** - AI agent with tool calling capabilities
- **OpenRouter Integration** - Uses OpenRouter as the LLM provider
- **Tool Calling** - Agent decides when to call tools based on context
- **State Tracking** - Maintains conversation state per user (in-memory)
- **FastAPI Backend** - RESTful API for chat interactions

## Project Structure

```
app/
├── __init__.py     # Package marker
├── main.py         # FastAPI app with /chat endpoint
├── agent.py        # Pydantic AI agent with tool calling
├── tools.py        # Tool functions (order status, returns)
├── state.py        # In-memory state management
└── config.py       # OpenRouter configuration
requirements.txt    # Dependencies
run.py              # Convenience runner
```

## Prerequisites

- Python 3.10+
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd pydantic-ai-agent-demo
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   .\venv\Scripts\activate.bat
   ```

   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file with your OpenRouter API key:**
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=openai/gpt-4o-mini
   ```

## Running the Application

**Option 1: Using uvicorn directly:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Option 2: Using the run script:**
```bash
python run.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
```
Returns server status.

### Chat
```
POST /chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "What is the status of my order ORD-12345?"
}
```

**Response:**
```json
{
  "reply": "Your order ORD-12345 is currently Out for Delivery..."
}
```

### Debug States
```
GET /debug/states
```
Returns all user states (for debugging).

## Interactive API Docs

Visit `http://localhost:8000/docs` for the Swagger UI where you can test the API interactively.

## Example Conversations

**1. Check order status:**
```json
{
  "user_id": "user123",
  "message": "What is the status of my order ORD-12345?"
}
```

**2. Request a return (uses remembered order ID):**
```json
{
  "user_id": "user123",
  "message": "I want to return my order"
}
```

**3. Ask a general question:**
```json
{
  "user_id": "user123",
  "message": "What is your return policy?"
}
```

## Available Tools

The agent has access to these tools:

| Tool | Description |
|------|-------------|
| `check_order_status` | Look up the status of an order by ID |
| `request_return` | Initiate a return request for an order |
| `get_previous_order_id` | Retrieve the last mentioned order ID from context |

## Configuration

Environment variables (set in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | (required) |
| `OPENROUTER_MODEL` | Model to use | `openai/gpt-4o-mini` |

## Notes

- This is a **demo project**, not production-ready
- State is stored **in-memory** and resets on server restart
- No authentication is implemented
- Tool responses are simulated (fake data)

## License

MIT

