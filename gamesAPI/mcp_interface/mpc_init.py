from mcp.server.fastmcp import FastMCP
from mcp.types import Resource
from .games import mcp_create_game, mcp_get_game_by_id, mcp_list_games, mcp_delete_game_by_id
from os import environ

games_api_mcp = FastMCP(
    name="Games API",
    stateless_http=True,
    port=8001    
)

games_api_mcp.add_tool(
    fn=mcp_create_game,
    name="create_new_game",
    description="Create a new game in Games API",
)

# For now, google gemini does not support resources
# def __get_uri_list_games_resource():
#     return environ.get("ROUTE_GAMES") + "/games?title={title}&category={category}&platform={platform}&year_of_creation={year_of_creation}&skip={skip}&limit={limit}"

# games_api_mcp.add_resource(
#     Resource(
#         uri=__get_uri_list_games_resource(),
#         description="List all games in the database",
#         name="list_games",
#         mimeType="application/json",
#     )
# )

games_api_mcp.add_tool(
    fn=mcp_get_game_by_id,
    name="get_game_by_id",
    description="Get a game by its ID from Games API",
)

games_api_mcp.add_tool(
    fn=mcp_list_games,
    name="list_games",
    description="List games from Games API with optional filters",
)

games_api_mcp.add_tool(
    fn=mcp_delete_game_by_id,
    name="delete_game_by_id",
    description="Delete a game by its ID from Games API",
)
