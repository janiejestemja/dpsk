from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

module_dir = Path(__file__).parent
DB_URL = "sqlite:///" + str(module_dir) + "/issues.db"

ngin = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=ngin)
Base = declarative_base()