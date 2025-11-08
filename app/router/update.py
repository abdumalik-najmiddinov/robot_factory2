import os
import shutil
from fastapi import APIRouter
from fastapi import Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import db, User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/update-user/{user_id}", response_class=HTMLResponse)
async def form_update(request: Request, user_id):
    user = db.query(User).filter_by(id=user_id).first()
    return templates.TemplateResponse("update_user.html",
                                      {"request": request, "user": user})



@router.post("/update-user/{user_id}")
async def update_user(request: Request, user_id):
    form = await request.form()

    fullname = form.get("fullname")
    job = form.get("job")
    about = form.get("about")
    image: UploadFile = form.get("image")

    user = db.query(User).filter_by(id=user_id).first()
    user.fullname = fullname
    user.job = job
    user.about = about

    if image and image.filename:
        file_location = os.path.join(UPLOAD_DIRECTION, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        user.image = image.filename

    db.commit()
    db.close()

    return RedirectResponse("/", status_code=HTTP_302_FOUND)