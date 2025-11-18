# Sistema de Solicitudes de Automatización

Sistema web para gestionar solicitudes de automatización de procesos internos para una firma legal especializada en visas humanitarias.

## Arquitectura

```
solicitudes/
├── backend/
│   ├── app/
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Esquemas Pydantic
│   │   ├── routers/         # Endpoints FastAPI
│   │   ├── services/        # Servicios (Google Sheets)
│   │   └── main.py          # Aplicación principal
│   └── requirements.txt
├── frontend/
│   ├── static/
│   │   ├── css/            # Estilos
│   │   └── js/             # JavaScript
│   └── templates/          # HTML
├── Dockerfile              # Para Cloud Run
├── cloudbuild.yaml         # CI/CD en Google Cloud
└── app.yaml               # Config App Engine
```

## Tecnologías

- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla
- **Integración**: Google Sheets API
- **Deployment**: Google Cloud (Cloud Run / App Engine)

## Configuración Local

### 1. Prerrequisitos

- Python 3.11+
- PostgreSQL 14+
- Cuenta de Google Cloud (para Google Sheets)

### 2. Base de Datos PostgreSQL

```bash
# Crear base de datos
createdb solicitudes_db

# O usando psql
psql -U postgres
CREATE DATABASE solicitudes_db;
```

### 3. Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env`:
```
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/solicitudes_db
GOOGLE_SHEET_ID=tu_sheet_id
GOOGLE_CREDENTIALS_JSON={"type": "service_account", ...}
```

### 4. Instalación

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 5. Ejecutar

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Visitar: http://localhost:8000

## Configuración Google Sheets

### 1. Crear Proyecto en Google Cloud

1. Ir a [Google Cloud Console](https://console.cloud.google.com)
2. Crear nuevo proyecto
3. Habilitar Google Sheets API

### 2. Crear Service Account

1. IAM & Admin > Service Accounts
2. Crear cuenta de servicio
3. Descargar JSON de credenciales
4. Copiar contenido JSON a variable `GOOGLE_CREDENTIALS_JSON`

### 3. Configurar Google Sheet

1. Crear nuevo Google Sheet
2. Nombrar primera hoja como "Solicitudes"
3. Compartir con email del service account (editor)
4. Copiar ID del Sheet (de la URL) a `GOOGLE_SHEET_ID`

### 4. Estructura del Sheet

El sistema creará automáticamente las columnas:
- Número Solicitud
- Fecha Creación
- Área Solicitante
- Nombre Solicitante
- Email
- Título del Proceso
- Descripción
- Situación Actual
- Resultado Esperado
- Urgencia
- Impacto
- Frecuencia
- Tiempo Manual Estimado
- Sistemas Involucrados
- Enlaces/Documentación
- Estado

## Despliegue en Google Cloud

### Opción 1: Cloud Run (Recomendado)

```bash
# Autenticarse
gcloud auth login

# Configurar proyecto
gcloud config set project TU_PROYECTO_ID

# Construir y desplegar
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_DATABASE_URL="tu_url",_GOOGLE_SHEET_ID="tu_id"
```

### Opción 2: App Engine

```bash
# Modificar app.yaml con tus credenciales
gcloud app deploy app.yaml
```

### Configurar Cloud SQL (PostgreSQL)

1. Crear instancia Cloud SQL PostgreSQL
2. Crear base de datos `solicitudes_db`
3. Configurar conexión privada o Auth Proxy
4. Actualizar `DATABASE_URL` en variables de entorno

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Frontend principal |
| POST | `/api/solicitudes/` | Crear solicitud |
| GET | `/api/solicitudes/` | Listar solicitudes |
| GET | `/api/solicitudes/{id}` | Obtener detalle |
| PATCH | `/api/solicitudes/{id}` | Actualizar estado |
| GET | `/api/solicitudes/estadisticas/resumen` | Estadísticas |
| GET | `/health` | Health check |

## Documentación API

FastAPI genera documentación automática:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Características

- Formulario completo para capturar solicitudes
- Validación de datos con Pydantic
- Estados de seguimiento (Recibido, En Análisis, En Desarrollo, Completado)
- Filtros por área y estado
- Dashboard con estadísticas
- Sincronización automática con Google Sheets
- Diseño responsive
- Interfaz moderna y profesional

## Áreas Soportadas

- SCC
- Psychology
- CC&C
- WAE's
- DCO
- Packets
- CA's
- Follow up
- Customer Service

## Seguridad

Para producción, considerar:
- Autenticación (OAuth2/JWT)
- HTTPS obligatorio
- Rate limiting
- Validación adicional en backend
- Auditoría de cambios
- Backup automático de BD

## Mantenimiento

```bash
# Ver logs
gcloud logging read "resource.type=cloud_run_revision"

# Escalar instancias
gcloud run services update solicitudes-app --max-instances=20
```

## Soporte

Centro de Automatización de Procesos
Firma Legal de Visas Humanitarias
