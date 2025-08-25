from connection import Session
from models import Action
session = Session()

session.begin()

jamie = Action(
    name="Unrecorded"
)

session.add(jamie)
session.commit()
session.close()


