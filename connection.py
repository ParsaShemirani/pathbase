from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import database_path

engine = create_engine("sqlite:///" + database_path, echo=True)

Session = sessionmaker(bind=engine)
