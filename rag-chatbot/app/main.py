from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.v1.routes import api_router
from app.core.logging_config import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator
import os

app = FastAPI(
    title="RAG Chatbot API",
    description="A production-ready RAG-based chatbot using Python and FastAPI.",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Setup logging
setup_logging()

# Include API router
app.include_router(api_router, prefix="/api")

# Instrument for Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("documentation.html", {"request": request})

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    # Read current values from .env to display in the form
    settings = {}
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    settings[key] = value
    return templates.TemplateResponse("settings.html", {"request": request, "settings": settings})

@app.post("/settings", response_class=HTMLResponse)
async def update_settings(
    request: Request,
    pinecone_api_key: str = Form(...),
    pinecone_cloud: str = Form(...),
    pinecone_region: str = Form(...)
):
    with open(".env", "w") as f:
        f.write(f"PINECONE_API_KEY={pinecone_api_key}\n")
        f.write(f"PINECONE_CLOUD={pinecone_cloud}\n")
        f.write(f"PINECONE_REGION={pinecone_region}\n")
    # Redirect to the settings page with a success message
    return templates.TemplateResponse("settings.html", {"request": request, "message": "Settings updated successfully. Please restart the application for the changes to take effect.", "settings": {"PINECONE_API_KEY": pinecone_api_key, "PINECONE_CLOUD": pinecone_cloud, "PINECONE_REGION": pinecone_region}})