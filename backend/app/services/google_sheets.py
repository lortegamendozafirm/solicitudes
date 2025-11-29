import os
import json
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError  # 👈 importa este

class GoogleSheetsService:
    def __init__(self):
        self.spreadsheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        self.credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
        self.service = None

        if self.credentials_json and self.spreadsheet_id:
            self._initialize_service()
        else:
            print("Google Sheets: variables de entorno no configuradas, se desactiva integración.")

    def _initialize_service(self):
        try:
            credentials_info = json.loads(self.credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            print("Google Sheets service inicializado correctamente.")
        except Exception as e:
            print(f"Error initializing Google Sheets service: {e}")
            self.service = None

    def append_solicitud(self, solicitud_data: dict) -> bool:
        if not self.service:
            print("Google Sheets service not initialized, se omite append.")
            return False

        try:
            values = [[
                solicitud_data.get("numero_solicitud", ""),
                solicitud_data.get("fecha_creacion", ""),
                solicitud_data.get("area_solicitante", ""),
                solicitud_data.get("nombre_solicitante", ""),
                solicitud_data.get("email_solicitante", ""),
                solicitud_data.get("titulo_proceso", ""),
                solicitud_data.get("descripcion_proceso", ""),
                solicitud_data.get("situacion_actual", ""),
                solicitud_data.get("resultado_esperado", ""),
                solicitud_data.get("urgencia", ""),
                solicitud_data.get("impacto", ""),
                solicitud_data.get("frecuencia_proceso", ""),
                solicitud_data.get("tiempo_manual_estimado", ""),
                solicitud_data.get("sistemas_involucrados", ""),
                solicitud_data.get("enlaces_documentacion", ""),
                solicitud_data.get("estado", "Recibido"),
            ]]

            body = {'values': values}

            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Solicitudes!A:P',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            print(f"Solicitud added to Google Sheets: {result}")
            return True

        except (HttpError, ServerNotFoundError, Exception) as error:
            # 👈 ahora se captura también el problema de red
            print(f"Error appending to Google Sheets: {error}")
            return False

    def update_estado(self, numero_solicitud: str, nuevo_estado: str) -> bool:
        if not self.service:
            print("Google Sheets service not initialized, se omite update_estado.")
            return False

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='Solicitudes!A:P'
            ).execute()

            values = result.get('values', [])

            for i, row in enumerate(values):
                if row and row[0] == numero_solicitud:
                    range_to_update = f'Solicitudes!P{i+1}'
                    body = {'values': [[nuevo_estado]]}

                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.spreadsheet_id,
                        range=range_to_update,
                        valueInputOption='USER_ENTERED',
                        body=body
                    ).execute()
                    print(f"Estado actualizado en Google Sheets para {numero_solicitud} -> {nuevo_estado}")
                    return True

            print(f"No se encontró la solicitud {numero_solicitud} en Google Sheets.")
            return False

        except (HttpError, ServerNotFoundError, Exception) as error:
            print(f"Error updating Google Sheets: {error}")
            return False

    def setup_headers(self) -> bool:
        if not self.service:
            print("Google Sheets service not initialized, se omite setup_headers.")
            return False

        try:
            headers = [[
                "Número Solicitud",
                "Fecha Creación",
                "Área Solicitante",
                "Nombre Solicitante",
                "Email",
                "Título del Proceso",
                "Descripción",
                "Situación Actual",
                "Resultado Esperado",
                "Urgencia",
                "Impacto",
                "Frecuencia",
                "Tiempo Manual Estimado",
                "Sistemas Involucrados",
                "Enlaces/Documentación",
                "Estado"
            ]]

            body = {'values': headers}

            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Solicitudes!A1:P1',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()

            print("Encabezados configurados en Google Sheets.")
            return True

        except (HttpError, ServerNotFoundError, Exception) as error:
            print(f"Error setting up headers: {error}")
            return False


google_sheets_service = GoogleSheetsService()
