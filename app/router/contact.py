import os
import shutil
from fastapi import APIRouter
from fastapi import Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from app.bot import bot, CHAT_ID
from app.model import db, User, Contact
from app.schemes import UserCreate, UserLogin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html",
                                      {"request": request})


@router.post("/contact")
async def create_register(request: Request):
    form = await request.form()

    gmail = form.get("gmail")
    phone_number = form.get("phone_number")
    text = form.get("text")

    contact = Contact(
        gmail=gmail,
        phone_number=phone_number,
        text=text)
    db.add(contact)
    db.commit()

    text = f"""<b>Gmail:</b> {gmail}
<b>Telegram:</b> <a href='https://t.me/{phone_number}'>{phone_number}</a>
<b>Phone number:</b> {phone_number}
<b>Text:</b> {text}"""
    await bot.send_message(chat_id=CHAT_ID,
                           text=text,
                           parse_mode="HTML")

    return RedirectResponse("/", status_code=HTTP_302_FOUND)
