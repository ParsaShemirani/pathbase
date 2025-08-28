from typing import Any
from datetime import datetime, timezone

from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session as SessionType
from connection import Session
from models import Action, ActionSegment

def get_all_actions(session: SessionType) -> list[Action]:
    results = session.scalars(
        select(Action)
    ).all()
    return results

def add_new_action(session: SessionType, name: str) -> Action:
    new_action = Action(
        name=name
    )
    session.add(new_action)
    return new_action

def end_running_segment(session: SessionType) -> ActionSegment:
    running_segment = session.scalar(
        select(ActionSegment).where(ActionSegment.end_at == None)
    )
    running_segment.end_at = datetime.now(tz=timezone.utc)
    session.commit()
    return running_segment
