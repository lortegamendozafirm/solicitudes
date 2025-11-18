from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from .database import Base
import enum


class AreaSolicitante(str, enum.Enum):
    SCC = "SCC"
    PSYCHOLOGY = "Psychology"
    CC_AND_C = "CC&C"
    WAES = "WAE's"
    DCO = "DCO"
    PACKETS = "Packets"
    CAS = "CA's"
    FOLLOW_UP = "Follow up"
    CUSTOMER_SERVICE = "Customer Service"


class Urgencia(str, enum.Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"


class Estado(str, enum.Enum):
    RECIBIDO = "Recibido"
    EN_ANALISIS = "En Análisis"
    EN_DESARROLLO = "En Desarrollo"
    COMPLETADO = "Completado"


class Impacto(str, enum.Enum):
    BAJO = "Bajo"
    MEDIO = "Medio"
    ALTO = "Alto"


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    numero_solicitud = Column(String(20), unique=True, index=True)
    area_solicitante = Column(SQLEnum(AreaSolicitante), nullable=False)
    nombre_solicitante = Column(String(100), nullable=False)
    email_solicitante = Column(String(100), nullable=False)
    titulo_proceso = Column(String(200), nullable=False)
    descripcion_proceso = Column(Text, nullable=False)
    situacion_actual = Column(Text, nullable=False)
    resultado_esperado = Column(Text, nullable=False)
    urgencia = Column(SQLEnum(Urgencia), nullable=False)
    impacto = Column(SQLEnum(Impacto), nullable=False)
    frecuencia_proceso = Column(String(100), nullable=True)
    tiempo_manual_estimado = Column(String(100), nullable=True)
    sistemas_involucrados = Column(Text, nullable=True)
    enlaces_documentacion = Column(Text, nullable=True)
    estado = Column(SQLEnum(Estado), default=Estado.RECIBIDO)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    notas_internas = Column(Text, nullable=True)
