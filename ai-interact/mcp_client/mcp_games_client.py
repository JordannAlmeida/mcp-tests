from .mcp_client_models import McpClientModels
from .mcp_client_base import McpClientBase
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import CallToolResult
from mcp.types import Tool, Resource, Prompt
from os import environ
from typing import Any

class McpGamesClient(McpClientBase):

    def __init__(self):
        self.route_mcp = environ.get("ROUTE_MCP_GAME_API_SERVER", "")

    @staticmethod
    def get_prefix_identifier() -> str:
        return f"games_api{McpClientBase.get_caracter_separator_identifier()}"

    async def get_mcp_client_models(self) -> McpClientModels:
        async with streamablehttp_client(self.route_mcp) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize();
                mcp_tools = await session.list_tools()
                resources = await session.list_resources()
                prompts = await session.list_prompts()
                mcp_client_models = McpClientModels(
                    list_tools=[Tool(name=f"{McpGamesClient.get_prefix_identifier()}{tool.name}", description=tool.description, inputSchema=tool.inputSchema, annotations=tool.annotations)  for tool in mcp_tools.tools],
                    list_resources=[Resource(name=f"{McpGamesClient.get_prefix_identifier()}{resource.name}", uri=resource.uri, description=resource.description, mimeType=resource.mimeType, size=resource.size, annotations=resource.annotations) for resource in resources.resources],
                    list_prompts=[Prompt(name=f"{McpGamesClient.get_prefix_identifier()}{prompt.name}", description=prompt.description, arguments=prompt.arguments) for prompt in prompts.prompts]
                )
                return mcp_client_models
    
    async def call_tool(self, name: str, args: dict[str, Any]) -> CallToolResult:
        async with streamablehttp_client(self.route_mcp) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(name, args)
                return response