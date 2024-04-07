from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from marko import Markdown
from marko.block import FencedCode

from . import models
from .database import SessionLocal

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/puml/{note_id}")
async def puml(note_id: str, db: Session = Depends(get_db)):
    note = (
        db.query(models.Note)
        .where(models.Note.id == models.from_url(note_id))
        .first()
    )

    if not note:
        return 404

    content = next(n for n in Markdown().parse(note.content).children
                    if isinstance(n, FencedCode))
    if content:
        return PlainTextResponse(content.children[0].children)


@app.get("/notes")
async def notes(
    request: Request,
    db: Session = Depends(get_db),
    page: Optional[int] = 0,
    size: Optional[int] = 30,
):
    notes = (
        db.query(models.Note)
        .where(models.Note.permission != "private")
        .order_by(models.Note.lastchangeAt.desc())
        .offset(size * page)
        .limit(size)
        .all()
    )
    return templates.TemplateResponse(
        name="notes.html.jinja",
        context={"request": request, "notes": notes, "page": page, "size": size},
    )
