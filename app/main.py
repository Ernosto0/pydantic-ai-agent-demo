"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent import process_message
from app.state import get_user_state, get_all_states

# Get the path to static files
STATIC_DIR = Path(__file__).parent.parent / "static"


# Request/Response models
class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    
    user_id: str
    message: str


class ChatResponse(BaseModel):
    """Response body for the chat endpoint."""
    
    reply: str


class HealthResponse(BaseModel):
    """Response body for health check."""
    
    status: str
    message: str


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("🛍️ E-commerce Support Agent is starting...")
    print("📱 Chat UI available at http://localhost:8000")
    print("🔧 API endpoint: POST /chat")
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="E-commerce Support Agent",
    description="A demo AI agent for e-commerce customer support using Pydantic AI",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_chat_ui():
    """Serve the chat UI."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        message="E-commerce Support Agent is running",
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message from a user.
    
    The agent will:
    - Understand the user's intent
    - Call tools if needed (order status, returns)
    - Maintain state across the conversation
    """
    try:
        # Get or create user state
        user_state = get_user_state(request.user_id)
        
        # Process the message through the agent
        reply = await process_message(user_state, request.message)
        
        return ChatResponse(reply=reply)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}",
        )


@app.get("/debug/states")
async def debug_states():
    """Debug endpoint to view all user states."""
    states = get_all_states()
    return {
        user_id: {
            "last_intent": state.last_intent,
            "last_order_id": state.last_order_id,
            "message_count": state.message_count,
        }
        for user_id, state in states.items()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


