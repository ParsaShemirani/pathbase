from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from connection import Session
from api_functions import get_all_actions, add_new_action, end_running_segment

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
            new_action = add_new_action(session=session, name=name)
        session.refresh(new_action)
    return templates.TemplateResponse(request=request, name="display_new_action.html", context={"new_action": new_action})

@app.get("/actions/all")
async def all_actions(request: Request):
    with Session() as session:
        actions = get_all_actions(session=session)
    return templates.TemplateResponse(request=request, name="actions_list.html", context={"actions": actions})

"""
@app.get("/end_segment")
async def end_segment(request: Request):
    with Session() as session:
        with session.begin():
            ended_segment_dict = end_running_segment(session=session)
        session.refresh(ended_segment)
    return templates.TemplateResponse(request=request, name="display_ended_segment.html", context={"ended_segment": ended_segment})
    """