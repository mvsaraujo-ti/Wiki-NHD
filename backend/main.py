from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.articles import router as articles_router

app = FastAPI(title="Zeus Knowledge 0.2 - Salesforce Edition")

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.include_router(articles_router, prefix="/articles")
