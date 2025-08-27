from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import select

from connection import Session
from models import Action, ActionSegment

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/current_segment")
def current_segment() -> str:
    """Return the currently running segment."""
    with Session() as session:
        running = session.scalar(
            select(ActionSegment).where(ActionSegment.end_at == None)  # noqa: E711
        )
        if running is None:
            return jsonify({"id": None})
        action = session.scalar(select(Action).where(Action.id == running.action_id))
        return jsonify(
            {
                "id": running.id,
                "action_id": running.action_id,
                "action_name": action.name if action else "Unknown",
                "start_at": running.start_at.isoformat(),
            }
        )


@app.route("/add_action", methods=["POST"])
def add_action() -> str:
    name = request.form.get("name", "").strip()
    if not name:
        return "<p>No name provided.</p>"
    new_action = Action(name=name)
    with Session() as session:
        with session.begin():
            session.add(new_action)
    return "<p>Action added.</p>"


@app.route("/search")
def search() -> str:
    query = request.args.get("q", "")
    with Session() as session:
        results: List[Action] = session.scalars(
            select(Action).where(Action.name.like(f"%{query}%"))
        ).all()
    return render_template("search_results.html", query=query, results=results)


@app.route("/switch", methods=["POST"])
def switch_action() -> str:
    action_id = request.form.get("action_id")
    if not action_id:
        return redirect(url_for("index"))
    with Session() as session:
        with session.begin():
            running = session.scalar(
                select(ActionSegment).where(ActionSegment.end_at == None)  # noqa: E711
            )
            if running is not None:
                running.end_at = datetime.now(tz=timezone.utc)
                session.add(running)
            new_segment = ActionSegment(
                action_id=int(action_id), start_at=datetime.now(tz=timezone.utc)
            )
            session.add(new_segment)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
