from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import Tool
from google.genai import types
from os import environ

class ClientMcpManager:

    @staticmethod
    async def get_tools() -> list[types.Tool]:
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
                return ClientMcpManager.__getTools_gemini_format(mcp_tools.tools)


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
                        }
                    ]
                )
                for tool in list_tools
            ]