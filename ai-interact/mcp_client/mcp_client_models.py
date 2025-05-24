from mcp.types import Tool, Resource, Prompt

class McpClientModels:

    def __init__(self, list_tools: list[Tool], list_resources: list[Resource], list_prompts: list[Prompt]):
        self.list_tools: list[Tool] = list_tools
        self.list_resources: list[Resource] = list_resources
        self.list_prompts: list[Prompt] =list_prompts