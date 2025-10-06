import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")

engine = create_engine("sqlite:///" + DATABASE_PATH, echo=True)

Session = sessionmaker(bind=engine)
