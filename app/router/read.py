from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.model import db, User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    users = db.query(User).all()

    return templates.TemplateResponse("index.html",
                                      {"request": request, "users":users})