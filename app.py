from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from connection import Session
from models import Action, ActionSegment

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Action Manager
@app.get("/action_manager")
async def action_manager(request: Request):
    return templates.TemplateResponse(request=request, name="action_manager.html")


@app.get("/add_action")
async def add_action(request: Request, name: str):
    with Session() as session:
        with session.begin():
            new_action = Action(name=name)
            session.add(new_action)
        new_action_id = new_action.id

    return templates.TemplateResponse(
        request=request,
        name="display_new_action.html",
        context={"new_action_id": new_action_id, "new_action_name": name},
    )


@app.get("/actions/all")
async def all_actions(request: Request):
    with Session() as session:
        actions = session.scalars(select(Action)).all()
    return templates.TemplateResponse(
        request=request, name="actions_list.html", context={"actions": actions}
    )


# Segment Manager
@app.get("/segment_manager")
async def segment_manager(request: Request):
    return templates.TemplateResponse(request=request, name="segment_manager.html")




@app.get("/start_segment")
async def start_segment(request: Request, action_id: int):
    with Session() as session:
        with session.begin():
            segment_start = datetime.now(tz=timezone.utc)
            new_segment = ActionSegment(
                action_id=action_id,
                start_at=segment_start,
            )
            session.add(new_segment)
        segment_action_name = new_segment.action.name
        segment_id = new_segment.id
    return templates.TemplateResponse(
        request=request,
        name="display_started_segment.html",
        context={
            "segment_action_name": segment_action_name,
            "segment_start": segment_start,
            "segment_id": segment_id,
        },
    )

@app.get("/running_segment_info")
async def running_segment_info(request: Request):
    with Session() as session:
        running_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)
        )
        current_time = datetime.now(tz=timezone.utc)
        segment_start = running_segment.start_at
        segment_action_name = running_segment.action.name
        segment_duration = current_time - segment_start.replace(tzinfo=timezone.utc)
    return templates.TemplateResponse(
        request=request,
        name="running_segment_info.html",
        context={
            "segment_action_name": segment_action_name,
            "segment_duration": segment_duration,
            "segment_start": segment_start,
            "current_time": current_time,
        }
    )


@app.get("/end_segment")
async def end_segment(request: Request):
    with Session() as session:
        with session.begin():
            running_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)
            )
            current_time = datetime.now(tz=timezone.utc)
            segment_start = running_segment.start_at
            segment_action_name = running_segment.action.name
            running_segment.end_at = current_time
            segment_duration = current_time - segment_start.replace(tzinfo=timezone.utc)
    return templates.TemplateResponse(
        request=request,
        name="display_ended_segment.html",
        context={
            "segment_start": segment_start,
            "segment_end": current_time,
            "segment_action_name": segment_action_name,
            "segment_duration": segment_duration,
        },
    )