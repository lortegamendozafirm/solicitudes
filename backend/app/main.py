# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from .models import Base, engine
from .models.database import get_db
from .routers import solicitudes_router

# Crear tablas (solo en desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Solicitudes de Automatización",
    description="API para gestionar solicitudes de automatización de procesos internos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(solicitudes_router)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

if os.path.exists(os.path.join(frontend_path, "static")):
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(frontend_path, "static")),
        name="static",
    )


@app.get("/")
async def root():
    index_path = os.path.join(frontend_path, "templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Sistema de Solicitudes de Automatización API"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # Probar la conexión a la BD de verdad
    db.execute("SELECT 1")
    return {"status": "healthy", "service": "solicitudes-automatizacion"}
