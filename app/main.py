from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


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
