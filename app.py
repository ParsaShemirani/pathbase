from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from connection import Session
from models import Action, ActionSegment

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


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
        new_action_name = new_action.name

    return templates.TemplateResponse(
        request=request,
        name="display_new_action.html",
        context={"new_action_id": new_action_id, "new_action_name": new_action_name},
    )


@app.get("/actions/all")
async def all_actions(request: Request):
    with Session() as session:
        actions = session.scalars(select(Action)).all()
    return templates.TemplateResponse(
        request=request, name="actions_list.html", context={"actions": actions}
    )


"""
@app.get("/end_segment")
async def end_segment(request: Request):
    with Session() as session:
        with session.begin():
            ended_segment_dict = end_running_segment(session=session)
        session.refresh(ended_segment)
    return templates.TemplateResponse(request=request, name="display_ended_segment.html", context={"ended_segment": ended_segment})
    """
