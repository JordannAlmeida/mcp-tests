from google import genai
from google.genai.chats import Chat
from google.genai.types import GenerateContentConfig, ToolConfig, FunctionCallingConfig, FunctionCallingConfigMode, Tool, FunctionResponse, FunctionCall, Part, UploadFileConfig
from mcp_client.manager import ClientMcpManager
from mcp_client.mcp_client_models import McpClientModels
from mcp.types import CallToolResult
from google.genai import types
import os
from io import BytesIO
from ..base_llm import BaseLLM
from typing import Optional, Any
from files.files_manager import FilesManager
import asyncio
import json
import traceback

class GeminiManager(BaseLLM):

    def __init__(self):
        self.model = "gemini-2.0-flash"
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.chat: Chat = None
        self.client: genai.Client = None

    def initialize_model(self) -> Chat:
        """Initializes and returns the Gemini model."""
        if not self.api_key:
            raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")
        mcp_tools: list[Tool]
        tools_config: Optional[ToolConfig]
        try :
            mcp_model: McpClientModels = asyncio.run(ClientMcpManager.get_mcp_client_models())
            mcp_tools = GeminiManager.__getTools_gemini_format(mcp_model.list_tools)
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
            
        self.client = genai.Client(api_key=self.api_key)
        self.chat = self.client.chats.create(
            model=self.model,
            config=GenerateContentConfig(
                tools=mcp_tools,
                tool_config=tools_config
            )
        )

    def generate_response(self, prompt: str = "", files: list[dict[str, BytesIO]] = None):
        self.generate_response(
            prompt=prompt,
            files=files,
            list_part_with_function_response_recursion=[]
        )

    def generate_response(self, prompt: str = "", files: list[dict[str, BytesIO]] = None, list_part_with_function_response_recursion: list[Part] = []) -> str:
        """
        Generates a response from the Gemini model. Optionally accepts files as BytesIO (not used yet).
        """
        try:
            inputs_gemini = []
            if files is not None:
                for file in files:
                    file["stream"].seek(0)
                    bytes = file["stream"].read()
                    mime_type=FilesManager.get_mine_type_from_file_name(file["name"])
                    file_part = Part.from_bytes(data=bytes, mime_type=mime_type)
                    inputs_gemini.append(file_part)
            if(list_part_with_function_response_recursion is not None and len(list_part_with_function_response_recursion) > 0):
                for part in list_part_with_function_response_recursion:
                    inputs_gemini.append(part)
            if(prompt is not None and len(prompt) > 0):
                inputs_gemini.append(prompt)
            response = self.chat.send_message(message=inputs_gemini)
            if response.function_calls and len(response.function_calls) > 0:
                parts_response = response.candidates[0].content.parts
                list_parts_with_function_response = []
                for part in parts_response:
                    function_call: FunctionCall = part.function_call
                    call_tool_result: CallToolResult = None
                    call_tool_result = asyncio.run(ClientMcpManager.call_tool(function_call.name, function_call.args))
                    if( call_tool_result is None or call_tool_result.isError):
                        return f"Error: No response from function call {function_call.name}"
                    content = call_tool_result.content[0]
                    if content is None:
                        return f"Error: No content from function call {function_call.name}"
                    dict_from_text_content: dict[str, Any] = {
                        "response": json.loads(content.text)
                    }
                    function_response = FunctionResponse(
                        id=function_call.id,
                        name=function_call.name,
                        response=dict_from_text_content
                    )
                    part_with_function_response = Part(
                        function_response=function_response
                    )
                    list_parts_with_function_response.append(part_with_function_response)
                return self.generate_response(
                    list_part_with_function_response_recursion = list_parts_with_function_response
                )

            return response.text
        except Exception as e:
            traceback.print_exc()
            return f"Error generating response: {str(e)}"

    @staticmethod
    def __getTools_gemini_format(list_tools: list[Tool]) -> list[types.Tool]:
        return [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                            "response": types.Schema(
                                type='STRING',
                                description="Indicate if the response was successful or failed",
                                title="message",
                            )
                        }
                    ]
                )
                for tool in list_tools
            ]