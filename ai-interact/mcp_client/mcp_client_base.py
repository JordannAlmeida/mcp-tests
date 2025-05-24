from abc import ABC
from typing import Any
from .mcp_client_models import McpClientModels

class McpClientBase(ABC):

    @staticmethod
    def get_caracter_separator_identifier() -> str:
        return "___"

    def get_prefix_identifier(self) -> str:
        """Return the prefix identifier for the MCP client."""
        raise NotImplementedError("Subclasses must implement get_prefix_identifier method.")

    async def get_mcp_client_models(self) -> McpClientModels:
        raise NotImplementedError("Subclasses must implement get_mcp_client_models method.")

    async def call_tool(self, name: str, args: dict[str, Any]) -> Any:
        raise NotImplementedError("Subclasses must implement call_tool method.")