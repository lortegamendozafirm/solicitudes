from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from ..models import get_db, Solicitud
from ..schemas import SolicitudCreate, SolicitudResponse, SolicitudListResponse, SolicitudUpdate
from ..services import google_sheets_service

router = APIRouter(prefix="/api/solicitudes", tags=["solicitudes"])


def generate_numero_solicitud() -> str:
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:6].upper()
    return f"AUTO-{timestamp}-{unique_id}"


@router.post("/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
def crear_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    numero_solicitud = generate_numero_solicitud()

    db_solicitud = Solicitud(
        numero_solicitud=numero_solicitud,
        **solicitud.model_dump()
    )

    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)

    sheets_data = {
        "numero_solicitud": db_solicitud.numero_solicitud,
        "fecha_creacion": db_solicitud.fecha_creacion.isoformat(),
        "area_solicitante": db_solicitud.area_solicitante.value,
        "nombre_solicitante": db_solicitud.nombre_solicitante,
        "email_solicitante": db_solicitud.email_solicitante,
        "titulo_proceso": db_solicitud.titulo_proceso,
        "descripcion_proceso": db_solicitud.descripcion_proceso,
        "situacion_actual": db_solicitud.situacion_actual,
        "resultado_esperado": db_solicitud.resultado_esperado,
        "urgencia": db_solicitud.urgencia.value,
        "impacto": db_solicitud.impacto.value,
        "frecuencia_proceso": db_solicitud.frecuencia_proceso or "",
        "tiempo_manual_estimado": db_solicitud.tiempo_manual_estimado or "",
        "sistemas_involucrados": db_solicitud.sistemas_involucrados or "",
        "enlaces_documentacion": db_solicitud.enlaces_documentacion or "",
        "estado": db_solicitud.estado.value,
    }

    google_sheets_service.append_solicitud(sheets_data)

    return db_solicitud


@router.get("/", response_model=List[SolicitudListResponse])
def listar_solicitudes(
    skip: int = 0,
    limit: int = 100,
    area: str = None,
    estado: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Solicitud)

    if area:
        query = query.filter(Solicitud.area_solicitante == area)

    if estado:
        query = query.filter(Solicitud.estado == estado)

    solicitudes = query.order_by(Solicitud.fecha_creacion.desc()).offset(skip).limit(limit).all()
    return solicitudes


@router.get("/{solicitud_id}", response_model=SolicitudResponse)
def obtener_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not solicitud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitud no encontrada"
        )
    return solicitud


@router.patch("/{solicitud_id}", response_model=SolicitudResponse)
def actualizar_solicitud(
    solicitud_id: int,
    solicitud_update: SolicitudUpdate,
    db: Session = Depends(get_db)
):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not solicitud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitud no encontrada"
        )

    update_data = solicitud_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(solicitud, field, value)

    db.commit()
    db.refresh(solicitud)

    if "estado" in update_data:
        google_sheets_service.update_estado(
            solicitud.numero_solicitud,
            solicitud.estado.value
        )

    return solicitud


@router.get("/estadisticas/resumen")
def obtener_estadisticas(db: Session = Depends(get_db)):
    total = db.query(Solicitud).count()
    recibidas = db.query(Solicitud).filter(Solicitud.estado == "Recibido").count()
    en_analisis = db.query(Solicitud).filter(Solicitud.estado == "En Análisis").count()
    en_desarrollo = db.query(Solicitud).filter(Solicitud.estado == "En Desarrollo").count()
    completadas = db.query(Solicitud).filter(Solicitud.estado == "Completado").count()

    return {
        "total": total,
        "recibidas": recibidas,
        "en_analisis": en_analisis,
        "en_desarrollo": en_desarrollo,
        "completadas": completadas
    }
