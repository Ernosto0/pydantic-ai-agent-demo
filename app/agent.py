"""Pydantic AI agent for e-commerce customer support."""

import os

from pydantic_ai import Agent

from app.config import get_config
from app.state import UserState
from app.tools import get_order_status, start_return


# System prompt for the e-commerce support agent
SYSTEM_PROMPT = """You are a helpful e-commerce customer support agent for "ShopEasy".

Your responsibilities:
- Help customers check their order status
- Assist with return requests
- Answer general questions about shipping and returns

Guidelines:
- Be friendly, concise, and helpful
- When a customer asks about an order, use the check_order_status tool
- When a customer wants to return an item, use the request_return tool
- If the customer mentions an order ID, remember it for future reference
- If the customer asks about "my order" without an ID, check if you have a previous order ID from context

Current user context:
- Last intent: {last_intent}
- Last order ID: {last_order_id}
- Message count: {message_count}

Use this context to provide continuity in the conversation. If the user refers to 
"my order" or "the order" without specifying an ID, use the last_order_id if available.
"""


def create_agent(user_state: UserState) -> Agent:
    """Create and configure the Pydantic AI agent."""
    config = get_config()
    
    # Set OpenAI env vars for OpenRouter compatibility
    os.environ["OPENAI_API_KEY"] = config.api_key
    os.environ["OPENAI_BASE_URL"] = config.base_url
    
    # Format system prompt with user context
    formatted_prompt = SYSTEM_PROMPT.format(
        last_intent=user_state.last_intent or "None",
        last_order_id=user_state.last_order_id or "None",
        message_count=user_state.message_count,
    )
    
    # Use the openai: prefix to tell pydantic-ai to use OpenAI provider
    model = f"openai:{config.model}"
    
    agent = Agent(
        model=model,
        system_prompt=formatted_prompt,
    )
    
    # Register tools with the agent
    @agent.tool_plain
    def check_order_status(order_id: str) -> str:
        """
        Check the status of a customer's order.
        
        Args:
            order_id: The order ID to look up (e.g., "ORD-12345").
        """
        # Update state with the order ID
        user_state.update(intent="check_order", order_id=order_id)
        return get_order_status(order_id)
    
    @agent.tool_plain
    def request_return(order_id: str) -> str:
        """
        Start a return request for an order.
        
        Args:
            order_id: The order ID to return (e.g., "ORD-12345").
        """
        # Update state with the order ID and intent
        user_state.update(intent="return_request", order_id=order_id)
        return start_return(order_id)
    
    @agent.tool_plain
    def get_previous_order_id() -> str:
        """
        Get the last order ID mentioned by this customer.
        Use this when the customer refers to "my order" without specifying an ID.
        """
        order_id = user_state.last_order_id
        if order_id:
            return f"The customer's last mentioned order ID is: {order_id}"
        return "No previous order ID found for this customer."
    
    return agent


async def process_message(user_state: UserState, message: str) -> str:
    """
    Process a user message and return the agent's response.
    
    Args:
        user_state: The current user's state.
        message: The user's message.
        
    Returns:
        The agent's response.
    """
    # Create a fresh agent with the current user state
    agent = create_agent(user_state)
    
    # Run the agent
    result = await agent.run(message)
    
    # Update message count
    user_state.message_count += 1
    
    return result.output
