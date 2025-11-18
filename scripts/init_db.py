#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models import Base, engine, SessionLocal, Solicitud, Estado, Urgencia, Impacto, AreaSolicitante
from datetime import datetime
import uuid


def generate_numero_solicitud():
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:6].upper()
    return f"AUTO-{timestamp}-{unique_id}"


def create_sample_data():
    """Crear datos de ejemplo para demostración"""

    # Crear tablas
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Verificar si ya hay datos
    existing = db.query(Solicitud).count()
    if existing > 0:
        print(f"Ya existen {existing} solicitudes en la base de datos.")
        response = input("¿Desea agregar datos de ejemplo adicionales? (s/n): ")
        if response.lower() != 's':
            db.close()
            return

    # Datos de ejemplo
    sample_solicitudes = [
        {
            "numero_solicitud": generate_numero_solicitud(),
            "area_solicitante": AreaSolicitante.CUSTOMER_SERVICE,
            "nombre_solicitante": "María González",
            "email_solicitante": "maria.gonzalez@firma.com",
            "titulo_proceso": "Generación automática de reportes de satisfacción",
            "descripcion_proceso": "Actualmente se generan reportes manualmente cada semana recopilando datos de encuestas de satisfacción del cliente. El proceso incluye: exportar datos de la plataforma de encuestas, consolidar en Excel, calcular métricas y crear gráficos.",
            "situacion_actual": "El proceso toma aproximadamente 4 horas cada semana y es propenso a errores humanos. Los reportes a veces se entregan tarde debido a la carga de trabajo.",
            "resultado_esperado": "Reportes generados automáticamente cada lunes a las 8am, enviados por correo a los gerentes con todas las métricas y gráficos actualizados.",
            "urgencia": Urgencia.ALTA,
            "impacto": Impacto.ALTO,
            "frecuencia_proceso": "Semanal",
            "tiempo_manual_estimado": "4 horas por semana",
            "sistemas_involucrados": "SurveyMonkey, Excel, Outlook",
            "enlaces_documentacion": "https://docs.google.com/document/d/ejemplo-reporte",
            "estado": Estado.EN_ANALISIS
        },
        {
            "numero_solicitud": generate_numero_solicitud(),
            "area_solicitante": AreaSolicitante.PSYCHOLOGY,
            "nombre_solicitante": "Dr. Roberto Méndez",
            "email_solicitante": "roberto.mendez@firma.com",
            "titulo_proceso": "Programación automática de citas de evaluación",
            "descripcion_proceso": "Coordinación manual de citas entre psicólogos y clientes. Se revisan disponibilidades, se contacta al cliente, se confirma horario y se actualiza el calendario.",
            "situacion_actual": "Proceso lento que requiere múltiples correos y llamadas. Frecuentes conflictos de horario y citas perdidas.",
            "resultado_esperado": "Sistema de auto-programación donde clientes seleccionen horario disponible y reciban confirmación automática.",
            "urgencia": Urgencia.MEDIA,
            "impacto": Impacto.MEDIO,
            "frecuencia_proceso": "Diario",
            "tiempo_manual_estimado": "2 horas diarias",
            "sistemas_involucrados": "Google Calendar, Sistema de gestión de casos",
            "enlaces_documentacion": "",
            "estado": Estado.RECIBIDO
        },
        {
            "numero_solicitud": generate_numero_solicitud(),
            "area_solicitante": AreaSolicitante.DCO,
            "nombre_solicitante": "Ana Torres",
            "email_solicitante": "ana.torres@firma.com",
            "titulo_proceso": "Validación automática de documentos de caso",
            "descripcion_proceso": "Revisión manual de documentos subidos por clientes verificando que estén completos, legibles y en el formato correcto antes de procesarlos.",
            "situacion_actual": "Alto volumen de documentos (50+ diarios), errores frecuentes que retrasan casos, tiempo significativo dedicado a tareas repetitivas.",
            "resultado_esperado": "Sistema que automáticamente valide formato, completitud y calidad de documentos, notificando al cliente si algo falta.",
            "urgencia": Urgencia.CRITICA,
            "impacto": Impacto.ALTO,
            "frecuencia_proceso": "Constante",
            "tiempo_manual_estimado": "6 horas diarias",
            "sistemas_involucrados": "Sistema de gestión documental, Portal del cliente",
            "enlaces_documentacion": "https://confluence/docs/proceso-validacion",
            "estado": Estado.EN_DESARROLLO
        },
        {
            "numero_solicitud": generate_numero_solicitud(),
            "area_solicitante": AreaSolicitante.FOLLOW_UP,
            "nombre_solicitante": "Carlos Ruiz",
            "email_solicitante": "carlos.ruiz@firma.com",
            "titulo_proceso": "Recordatorios automáticos de fechas importantes",
            "descripcion_proceso": "Envío manual de recordatorios a clientes sobre fechas límite, citas, y documentos pendientes.",
            "situacion_actual": "Se olvidan recordatorios importantes, clientes pierden fechas límite, proceso tedioso de revisar calendario diariamente.",
            "resultado_esperado": "Sistema de alertas automáticas que envíe recordatorios programados por email y SMS a clientes.",
            "urgencia": Urgencia.ALTA,
            "impacto": Impacto.ALTO,
            "frecuencia_proceso": "Diario",
            "tiempo_manual_estimado": "3 horas diarias",
            "sistemas_involucrados": "CRM, Sistema de correo, Base de datos de casos",
            "enlaces_documentacion": "",
            "estado": Estado.COMPLETADO
        },
        {
            "numero_solicitud": generate_numero_solicitud(),
            "area_solicitante": AreaSolicitante.SCC,
            "nombre_solicitante": "Laura Fernández",
            "email_solicitante": "laura.fernandez@firma.com",
            "titulo_proceso": "Generación automática de cartas estándar",
            "descripcion_proceso": "Creación manual de cartas de presentación, solicitud y seguimiento usando plantillas de Word que se personalizan para cada cliente.",
            "situacion_actual": "Proceso repetitivo, errores de transcripción, inconsistencias en formato entre diferentes empleados.",
            "resultado_esperado": "Generación automática de cartas desde plantillas con datos del cliente pre-poblados, manteniendo consistencia.",
            "urgencia": Urgencia.BAJA,
            "impacto": Impacto.MEDIO,
            "frecuencia_proceso": "Varias veces al día",
            "tiempo_manual_estimado": "30 minutos por carta",
            "sistemas_involucrados": "Word, Sistema de gestión de casos",
            "enlaces_documentacion": "https://sharepoint/plantillas-cartas",
            "estado": Estado.RECIBIDO
        }
    ]

    print("Insertando datos de ejemplo...")
    for data in sample_solicitudes:
        solicitud = Solicitud(**data)
        db.add(solicitud)

    db.commit()
    print(f"Se crearon {len(sample_solicitudes)} solicitudes de ejemplo.")

    db.close()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    create_sample_data()
