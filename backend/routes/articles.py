from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

# Caminho CORRETO para os artigos
ARTICLES_DIR = r"D:\IA-ZEUS\Zeus.00\ZeusKnowledge0.2\articles"

@router.get("/")
def list_articles(request: Request):
    try:
        files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]
    except FileNotFoundError:
        return templates.TemplateResponse("list.html", {"request": request, "files": [], "error": "Pasta de artigos não encontrada"})
    return templates.TemplateResponse("list.html", {"request": request, "files": files})

@router.get("/{name}")
def read_article(name: str, request: Request):
    path = os.path.join(ARTICLES_DIR, name)
    if not os.path.exists(path):
        return templates.TemplateResponse("article.html", {"request": request, "content": "Artigo não encontrado."})

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return templates.TemplateResponse("article.html", {"request": request, "content": content})
