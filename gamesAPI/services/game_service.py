from sqlalchemy.orm import Session
from typing import List, Optional

from repositories.game_repository import GameRepository
import models
from schemas import GameCreate, GameUpdate


class GameService:

    @staticmethod
    def get_game(db: Session, game_id: int) -> Optional[models.Game]:
        return GameRepository.get_game(db, game_id=game_id)

    @staticmethod
    def get_games_by_title_contains(db: Session, title_query: str) -> List[models.Game]:
        return GameRepository.get_games_by_title_contains(db, title_query=title_query)

    @staticmethod
    def get_games(
        db: Session, 
        title: Optional[str] = None,
        category: Optional[str] = None,
        platform: Optional[str] = None,
        year_of_creation: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.Game]:
        return GameRepository.get_games(
            db, 
            title=title, 
            category=category, 
            platform=platform, 
            year_of_creation=year_of_creation, 
            skip=skip, 
            limit=limit
        )

    @staticmethod
    def create_game(db: Session, game: GameCreate) -> models.Game:
        return GameRepository.create_game(db=db, game=game)

    @staticmethod
    def update_game(db: Session, game_id: int, game_update_data: GameUpdate) -> Optional[models.Game]:
        return GameRepository.update_game(db, game_id=game_id, game_update_data=game_update_data)

    @staticmethod
    def delete_game(db: Session, game_id: int) -> Optional[models.Game]:
        return GameRepository.delete_game(db, game_id=game_id)

    @staticmethod
    def get_games_count(db: Session) -> int:
        return GameRepository.get_games_count(db)
