from .mcp_games_client import McpGamesClient
from .fetch_client_mcp import FetchClientMCP
from .mcp_client_base import McpClientBase
from .mcp_client_models import McpClientModels
from mcp.types import CallToolResult
from typing import Any
import asyncio


class ClientMcpManager:

    def __init__(self):
        self.mcp_clients: dict[str, McpClientBase] = self.__add_mcp_clients()

    async def get_mcp_client_models(self) -> list[McpClientModels]:
        tasks = [client.get_mcp_client_models() for client in self.mcp_clients.values()]
        return await asyncio.gather(*tasks)
    
    async def call_tool(self, name: str, args: dict[str, Any]) -> CallToolResult:
        client: McpClientBase = self.__get_client_by_tool_name(name)
        if client:
            return await client.call_tool(name.split(McpClientBase.get_caracter_separator_identifier())[1], args)
        else:
            raise ValueError(f"No client found for tool name: {name}")
        
    def __get_client_by_tool_name(self, name: str) -> McpClientBase | None:
        key_client = f"{name.split(McpClientBase.get_caracter_separator_identifier())[0]}{McpClientBase.get_caracter_separator_identifier()}"
        return  self.mcp_clients.get(key_client, None)


    def __add_mcp_clients(self) -> dict[str, McpClientBase]:
        mcp_clients = {}
        mcp_clients[McpGamesClient.get_prefix_identifier()] = McpGamesClient()
        mcp_clients[FetchClientMCP.get_prefix_identifier()] = FetchClientMCP()
        return mcp_clients