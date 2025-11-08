from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.model import db, User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/media"


@router.get("/delete-user/{user_id}")
async def delete_user(user_id):

    user = db.query(User).filter_by(id=user_id).first()
    db.delete(user)
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=HTTP_302_FOUND)