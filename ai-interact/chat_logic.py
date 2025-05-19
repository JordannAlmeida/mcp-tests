import os
import asyncio
from typing import Optional
from google import genai
from google.genai.chats import Chat
from google.genai.types import GenerateContentConfig, ToolConfig, FunctionCallingConfig, FunctionCallingConfigMode, Tool
from mcp_client.manager import ClientMcpManager
from dotenv import load_dotenv

def load_api_key():
    """Loads the Google API key from the appropriate .env file."""
    environment = os.getenv("ENVIRONMENT", "local")
    if environment == "local":
        load_dotenv(".env.local")
    else:
        load_dotenv(".env")
    return os.getenv("GOOGLE_API_KEY")

def generate_response(chat: Chat, prompt: str) -> str:
    """Generates a response from the Gemini model."""
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def start_new_chat(api_key: str) -> Chat:
    """Initializes and returns the Gemini model."""
    if not api_key:
        raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")
    mcp_tools: list[Tool]
    tools_config: Optional[ToolConfig]
    try :
        mcp_tools = asyncio.run(ClientMcpManager.get_tools())
        tools_config=ToolConfig(
            function_calling_config=FunctionCallingConfig(
                mode=FunctionCallingConfigMode.AUTO,
            )
        )
    except Exception as e:
        import traceback
        print(f"Error fetching tools: {e}\nStack trace:\n{traceback.format_exc()}")
        
        mcp_tools = []
        tools_config = None
        
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            tools=mcp_tools,
            tool_config=tools_config
        )
    )
    return chat

