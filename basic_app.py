from datetime import datetime, timezone

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from basic_connection import Session
from basic_models import ActionSegment

app = FastAPI()

templates = Jinja2Templates(directory="basic_templates")

@app.get("/")
async def home(request: Request):
    # Get running segment info
    with Session() as session:
        running_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)
        )

        if running_segment:
            delta_duration = datetime.now(tz=timezone.utc) - running_segment.start_at.replace(tzinfo=timezone.utc)
            total_seconds = int(delta_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            running_segment_dict = {
                "action_name": running_segment.action_name,
                "segment_duration": duration_str,
                "segment_start": running_segment.start_at,
            }
        else:
            running_segment_dict = {"no_running_segment": True}

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "running_segment_dict": running_segment_dict
        }
    )

# PUT GUARD SO WONT ADD SEGMENT IF ONE IS ALREADY RUNNING

@app.get("/start_segment")
async def start_segment(request: Request, action_name: str):
    with Session() as session:
        with session.begin():
            # Make sure no session is active
            running_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            if running_segment:
                return HTTPException(status_code=400, detail="There is already a running segment.")

            # Since no active session, lets make the new one
            current_time = datetime.now(tz=timezone.utc)
            new_segment = ActionSegment(
                action_name=action_name,
                start_at=current_time,
            )
            session.add(new_segment)
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)


@app.get("/end_segment")
async def end_segment():
    with Session() as session:
        with session.begin():
            running_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            if not running_segment:
                raise HTTPException(status_code=400, detail="There is no running segment")
            running_segment.end_at = datetime.now(tz=timezone.utc)

    
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)