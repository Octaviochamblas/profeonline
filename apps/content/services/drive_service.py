"""Servicio de Google Drive (solo lectura) para la biblioteca de guías.

Permite listar los documentos de una **carpeta de Drive** compartida con un
*service account* e importar su texto como guías de referencia (`QuizGuide`).

Diseño:
- Service account (no OAuth por usuario, no Google Picker): todo del lado del
  servidor, así no toca la CSP.
- Se usa la **REST API de Drive v3** directamente con una sesión autorizada de
  ``google-auth`` (sin el cliente pesado ``google-api-python-client``).
- Import **perezoso** de ``google-auth``: si el paquete no está o falta la
  credencial, se degrada con un mensaje claro y el resto del panel sigue vivo.
"""

import json
import logging
import re

from django.conf import settings

from apps.content.services.guide_service import extract_guide_text

logger = logging.getLogger(__name__)

_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
_FILES_URL = "https://www.googleapis.com/drive/v3/files"

# MIME de un Google Doc nativo: se exporta a texto (no se descarga binario).
GOOGLE_DOC_MIME = "application/vnd.google-apps.document"

# Tipos que sabemos convertir a texto (Google Doc, PDF, Word, texto plano).
SUPPORTED_MIMES = {
    GOOGLE_DOC_MIME,
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}

_FOLDER_RE = re.compile(r"/folders/([A-Za-z0-9_-]+)")
_ID_PARAM_RE = re.compile(r"[?&]id=([A-Za-z0-9_-]+)")


def is_configured():
    """¿Hay credencial de service account cargada?"""
    return bool(getattr(settings, "GOOGLE_SERVICE_ACCOUNT_JSON", ""))


def parse_folder_id(value):
    """Extrae el ID de carpeta de un link de Drive o devuelve el ID pelado.

    Acepta ``…/folders/<id>``, ``…?id=<id>`` o un ID directo. Devuelve "" si no
    se pudo reconocer.
    """
    if not value:
        return ""
    value = value.strip()
    match = _FOLDER_RE.search(value) or _ID_PARAM_RE.search(value)
    if match:
        return match.group(1)
    # ID pelado: sin barras ni espacios.
    if "/" not in value and " " not in value:
        return value
    return ""


def _get_session():
    """Crea una ``AuthorizedSession`` con la credencial del service account."""
    if not is_configured():
        raise RuntimeError(
            "Drive no está configurado: falta la variable GOOGLE_SERVICE_ACCOUNT_JSON."
        )
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError as exc:  # pragma: no cover - depende del entorno
        raise RuntimeError(
            "Falta el paquete 'google-auth'. Instalalo con: pip install google-auth."
        ) from exc

    try:
        info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON no es un JSON válido.") from exc

    creds = service_account.Credentials.from_service_account_info(info, scopes=[_SCOPE])
    return AuthorizedSession(creds)


def _check(response):
    """Convierte errores HTTP de Drive en mensajes accionables."""
    if response.status_code == 403:
        raise RuntimeError(
            "Drive denegó el acceso (403). ¿Compartiste la carpeta con el email "
            "del service account (rol Lector)?"
        )
    if response.status_code == 404:
        raise RuntimeError("Carpeta o archivo no encontrado en Drive (404). Revisá el ID/enlace.")
    response.raise_for_status()


def list_folder_files(folder):
    """Lista los documentos soportados de una carpeta de Drive.

    ``folder`` puede ser un ID o un link. Devuelve ``[{id, name, mime}]``.
    """
    folder_id = parse_folder_id(folder)
    if not folder_id:
        raise RuntimeError("No se reconoció la carpeta de Drive. Pegá el ID o el enlace de la carpeta.")

    session = _get_session()
    query = f"'{folder_id}' in parents and trashed = false"
    files = []
    page_token = None
    while True:
        params = {
            "q": query,
            "fields": "nextPageToken, files(id, name, mimeType)",
            "pageSize": 200,
            "orderBy": "name",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        }
        if page_token:
            params["pageToken"] = page_token
        response = session.get(_FILES_URL, params=params, timeout=30)
        _check(response)
        data = response.json()
        for item in data.get("files", []):
            if item.get("mimeType") in SUPPORTED_MIMES:
                files.append({
                    "id": item["id"],
                    "name": item.get("name", item["id"]),
                    "mime": item["mimeType"],
                })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return files


def fetch_file(file_id):
    """Descarga/exporta un archivo de Drive y devuelve ``{id, name, mime, text}``."""
    session = _get_session()

    meta = session.get(
        f"{_FILES_URL}/{file_id}",
        params={"fields": "id, name, mimeType", "supportsAllDrives": "true"},
        timeout=30,
    )
    _check(meta)
    info = meta.json()
    name = info.get("name", file_id)
    mime = info.get("mimeType", "")

    if mime == GOOGLE_DOC_MIME:
        exported = session.get(
            f"{_FILES_URL}/{file_id}/export",
            params={"mimeType": "text/plain"},
            timeout=60,
        )
        _check(exported)
        text = exported.content.decode("utf-8", errors="ignore")
    else:
        downloaded = session.get(
            f"{_FILES_URL}/{file_id}",
            params={"alt": "media", "supportsAllDrives": "true"},
            timeout=60,
        )
        _check(downloaded)
        text = extract_guide_text(downloaded.content, filename=name)

    return {"id": file_id, "name": name, "mime": mime, "text": text}
