import io
from datetime import datetime, timezone

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
import pandas as pd

from server.connection import Session
from server.models import ActionSegment

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    with Session() as session:
        active_segment = session.scalar(
            select(ActionSegment).where(ActionSegment.str_end_at == None)
        )
        if active_segment:
            active_segment_dict = {
                "action_name": active_segment.action_name,
                "segment_duration": active_segment.str_duration,
                "segment_start": active_segment.str_start_at,
            }
        else:
            active_segment_dict = {"no_active_segment": True}

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_segment_dict": active_segment_dict},
    )


@app.get("/start_segment")
async def start_segment(action_name: str):
    with Session() as session:
        with session.begin():
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.str_end_at == None)
            )
            if active_segment:
                raise HTTPException(
                    status_code=400, detail="There is already an active segment."
                )
            new_segment = ActionSegment(action_name=action_name)
            new_segment.dt_start_at = datetime.now(tz=timezone.utc)
            session.add(new_segment)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)


@app.get("/end_segment")
async def end_segment():
    with Session() as session:
        with session.begin():
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.str_end_at == None)
            )
            if not active_segment:
                raise HTTPException(
                    status_code=400, detail="There is no active segment."
                )
            active_segment.dt_end_at = datetime.now(tz=timezone.utc)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)


@app.get("/delete_active_segment")
async def delete_active_segment():
    with Session() as session:
        with session.begin():
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.str_end_at == None)
            )
            if not active_segment:
                raise HTTPException(
                    status_code=400, detail="There is no active segment."
                )
            session.delete(active_segment)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)

@app.get("/download_csv")
async def download_csv():
    with Session() as session:
        conn = session.connection()
        df = pd.read_sql_table(table_name="action_segments", con=conn)
        str_iso_now = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d")
        with io.StringIO() as sio:
            df.to_csv(sio, index=False)
            return Response(
                content=sio.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={str_iso_now}.csv"}
            )
    


