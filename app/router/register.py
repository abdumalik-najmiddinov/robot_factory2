import os
import shutil
from fastapi import APIRouter
from fastapi import Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import db, User
from app.schemes import UserCreate, UserLogin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html",
                                      {"request": request})


@router.post("/register")
async def create_register(request: Request):
    form = await request.form()

    gmail = form.get("gmail")
    password = form.get("password")
    confirm_password = form.get("confirm_password")

    try:
        data = UserCreate(
            gmail=gmail,
            password=password,
            confirm_password=confirm_password)
    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": error_message
        })

    user = User(
        gmail=data.gmail,
        password=data.password,
        confirm_password=data.confirm_password
    )
    db.add(user)
    db.commit()

    return RedirectResponse("/", status_code=HTTP_302_FOUND)


@router.get("/login")
async def create_register(request: Request):
    form = await request.form()

    gmail = form.get("gmail")
    password = form.get("password")

    user = db.query(User).filter(User.gmail==gmail).first()

    if not user or user.password != password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error2": "Email yoki parol noto‘g‘ri"
        })


    return RedirectResponse("/", status_code=HTTP_302_FOUND)

