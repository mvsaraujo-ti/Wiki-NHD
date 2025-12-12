from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routes.articles import router as articles_router
from pydantic import BaseModel
import os
import requests

# ============================
#  CONFIGURAÇÃO BASE
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

app = FastAPI(title="Wiki NHD + Zeus Assistant")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(ROOT_DIR, "static")),
    name="static"
)

ARTICLES_DIR = os.path.join(ROOT_DIR, "articles")


# ============================
#  ROTA HOME
# ============================
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# ============================
#  ROTA BUSCA
# ============================
@app.get("/search", response_class=HTMLResponse)
def search_articles(request: Request, query: str = ""):
    results = []
    query_lower = query.lower()

    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(ARTICLES_DIR, filename)

            # Busca em nome do arquivo
            if query_lower in filename.lower():
                results.append(filename)
                continue

            # Busca no conteúdo
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if query_lower in content:
                    results.append(filename)

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "query": query, "results": results}
    )


# ============================
#  ROTA CATEGORIAS
# ============================
@app.get("/category/{category_name}", response_class=HTMLResponse)
def category_page(request: Request, category_name: str):
    results = []
    category_lower = category_name.lower()

    mapping = {
        "sentinela": ["sentinela", "tutor"],
        "cnj": ["cnj", "apoia", "enatjus", "datajud"],
        "infra": ["vpn", "configuracao", "estacoes", "desligamento"],
        "segurança": ["certificado", "e-mails", "seguranca"],
        "suporte": ["suporte", "contatos", "atendimento"]
    }

    valid_terms = mapping.get(category_lower, [])

    for filename in os.listdir(ARTICLES_DIR):
        if any(term in filename.lower() for term in valid_terms):
            results.append(filename)

    return templates.TemplateResponse(
        "category.html",
        {"request": request, "category": category_name, "results": results}
    )


# ============================
#  ROTAS DE ARTIGOS
# ============================
app.include_router(articles_router, prefix="/articles")


# ============================
#  ZEUS PANEL (assistente)
# ============================
@app.get("/zeus-panel")
def zeus_panel(request: Request):
    return templates.TemplateResponse("zeus_panel.html", {"request": request})


# ============================
#  CHAT DO ZEUS
# ============================
class ZeusQuery(BaseModel):
    question: str

@app.post("/zeus-chat")
def zeus_chat(payload: ZeusQuery):
    try:
        response = requests.post(
            "http://localhost:8601/chat",
            json={"question": payload.question},
            timeout=120
        )
        data = response.json()
        return {"answer": data.get("answer", "Erro: Resposta vazia do Zeus")}

    except Exception as e:
        return {"answer": f"Erro ao conectar ao Zeus: {str(e)}"}

@app.get("/feed")
def feed_page(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})

@app.get("/incidentes")
def incidentes_page(request: Request):
    return templates.TemplateResponse("incidentes.html", {"request": request})

@app.get("/portal", response_class=HTMLResponse)
def portal(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request})
