from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:////users/parsashemirani/main/basic_pathbase.db", echo=True)

Session = sessionmaker(bind=engine)
