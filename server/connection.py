import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.env_vars import DATABASE_PATH

if not DATABASE_PATH:
    raise ValueError("DATABASE_PATH variable not set in .env")

engine = create_engine("sqlite:///" + DATABASE_PATH, echo=True)

Session = sessionmaker(bind=engine)
