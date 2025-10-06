from datetime import datetime, timezone

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from connection import Session
from models import ActionSegment

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    # Get active segment info
    with Session() as session:
        active_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)
        )

        if active_segment:
            delta_duration = datetime.now(
                tz=timezone.utc
            ) - active_segment.start_at.replace(tzinfo=timezone.utc)
            total_seconds = int(delta_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            active_segment_dict = {
                "action_name": active_segment.action_name,
                "segment_duration": duration_str,
                "segment_start": active_segment.start_at,
            }
        else:
            active_segment_dict = {"no_active_segment": True}

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_segment_dict": active_segment_dict},
    )


@app.get("/start_segment")
async def start_segment(request: Request, action_name: str):
    with Session() as session:
        with session.begin():
            # Make sure no session is active
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            if active_segment:
                raise HTTPException(
                    status_code=400, detail="There is already a active segment."
                )

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
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            if not active_segment:
                raise HTTPException(status_code=400, detail="There is no active segment")
            active_segment.end_at = datetime.now(tz=timezone.utc)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)


@app.get("/delete_active_segment")
async def delete_active_segment():
    with Session() as session:
        with session.begin():
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            if not active_segment:
                raise HTTPException(status_code=400, detail="There is no active segment")
            session.delete(active_segment)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)
