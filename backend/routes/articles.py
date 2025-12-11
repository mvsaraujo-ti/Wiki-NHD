import os
import yaml
import markdown
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(BASE_DIR, "..", "articles")


# ------------------------
# LISTAR ARTIGOS
# ------------------------
@router.get("/")
def list_articles(request: Request):
    try:
        files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]
    except FileNotFoundError:
        return templates.TemplateResponse(
            "list.html",
            {
                "request": request,
                "files": [],
                "error": "Pasta de artigos não encontrada"
            },
        )

    return templates.TemplateResponse(
        "list.html",
        {"request": request, "files": files}
    )


# ------------------------
# LER ARTIGO INDIVIDUAL (com suporte a YAML)
# ------------------------
@router.get("/{name}")
def read_article(name: str, request: Request):
    path = os.path.join(ARTICLES_DIR, name)

    if not os.path.exists(path):
        return templates.TemplateResponse(
            "article.html",
            {
                "request": request,
                "content": "Artigo não encontrado.",
                "name": name,
                "meta": {}
            }
        )

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # --- Extrair YAML ---
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        meta = yaml.safe_load(parts[1])
        body_md = parts[2]
    else:
        meta = {}
        body_md = raw

    # Converter markdown para HTML
    content = markdown.markdown(body_md, extensions=['fenced_code', 'tables'])

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "content": content,
            "name": name,
            "meta": meta
        }
    )
