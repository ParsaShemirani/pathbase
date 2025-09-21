from connection import Session
from models import Action
session = Session()

session.begin()

jamie = Action(
    name="FastTianglo"
)

session.add(jamie)
session.commit()
session.close()


