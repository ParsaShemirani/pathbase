from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from connection import Session
from basic_models import Action, ActionSegment

app = FastAPI()

templates = Jinja2Templates(directory="basic_templates")

@app.get("/")
async def home(request: Request):
    # Get running segment info
    with Session() as session:
        running_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)
        )

        running_segment_dict = {
            "action_name": running_segment.action_name,
            "segment_duration": datetime.now(tz=timezone.utc) - running_segment.start_at.replace(tzinfo=timezone.utc),
            "segment_start": running_segment.start_at,
        }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "running_segment_dict": running_segment_dict
        }
    )

# PUT GUARD SO WONT ADD SEGMENT IF ONE IS ALREADY RUNNING
