"""Servicio para obtener la transcripción de un video de YouTube.

Se usa para alimentar la generación de preguntas con lo que *realmente* se dice
en el video (no solo el título o la descripción). Depende de la librería
``youtube-transcript-api``; si no está instalada o el video no tiene subtítulos,
las funciones devuelven ``None`` en vez de fallar, para que el llamador degrade
con elegancia.
"""

import logging
import re

logger = logging.getLogger(__name__)

# Idiomas preferidos, en orden. Se prioriza español de cualquier variante.
DEFAULT_LANGUAGES = ("es", "es-419", "es-ES", "es-US")

# Patrones para extraer el ID de un video desde distintas formas de URL de YouTube.
_VIDEO_ID_PATTERNS = (
    re.compile(r"(?:v=|/v/)([0-9A-Za-z_-]{11})"),        # watch?v=ID  /v/ID
    re.compile(r"youtu\.be/([0-9A-Za-z_-]{11})"),         # youtu.be/ID
    re.compile(r"/embed/([0-9A-Za-z_-]{11})"),            # /embed/ID
    re.compile(r"/shorts/([0-9A-Za-z_-]{11})"),           # /shorts/ID
)


def extract_video_id(url_or_id):
    """Devuelve el ID de 11 caracteres de un video de YouTube, o ``None``.

    Acepta una URL completa (watch, youtu.be, embed, shorts) o directamente el ID.
    """
    if not url_or_id:
        return None

    value = url_or_id.strip()

    # Ya es un ID limpio.
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", value):
        return value

    for pattern in _VIDEO_ID_PATTERNS:
        match = pattern.search(value)
        if match:
            return match.group(1)

    return None


def _pick_transcript(transcript_list, languages):
    """Elige la mejor pista: español manual > español auto > primera disponible."""
    pistas = list(transcript_list)
    if not pistas:
        return None

    # 1) Español manual (más fiel).
    for t in pistas:
        if any(t.language_code.startswith(lang[:2]) for lang in languages) and not t.is_generated:
            return t
    # 2) Español auto-generado.
    for t in pistas:
        if any(t.language_code.startswith(lang[:2]) for lang in languages):
            return t
    # 3) Cualquier pista (mejor algo que nada).
    return pistas[0]


def _segments_to_text(segments):
    """Une los segmentos (objetos o dicts) en un solo texto plano."""
    partes = []
    for seg in segments:
        texto = getattr(seg, "text", None)
        if texto is None and isinstance(seg, dict):
            texto = seg.get("text", "")
        if texto:
            partes.append(texto.strip())
    return " ".join(p for p in partes if p)


def fetch_transcript(video_url_or_id, languages=DEFAULT_LANGUAGES, max_chars=None):
    """Devuelve el texto de la transcripción de un video, o ``None`` si no hay.

    - ``video_url_or_id``: URL de YouTube o ID directo.
    - ``languages``: idiomas preferidos (por defecto, variantes de español).
    - ``max_chars``: si se indica, recorta el texto a esa longitud.

    Robusta a las dos APIs de ``youtube-transcript-api`` (la estática <1.0 y la
    basada en instancia >=1.0). Nunca lanza: registra y devuelve ``None``.
    """
    video_id = extract_video_id(video_url_or_id)
    if not video_id:
        logger.info("transcript: no se pudo extraer video_id de %r", video_url_or_id)
        return None

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        logger.warning("transcript: 'youtube-transcript-api' no está instalado.")
        return None

    texto = None

    # --- API nueva (>=1.0): instancia con .list()/.fetch() ---
    try:
        api = YouTubeTranscriptApi()
        pista = _pick_transcript(api.list(video_id), languages)
        if pista is not None:
            texto = _segments_to_text(pista.fetch())
    except AttributeError:
        # La instancia no tiene .list(): es la API vieja. Se intenta abajo.
        pass
    except Exception as exc:  # noqa: BLE001 - degradar con elegancia
        logger.info("transcript(API nueva) falló para %s: %s", video_id, exc)

    # --- API vieja (<1.0): métodos estáticos ---
    if not texto:
        try:
            listado = YouTubeTranscriptApi.list_transcripts(video_id)
            pista = _pick_transcript(listado, languages)
            if pista is not None:
                texto = _segments_to_text(pista.fetch())
        except Exception as exc:  # noqa: BLE001
            logger.info("transcript(API vieja) falló para %s: %s", video_id, exc)

    if not texto:
        return None

    if max_chars and len(texto) > max_chars:
        texto = texto[:max_chars]

    return texto
