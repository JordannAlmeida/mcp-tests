from pydantic import BaseModel
from typing import Optional

class GameBase(BaseModel):
    title: str
    year_of_creation: Optional[int] = None
    platform: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    title: Optional[str] = None # Allow title to be optional during update

class Game(GameBase):
    id: int

    class Config:
        from_attributes = True
