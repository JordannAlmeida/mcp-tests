from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import CallToolResult
from os import environ
from typing import Any
from .mcp_client_models import McpClientModels

class ClientMcpManager:

    @staticmethod
    async def get_mcp_client_models() -> McpClientModels:
        route_mcp = environ.get("ROUTE_MCP_SERVER", "")
        print(f"ROUTE_MCP_SERVER: {route_mcp}")
        async with streamablehttp_client(route_mcp) as (
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
                    list_tools=mcp_tools.tools,
                    list_resources=resources.resources,
                    list_prompts=prompts.prompts
                )
                return mcp_client_models
    
    @staticmethod
    async def call_tool(name: str, args: dict[str, Any]) -> CallToolResult:
        print(f"Calling tool: {name} with args: {args}")
        route_mcp = environ.get("ROUTE_MCP_SERVER", "")
        async with streamablehttp_client(route_mcp) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(name, args)
                return response