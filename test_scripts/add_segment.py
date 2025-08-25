from datetime import datetime, timezone
from connection import Session
from models import ActionSegment

session = Session()
session.begin()

jamiestart = datetime(2025, 8, 25, 15, 30, 12, tzinfo=timezone.utc)
jamieend = datetime(2025, 8, 25, 15, 35, 1, tzinfo=timezone.utc)


jamie = ActionSegment(
    action_id=1,
    start_at=jamiestart
)   
session.add(jamie)
session.commit()