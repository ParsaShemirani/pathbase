from datetime import datetime, timezone
from connection import Session
from models import ActionSegment

from sqlalchemy import select

session = Session()
session.begin()

jamie = session.scalar(select(ActionSegment).where(ActionSegment.end_at == None))

jamieend = datetime(2025, 8, 25, 15, 35, 1, tzinfo=timezone.utc)

jamie.end_at = jamieend
session.add(jamie)
session.commit()
session.close()