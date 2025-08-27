from datetime import datetime, timezone
from connection import Session
from models import Action, ActionSegment
from sqlalchemy import select


def initiate_unrecorded():
    unrecorded_segment = ActionSegment(
        action_id=1, start_at=datetime.now(tz=timezone.utc)
    )
    with Session() as session:
        with session.begin():
            session.add(unrecorded_segment)


def create_action(name: str) -> None:
    new_action = Action(
        name=name
    )
    with Session() as session:
        with session.begin():
            session.add(new_action)


def switch_to_action(action_id):
    with Session() as session:
        with session.begin():
            running_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            running_segment.end_at = datetime.now(tz=timezone.utc)

            new_segment = ActionSegment(
                action_id=action_id, start_at=datetime.now(tz=timezone.utc)
            )

            session.add_all([running_segment, new_segment])


def show_current_segment():
    with Session() as session:
        running_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)
        )
        running_action = session.scalar(
            select(Action).where(Action.id == running_segment.action_id)
        )

        elapsed = datetime.now(tz=timezone.utc) - running_segment.start_at.replace(
            tzinfo=timezone.utc
        )

        print(f"Current_time = {datetime.now()}")

        print(f"running_action: {running_action}")
        print(f"running_segment: {running_segment}")
        print(f"time_elapsed: {elapsed}")
