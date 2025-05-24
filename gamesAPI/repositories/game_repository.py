from sqlalchemy.orm import Session
from typing import List, Optional
from schemas import GameCreate, GameUpdate
import models

class GameRepository:

    @staticmethod
    def get_game(db: Session, game_id: int) -> Optional[models.Game]:
        return db.query(models.Game).filter(models.Game.id == game_id).first()

    @staticmethod
    def get_games_by_title_contains(db: Session, title_query: str) -> List[models.Game]:
        return db.query(models.Game).filter(models.Game.title.contains(title_query)).all()

    @staticmethod
    def get_games(
        db: Session, 
        title: Optional[str] = None,
        category: Optional[str] = None,
        platform: Optional[str] = None,
        year_of_creation_min: Optional[int] = None,
        year_of_creation_max: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.Game]:
        query = db.query(models.Game)
        if title:
            query = query.filter(models.Game.title.contains(title))
        if category:
            query = query.filter(models.Game.category.contains(category))
        if platform:
            query = query.filter(models.Game.platform.contains(platform))
        if year_of_creation_min is not None:
            query = query.filter(models.Game.year_of_creation >= year_of_creation_min)
        if year_of_creation_max is not None:
            query = query.filter(models.Game.year_of_creation <= year_of_creation_max)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_game(db: Session, game: GameCreate) -> models.Game:
        db_game = models.Game(**game.dict())
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game

    @staticmethod
    def update_game(db: Session, game_id: int, game_update_data: GameUpdate) -> Optional[models.Game]:
        db_game = GameRepository.get_game(db, game_id)
        if db_game:
            update_data = game_update_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_game, key, value)
            db.commit()
            db.refresh(db_game)
        return db_game

    @staticmethod
    def delete_game(db: Session, game_id: int) -> Optional[models.Game]:
        db_game = GameRepository.get_game(db, game_id)
        if db_game:
            db.delete(db_game)
            db.commit()
        return db_game

    @staticmethod
    def get_games_count(db: Session) -> int:
        return db.query(models.Game).count()
