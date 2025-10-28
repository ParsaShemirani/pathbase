from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env_vars import DATABASE_PATH

if not DATABASE_PATH:
    raise ValueError("DATABASE_PATH variable not set in .env")

engine = create_engine("sqlite:///" + str(DATABASE_PATH), echo=True)

Session = sessionmaker(bind=engine)
