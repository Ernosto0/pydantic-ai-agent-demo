"""Configuration for OpenRouter LLM provider."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


@dataclass
class OpenRouterConfig:
    """OpenRouter API configuration."""
    
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "openai/gpt-4o-mini"
    
    @classmethod
    def from_env(cls) -> "OpenRouterConfig":
        """Load configuration from environment variables."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        )


# Global config instance
config = OpenRouterConfig.from_env() if os.getenv("OPENROUTER_API_KEY") else None


def get_config() -> OpenRouterConfig:
    """Get the OpenRouter configuration."""
    global config
    if config is None:
        config = OpenRouterConfig.from_env()
    return config


