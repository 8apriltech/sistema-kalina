from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.dashboard import router as dashboard_router
from routes.pacientes import router as pacientes_router
from routes.retiradas import router as retiradas_router

from database import engine, Base
from models import Paciente, RetiradaMensal

from starlette.middleware.proxy_headers import ProxyHeadersMiddleware

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)

# confia no Traefik / proxy
app.add_middleware(
    ProxyHeadersMiddleware,
    trusted_hosts="*"
)

templates = Jinja2Templates(directory="templates")


def no_cache(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"


app.include_router(dashboard_router)
app.include_router(pacientes_router)
app.include_router(retiradas_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, response: Response):
    no_cache(response)
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/dashboard-view", response_class=HTMLResponse)
def dashboard_view(request: Request, response: Response):
    no_cache(response)
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/cadastrar-paciente", response_class=HTMLResponse)
def cadastrar_paciente_view(request: Request, response: Response):
    no_cache(response)
    return templates.TemplateResponse("cadastrar_paciente.html", {"request": request})