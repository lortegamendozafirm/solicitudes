from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models.solicitud import AreaSolicitante, Urgencia, Estado, Impacto


class SolicitudBase(BaseModel):
    area_solicitante: AreaSolicitante
    nombre_solicitante: str = Field(..., min_length=2, max_length=100)
    email_solicitante: EmailStr
    titulo_proceso: str = Field(..., min_length=5, max_length=200)
    descripcion_proceso: str = Field(..., min_length=20)
    situacion_actual: str = Field(..., min_length=10)
    resultado_esperado: str = Field(..., min_length=10)
    urgencia: Urgencia
    impacto: Impacto
    frecuencia_proceso: Optional[str] = None
    tiempo_manual_estimado: Optional[str] = None
    sistemas_involucrados: Optional[str] = None
    enlaces_documentacion: Optional[str] = None


class SolicitudCreate(SolicitudBase):
    pass


class SolicitudUpdate(BaseModel):
    estado: Optional[Estado] = None
    notas_internas: Optional[str] = None


class SolicitudResponse(SolicitudBase):
    id: int
    numero_solicitud: str
    estado: Estado
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    notas_internas: Optional[str] = None

    class Config:
        from_attributes = True


class SolicitudListResponse(BaseModel):
    id: int
    numero_solicitud: str
    area_solicitante: AreaSolicitante
    titulo_proceso: str
    urgencia: Urgencia
    estado: Estado
    fecha_creacion: datetime

    class Config:
        from_attributes = True
