from fastapi import FastAPI
from database import engine, Base
from controllers import game_controller
from multiprocessing import Process
import uvicorn
import asyncio

Base.metadata.create_all(bind=engine) # Create database tables

app = FastAPI(
        title="Games API",
        description="API for managing information about games.",
        version="0.1.0",
    )

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}

app.include_router(game_controller.router)

# Optional: Add initial data
from database import SessionLocal
from services.game_service import GameService
from schemas import GameCreate

def init_db():
    db = SessionLocal()
    try:
        if GameService.get_games_count(db) == 0:
            initial_games = [
                GameCreate(title="The Legend of Zelda: Breath of the Wild", year_of_creation=2017, platform="Nintendo Switch", category="Action-adventure", summary="An open-world action-adventure game."),
                GameCreate(title="Red Dead Redemption 2", year_of_creation=2018, platform="PlayStation 4", category="Action-adventure", summary="A western-themed action-adventure game."),
                GameCreate(title="The Witcher 3: Wild Hunt", year_of_creation=2015, platform="PC", category="Action RPG", summary="An open-world action role-playing game."),
                GameCreate(title="Grand Theft Auto V", year_of_creation=2013, platform="PlayStation 5", category="Action-adventure", summary="An action-adventure game with a large open world."),
                GameCreate(title="Super Mario Odyssey", year_of_creation=2017, platform="Nintendo Switch", category="Platformer", summary="A 3D platform game in the Super Mario series.")
            ]
            for game_data in initial_games:
                GameService.create_game(db=db, game=game_data)
            print("Initial data added to the database.")
        else:
            print("Database already contains data. Skipping initial data population.")
    finally:
        db.close()

def start_fastmcp_server():

    from mcp.server.fastmcp import FastMCP
    games_api_mcp = FastMCP(
            name="Games API",
            stateless_http=True,
            port=8001    
        )
    from mcp_interface.games import McpGames
    games_api_mcp = McpGames.add_games_mcp(games_api_mcp)

    print("Starting FastMCP server on port 8001...")
    asyncio.run(games_api_mcp.run_streamable_http_async())
    

def start_fastapi_server():
    print("Starting FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    init_db()  # Initialize DB with data if empty

    fastapi_process = Process(target=start_fastapi_server)
    fastmcp_process = Process(target=start_fastmcp_server)

    fastapi_process.start()
    fastmcp_process.start()

    fastapi_process.join()
    fastmcp_process.join()
