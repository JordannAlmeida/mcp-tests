from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from services.game_service import GameService
from schemas import Game, GameCreate, GameUpdate
from database import get_db
import mcp

router = APIRouter(
    prefix="/games",
    tags=["Games"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Game, status_code=201)
def create_game_endpoint(game: GameCreate, db: Session = Depends(get_db)):
    return GameService.create_game(db=db, game=game)

@router.get("/", response_model=List[Game])
def read_games_endpoint(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Part of the game title to search for"),
    category: Optional[str] = Query(None, description="Category of the game"),
    platform: Optional[str] = Query(None, description="Platform of the game"),
    year_of_creation: Optional[int] = Query(None, description="Year of creation of the game"),
    skip: int = 0,
    limit: int = 100
):
    return GameService.get_games(
        db=db, 
        title=title, 
        category=category, 
        platform=platform, 
        year_of_creation=year_of_creation, 
        skip=skip, 
        limit=limit
    )

@router.get("/{game_id}", response_model=Game)
def read_game_endpoint(game_id: int, db: Session = Depends(get_db)):
    db_game = GameService.get_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.put("/{game_id}", response_model=Game)
def update_game_endpoint(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    db_game = GameService.update_game(db, game_id=game_id, game_update_data=game)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.delete("/{game_id}", response_model=Game)
def delete_game_endpoint(game_id: int, db: Session = Depends(get_db)):
    db_game = GameService.delete_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game
