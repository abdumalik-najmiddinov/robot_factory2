import os
import shutil

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_302_FOUND

from app.bot import dp, bot, setup_webhook
from app.model import db, Product

from app.router import register, contact

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIRECTION = "app/static/media"
os.makedirs(UPLOAD_DIRECTION, exist_ok=True)
app.mount("/static", StaticFiles(directory='app/static'), name="static")


app.include_router(register.router)
app.include_router(contact.router)



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})


@app.get("/about.html", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("about.html",
                                      {"request": request})


@app.get("/shop.html", response_class=HTMLResponse)
async def index(request: Request):
    products = db.query(Product).all()
    return templates.TemplateResponse("shop.html",
                                      {"request": request, "products": products})


@app.get("/faq.html", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("faq.html",
                                      {"request": request})


@app.get("/create-product", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("create_product.html",
                                      {"request": request})


@app.post("/create-product")
async def index(request: Request):
    form = await request.form()
    title = form.get('title')
    about = form.get('about')
    price = form.get('price')
    review = form.get('review')
    image: UploadFile = form.get('image')

    file_path = os.path.join(UPLOAD_DIRECTION, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    product = Product(image=image.filename,
                      title=title,
                      about=about,
                      price=price,
                      review=review)
    db.add(product)
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=HTTP_302_FOUND)


# TELEGRAM WEBHOOK QO'SHAMIZ
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    await dp.feed_raw_update(bot, data)
    return JSONResponse({"ok": True})


# --- FastAPI ishga tushganda webhookni o‘rnatish ---
@app.on_event("startup")
async def on_startup():
    await setup_webhook()