from services.game_service import GameService
from database import SessionLocal
from schemas import GameCreate, Game
from typing import Optional
import traceback

def mcp_create_game(
    title: str,
    year_of_creation: Optional[int] = None,
    platform: Optional[str] = None,
    category: Optional[str] = None,
    summary: Optional[str] = None
) -> dict[str, str]:
    """
    Creates a new game entry in the database.
    Args:
        title (str): The title of the game.
        year_of_creation (Optional[int], optional): The year the game was created. Defaults to None.
        platform (Optional[str], optional): The platform the game is available on. Defaults to None.
        category (Optional[str], optional): The category or genre of the game. Defaults to None.
        summary (Optional[str], optional): A brief summary or description of the game. Defaults to None.
    Returns:
        str: A confirmation message indicating the game was created successfully.
    Raises:
        Any exceptions raised by the underlying GameService.create_game method.
    """
    print(f"Creating game with title: {title}, year_of_creation: {year_of_creation}, platform: {platform}, category: {category}, summary: {summary}")
    db = SessionLocal()
    try:
        model_game = GameService.create_game(
            db=db,
            game=GameCreate(
                title=title,
                year_of_creation=year_of_creation,
                platform=platform,
                category=category,
                summary=summary
        ))
        print(f"Game {model_game.title} created successfully.")
        return {
            "message": f"Game '{model_game.title}' created successfully."
        }
    except Exception as e:
        print(f"Error creating game: {str(e)}")
        traceback.print_exc()
        return {
            "message": f"Error to create the game {str(e)}"
        }
    finally:
        db.close()

def mcp_get_game_by_id(game_id: int) -> dict[str, str]:
    """
    Retrieves a game by its ID and returns it as a JSON message.
    Args:
        game_id (int): The ID of the game to retrieve.
    Returns:
        dict[str, str]: A message containing the game as JSON, or an error message if not found.
    """
    db = SessionLocal()
    try:
        model_game = GameService.get_game(db=db, game_id=game_id)
        if model_game is None:
            return {"message": f"Game with id {game_id} not found."}

        game_schema = Game.model_validate(model_game)
        return game_schema.model_dump_json()
    except Exception as e:
        traceback.print_exc()
        return {"message": f"Error retrieving game: {str(e)}"}
    finally:
        db.close()

def mcp_list_games(
    title: str = None,
    category: str = None,
    platform: str = None,
    year_of_creation_min: int = None,
    year_of_creation_max: int = None,
    skip: int = 0,
    limit: int = 100
) -> dict[str, str]:
    """
    Retrieves a list of games and returns them as a JSON message.
    Args:
        title (str, optional): Filter by title.
        category (str, optional): Filter by category.
        platform (str, optional): Filter by platform.
        year_of_creation_min (int, optional): Minimum year of creation.
        year_of_creation_max (int, optional): Maximum year of creation.
        skip (int): Number of records to skip.
        limit (int): Max number of records to return.
    Returns:
        dict[str, str]: A message containing the list of games as JSON.
    """
    db = SessionLocal()
    try:
        model_games = GameService.get_games(
            db=db,
            title=title,
            category=category,
            platform=platform,
            year_of_creation_min=year_of_creation_min,
            year_of_creation_max=year_of_creation_max,
            skip=skip,
            limit=limit
        )
        games_schema = [Game.model_validate(g) for g in model_games]
        games_json = [g.model_dump() for g in games_schema]
        import json
        return json.dumps(games_json)
    except Exception as e:
        traceback.print_exc()
        return {"message": f"Error retrieving games: {str(e)}"}
    finally:
        db.close()


