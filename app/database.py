from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Determine database path based on environment
if os.getenv('DOCKER_ENV'):
    # Docker environment - use mounted volume
    DB_PATH = "/app/data/words.db"
    DATA_DIR = "/app/data"
else:
    # Local development - use local directory
    DB_PATH = "data/words.db"
    DATA_DIR = "data"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
logging.info(f"Database path: {DB_PATH}")
logging.info(f"Data directory: {DATA_DIR}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 