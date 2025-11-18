# app/models/database.py
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# === Cargar .env ===
# Asumiendo que .env está en la raíz del proyecto: solicitudes/.env
# database.py está en: solicitudes/backend/app/models/database.py
# parents[0] = models, [1] = app, [2] = backend, [3] = solicitudes (raíz)
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

# Ahora sí, tomar la URL desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definido en el .env")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
