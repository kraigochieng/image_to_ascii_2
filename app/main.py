from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import os

from .routes import image_to_ascii

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}

    return templates.TemplateResponse("index.html", context=context)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_to_ascii.router)
