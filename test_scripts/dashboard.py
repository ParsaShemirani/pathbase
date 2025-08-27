
from datetime import datetime, timezone, timedelta
from connection import Session
from models import Action, ActionSegment, TimeFrame, ActionPlan
from sqlalchemy import select

def create_time_frame(start_at, end_at):
    time_frame = TimeFrame(
        start_at=start_at,
        end_at=end_at
    )
    with Session() as session:
        with session.begin():
            session.add(time_frame)
            new_id = time_frame.id
    return new_id

def create_action_plan(time_frame_id, action_id, duration: timedelta):
    action_plan = ActionPlan(
        time_frame_id=time_frame_id,
        action_id=action_id,
        duration=duration.total_seconds()
    )
    with Session() as session:
        with session.begin():
            session.add(action_plan)
            action_plan_id = action_plan.id
    return action_plan_id



def get_current_time_frame():
    now = datetime.now(tz=timezone.utc)
    with Session() as session:
        result = session.scalar(
            select(TimeFrame).where(TimeFrame.start_at <= now, TimeFrame.end_at > now)
        )
        retrieved_id = result.id
    if result:
        return retrieved_id
    else:
        return None
    

jamies = datetime(2025, 8, 26, 4)

jamiee = datetime(2025, 8, 27, 6)

mario = timedelta(hours=2, minutes=2, seconds=334)