#!/usr/bin/env python3
"""
Script para configurar los encabezados en Google Sheets
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.services import google_sheets_service


def setup_google_sheets():
    """Configurar encabezados en Google Sheets"""

    if not google_sheets_service.service:
        print("ERROR: No se pudo inicializar el servicio de Google Sheets.")
        print("Verifique que las variables de entorno estén configuradas:")
        print("  - GOOGLE_SHEET_ID")
        print("  - GOOGLE_CREDENTIALS_JSON")
        return False

    print("Configurando encabezados en Google Sheets...")
    success = google_sheets_service.setup_headers()

    if success:
        print("Encabezados configurados exitosamente.")
        print("\nAsegúrese de que la hoja se llame 'Solicitudes'")
        print("Los datos se agregarán automáticamente cuando se creen nuevas solicitudes.")
    else:
        print("ERROR: No se pudieron configurar los encabezados.")
        print("Verifique que:")
        print("  1. El Sheet ID sea correcto")
        print("  2. El service account tenga permisos de editor")
        print("  3. La hoja 'Solicitudes' exista")

    return success


if __name__ == "__main__":
    setup_google_sheets()
