# ZEUS Knowledge Base 0.2  
### 📘 Portal de Conhecimento Estilo Salesforce Lightning

O **ZEUS Knowledge Base 0.2** é um portal local de documentação técnica desenvolvido para servir como base de conhecimento estruturada, rápida e acessível, inspirada na interface **Salesforce Lightning Knowledge**.

Este projeto funciona de forma totalmente **local**, sem internet, e integra-se facilmente ao **ZEUS (Copiloto IA com RAG + Ollama)**.

---

## 🚀 Principais Recursos

### 🔹 Interface estilo Salesforce Lightning
- Layout limpo e moderno  
- Cards, categorias (v0.3), painel lateral e breadcrumbs  
- Navegação rápida e responsiva  

### 🔹 Renderização automática de Markdown
Arquivos `.md` adicionados na pasta `/articles` aparecem automaticamente no portal.

### 🔹 Backend FastAPI
- Rápido, seguro e leve  
- Rotas para home, artigos e listagem  

### 🔹 Suporte multiplataforma
Funciona em:
- Windows  
- Linux  
- WSL2  
- Máquinas sem internet  

### 🔹 Compatível com o ZEUS (RAG)
Os mesmos artigos podem ser usados no RAG do ZEUS para gerar respostas contextualizadas.

---

## 📁 Estrutura das Pastas

```plaintext
ZeusKnowledge0.2/
│
├── backend/
│   ├── main.py               # Servidor FastAPI
│   └── routes/
│       └── articles.py       # Rotas de artigos
│
├── templates/
│   ├── home.html
│   ├── list.html
│   ├── article.html
│   └── partials/
│       ├── header.html
│       └── footer.html
│
├── static/
│   ├── css/
│   │   └── style.css         # Estilo básico
│   └── js/
│       └── app.js            # Scripts
│
├── articles/                 # 📝 Onde ficam seus arquivos .md
│   └── exemplo.md
│
├── requirements.txt
└── run_knowledge02.bat
