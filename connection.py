import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")
if not DATABASE_PATH:
    raise ValueError("DATABASE_PATH variable not set in .env")

engine = create_engine("sqlite:///" + DATABASE_PATH, echo=True)

Session = sessionmaker(bind=engine)
