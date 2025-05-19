from sqlalchemy import Column, Integer, String, Text
from database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year_of_creation = Column(Integer, index=True)
    platform = Column(String, index=True)
    category = Column(String, index=True)
    summary = Column(Text, nullable=True)
