from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routes.articles import router as articles_router
import os  # IMPORTANTE

# Inicializa a aplicação FastAPI
app = FastAPI(title="Zeus Knowledge 0.2 - Salesforce Edition")

# Caminhos de templates e arquivos estáticos
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Diretório dos artigos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(BASE_DIR, "..", "articles")


# ------------------------
#   ROTA DE BUSCA /search
# ------------------------
@app.get("/search", response_class=HTMLResponse)
def search_articles(request: Request, query: str = ""):
    results = []

    query_lower = query.lower()

    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(ARTICLES_DIR, filename)

            # Verificar no nome do arquivo
            if query_lower in filename.lower():
                results.append(filename)
                continue

            # Verificar dentro do conteúdo
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if query_lower in content:
                    results.append(filename)

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "query": query, "results": results}
    )
# ------------------------
#   ROTA DE CATEGORIAS
# ------------------------
@app.get("/category/{category_name}", response_class=HTMLResponse)
def category_page(request: Request, category_name: str):
    results = []
    category_lower = category_name.lower()

    # Regras simples de identificação automática da categoria
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


# ------------------------
#   HOME
# ------------------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# ------------------------
#   ARTIGOS
# ------------------------
app.include_router(articles_router, prefix="/articles")

@app.get("/zeus-panel")
def zeus_panel(request: Request):
    return templates.TemplateResponse("zeus_panel.html", {"request": request})

from pydantic import BaseModel

class ZeusQuery(BaseModel):
    question: str

import requests  # coloque no topo se não existir

@app.post("/zeus-chat")
def zeus_chat(payload: ZeusQuery):
    question = payload.question

    try:
        response = requests.post(
            "http://localhost:8601/chat",   # endpoint real do Zeus
            json={"question": question},
            timeout=120
        )

        data = response.json()
        return {"answer": data.get("answer", "Erro: resposta vazia do Zeus")}

    except Exception as e:
        return {"answer": f"Erro ao conectar ao Zeus: {str(e)}"}

