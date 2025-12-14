from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from routes.articles import router as articles_router
from pydantic import BaseModel
import os
import requests

# =======================================
#   CONFIGURAÇÃO DE CAMINHOS
# =======================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # /backend
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))     # /Wiki-NHD

TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
STATIC_DIR = os.path.join(ROOT_DIR, "static")
ARTICLES_DIR = os.path.join(ROOT_DIR, "articles")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# =======================================
#   FASTAPI
# =======================================

app = FastAPI(title="Wiki NHD + Zeus Assistant")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =======================================
#   FUNÇÃO DE GATE (LOGIN ÚNICO – DEMO)
# =======================================
def require_login(request: Request):
    token = request.cookies.get("token")
    if not token:
        return False
    return True


# =======================================
#   LOGIN
# =======================================
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# =======================================
#   HOME (PROTEGIDA)
# =======================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not require_login(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("home.html", {"request": request})


# =======================================
#   BUSCA
# =======================================
@app.get("/search", response_class=HTMLResponse)
def search_articles(request: Request, query: str = ""):
    if not require_login(request):
        return RedirectResponse("/login")

    results = []
    query_lower = query.lower()

    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(ARTICLES_DIR, filename)

            if query_lower in filename.lower():
                results.append(filename)
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if query_lower in content:
                    results.append(filename)

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "query": query, "results": results}
    )


# =======================================
#   CATEGORIAS
# =======================================
@app.get("/category/{category_name}", response_class=HTMLResponse)
def category_page(request: Request, category_name: str):
    if not require_login(request):
        return RedirectResponse("/login")

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


# =======================================
#   ARTIGOS
# =======================================
app.include_router(articles_router, prefix="/articles")


# =======================================
#   ZEUS PANEL
# =======================================
@app.get("/zeus-panel", response_class=HTMLResponse)
def zeus_panel(request: Request):
    if not require_login(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("zeus_panel.html", {"request": request})


# =======================================
#   ZEUS CHAT
# =======================================
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


# =======================================
#   PÁGINAS DO NHD+
# =======================================
@app.get("/feed", response_class=HTMLResponse)
def feed_page(request: Request):
    if not require_login(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("feed.html", {"request": request})

@app.get("/incidentes", response_class=HTMLResponse)
def incidentes_page(request: Request):
    if not require_login(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("incidentes.html", {"request": request})

@app.get("/portal", response_class=HTMLResponse)
def portal_page(request: Request):
    if not require_login(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("portal.html", {"request": request})
