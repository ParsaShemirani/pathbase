import io
from datetime import datetime, timezone

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
import pandas as pd

from connection import Session
from models import ActionSegment, Note

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
                "action": active_segment.name,
                "segment_duration": active_segment.str_duration,
                "segment_start": active_segment.str_start_at,
            }
            segment_notes = session.scalars(
                select(Note).where(Note.str_created_ts > active_segment.str_start_at)
            ).all()
        else:
            active_segment_dict = {"no_active_segment": "True"}
            segment_notes = []

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_segment_dict": active_segment_dict, "segment_notes": segment_notes},
    )


@app.get("/start_segment")
async def start_segment(name: str):
    with Session() as session:
        with session.begin():
            active_segment = session.scalar(
                select(ActionSegment).where(ActionSegment.str_end_at == None)
            )
            if active_segment:
                raise HTTPException(
                    status_code=400, detail="There is already an active segment."
                )
            new_segment = ActionSegment(name=name)
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


@app.get("/add_note")
async def add_note(note_text: str):
    with Session() as session:
        with session.begin():
            new_note = Note(text=note_text)
            new_note.dt_created_ts = datetime.now(tz=timezone.utc)
            session.add(new_note)
    return RedirectResponse(url=app.url_path_for("home"), status_code=303)


@app.get("/download_segments_csv")
async def download_segments_csv():
    with Session() as session:
        conn = session.connection()
        df = pd.read_sql_table(table_name="action_segments", con=conn)
        str_iso_now = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d")
        with io.StringIO() as sio:
            df.to_csv(sio, index=False)
            return Response(
                content=sio.getvalue(),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=segments_{str_iso_now}.csv"
                },
            )

@app.get("/download_notes_csv")
async def download_notes_csv():
    with Session() as session:
        conn = session.connection()
        df = pd.read_sql_table(table_name="notes", con=conn)
        str_iso_now = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d")
        with io.StringIO() as sio:
            df.to_csv(sio, index=False)
            return Response(
                content=sio.getvalue(),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=notes_{str_iso_now}.csv"
                },
            )