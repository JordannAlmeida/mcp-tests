from services.game_service import GameService
from database import get_db
from schemas import GameCreate
from typing import Optional
from mcp.server.fastmcp import FastMCP    

class McpGames:

    @staticmethod
    def add_games_mcp(mcp: FastMCP) -> FastMCP:
        mcp.add_tool(
            fn=McpGames.mcp_create_game,
            name="Create a new game",
            description="Create a new game in Games API",
            # inputSchema={
            #     "title": {"type": "string", "description": "Title of the game"},
            #     "year_of_creation": {"type": "integer", "description": "Year of creation of the game"},
            #     "platform": {"type": "string", "description": "Platform of the game"},
            #     "category": {"type": "string", "description": "Category of the game"},
            #     "summary": {"type": "string", "description": "Summary of the game"},
            # } 
        )
        return mcp

    @staticmethod
    def mcp_create_game(
        title: str,
        year_of_creation: Optional[int] = None,
        platform: Optional[str] = None,
        category: Optional[str] = None,
        summary: Optional[str] = None
    ) -> str:
        """
        Create a new game
        """
        GameService.create_game(
            db=get_db(),
            game=GameCreate(
                title=title,
                year_of_creation=year_of_creation,
                platform=platform,
                category=category,
                summary=summary
        ))
        return f"Game '{title}' created successfully."

