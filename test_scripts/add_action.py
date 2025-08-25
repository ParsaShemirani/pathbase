from connection import Session
from models import Action
session = Session()

session.begin()

jamie = Action(
    name="Eat_tomatoes"
)

session.add(jamie)

session.close()


