from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.dashboard import router as dashboard_router
from routes.pacientes import router as pacientes_router
from routes.retiradas import router as retiradas_router

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Rotas API
app.include_router(dashboard_router)
app.include_router(pacientes_router)
app.include_router(retiradas_router)

# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# DASHBOARD VISUAL
@app.get("/dashboard-view", response_class=HTMLResponse)
def dashboard_view(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# CADASTRAR PACIENTE
@app.get("/cadastrar-paciente", response_class=HTMLResponse)
def cadastrar_paciente_view(request: Request):
    return templates.TemplateResponse("cadastrar_paciente.html", {"request": request})
