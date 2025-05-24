from .mcp_client_models import McpClientModels
from .mcp_client_base import McpClientBase
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from mcp.types import CallToolResult
from mcp.types import Tool, Resource, Prompt
from typing import Any

class FetchClientMCP(McpClientBase):

    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_server_fetch"]
        )
        
    @staticmethod
    def get_prefix_identifier() -> str:
        return f"fetch_api{McpClientBase.get_caracter_separator_identifier()}"

    async def get_mcp_client_models(self) -> McpClientModels:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(
                read, write
            ) as session:
                await session.initialize()
                mcp_tools = await session.list_tools()
                prompts = await session.list_prompts()
                mcp_client_models = McpClientModels(
                    list_tools=[Tool(name=f"{FetchClientMCP.get_prefix_identifier()}{tool.name}", description=tool.description, inputSchema=tool.inputSchema, annotations=tool.annotations) for tool in mcp_tools.tools],
                    list_resources=[],
                    list_prompts=[Prompt(name=f"{FetchClientMCP.get_prefix_identifier()}{prompt.name}", description=prompt.description, arguments=prompt.arguments) for prompt in prompts.prompts]
                )
                return mcp_client_models

    async def call_tool(self, name: str, args: dict[str, Any]) -> CallToolResult:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(
                read, write
            ) as session:
                await session.initialize()
                response = await session.call_tool(name, args)
                return response