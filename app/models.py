from sqlalchemy import Column, Integer, String, Enum, DateTime
from .database import Base
import enum
import datetime

class LearningStatus(enum.Enum):
    NOT_MASTERED = "fremd"
    MASTERED = "gemeistert"
    NEED_TO_LEARN = "lernende"

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True)
    explanation = Column(String)
    example = Column(String)
    status = Column(Enum(LearningStatus), default=LearningStatus.NOT_MASTERED)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
