"""Agente local para `profeonline.upload-batch/v1`.

Sube cada video como no listado, obtiene la transcripción desde la IP local,
registra el ítem en ProfeOnline y espera la validación antes de hacerlo público.
No contiene credenciales y no se ejecuta automáticamente.
"""

import argparse
import json
import mimetypes
import os
import time
from pathlib import Path

import requests
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from youtube_transcript_api import YouTubeTranscriptApi

SCHEMA = "profeonline.upload-batch/v1"
YOUTUBE_API = "https://www.googleapis.com/youtube/v3"
YOUTUBE_UPLOAD_API = "https://www.googleapis.com/upload/youtube/v3/videos"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"


def load_batch(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"Contrato no soportado: {data.get('schema')!r}")
    if not data.get("batch_id"):
        raise ValueError("El lote no contiene batch_id.")
    files = data.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("El lote no contiene archivos.")
    for name in files:
        if not isinstance(name, str) or Path(name).name != name or name in {".", ".."}:
            raise ValueError(f"Nombre de archivo inseguro: {name!r}")
    return data


def load_local_state(path):
    state_path = Path(path)
    if not state_path.exists():
        return {"files": {}}
    data = json.loads(state_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"files": {}}


def save_local_state(path, state):
    state_path = Path(path)
    temporary = state_path.with_suffix(state_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary.replace(state_path)


def youtube_session(token_file):
    credentials = Credentials.from_authorized_user_file(token_file, scopes=[YOUTUBE_SCOPE])
    return AuthorizedSession(credentials)


def upload_unlisted(session, video_path, title, description):
    mime = mimetypes.guess_type(video_path.name)[0] or "application/octet-stream"
    size = video_path.stat().st_size
    response = session.post(
        YOUTUBE_UPLOAD_API,
        params={"uploadType": "resumable", "part": "snippet,status"},
        headers={
            "X-Upload-Content-Length": str(size),
            "X-Upload-Content-Type": mime,
            "Content-Type": "application/json",
        },
        json={
            "snippet": {"title": title[:100], "description": description},
            "status": {"privacyStatus": "unlisted"},
        },
        timeout=60,
    )
    response.raise_for_status()
    upload_url = response.headers["Location"]
    with video_path.open("rb") as stream:
        uploaded = session.put(
            upload_url,
            headers={"Content-Type": mime, "Content-Length": str(size)},
            data=stream,
            timeout=60 * 60,
        )
    uploaded.raise_for_status()
    return uploaded.json()["id"]


def create_playlist(session, title, description):
    response = session.post(
        f"{YOUTUBE_API}/playlists",
        params={"part": "snippet,status"},
        json={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": "unlisted"},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["id"]


def add_to_playlist(session, playlist_id, video_id):
    response = session.post(
        f"{YOUTUBE_API}/playlistItems",
        params={"part": "snippet"},
        json={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
        timeout=30,
    )
    response.raise_for_status()


def fetch_transcript(video_id):
    api = YouTubeTranscriptApi()
    transcripts = list(api.list(video_id))
    if not transcripts:
        return ""
    preferred = next(
        (track for track in transcripts if track.language_code.startswith("es") and not track.is_generated),
        None,
    ) or next(
        (track for track in transcripts if track.language_code.startswith("es")),
        transcripts[0],
    )
    return " ".join(segment.text.strip() for segment in preferred.fetch() if segment.text.strip())


def fetch_transcript_with_retry(video_id, attempts, delay):
    for attempt in range(attempts):
        try:
            transcript = fetch_transcript(video_id)
        except Exception:  # YouTube aún puede estar procesando subtítulos
            transcript = ""
        if transcript:
            return transcript
        if attempt < attempts - 1:
            time.sleep(delay)
    return ""


def api_headers(token):
    return {"X-Api-Token": token, "Content-Type": "application/json"}


def register_item(base_url, token, batch, filename, video_id, transcript):
    taxonomy = batch.get("taxonomy") or {}
    response = requests.post(
        f"{base_url.rstrip('/')}/api/recursos/crear-video/",
        headers=api_headers(token),
        json={
            "batch_id": batch["batch_id"],
            "source_filename": filename,
            "title": Path(filename).stem,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "youtube_privacy": "unlisted",
            "transcript": transcript,
            "subject_slug": taxonomy.get("subject_slug"),
            "topic_slug": taxonomy.get("topic_slug"),
            "taxonomy": taxonomy,
            "instructions": batch.get("instructions", ""),
            "is_published": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["publication_item_id"]


def wait_until_ready(base_url, token, item_id, poll_seconds):
    while True:
        response = requests.get(
            f"{base_url.rstrip('/')}/api/publicacion/{item_id}/",
            headers=api_headers(token),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        if data["state"] in {"questions_ready", "published", "failed", "transcript_pending"}:
            return data
        time.sleep(poll_seconds)


def publish_video(session, video_id, metadata):
    current = session.get(
        f"{YOUTUBE_API}/videos",
        params={"part": "snippet,status", "id": video_id},
        timeout=30,
    )
    current.raise_for_status()
    item = current.json()["items"][0]
    snippet = item["snippet"]
    status = item["status"]
    snippet["title"] = metadata["youtube_title"][:100]
    snippet["description"] = metadata["youtube_description"]
    status["privacyStatus"] = "public"
    updated = session.put(
        f"{YOUTUBE_API}/videos",
        params={"part": "snippet,status"},
        json={"id": video_id, "snippet": snippet, "status": status},
        timeout=60,
    )
    updated.raise_for_status()


def confirm_publication(base_url, token, item_id):
    response = requests.post(
        f"{base_url.rstrip('/')}/api/publicacion/{item_id}/confirmar/",
        headers=api_headers(token),
        json={"youtube_privacy": "public"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def set_video_unlisted(session, video_id):
    """Revierte el video a no listado (compensación si el cierre server-side falla)."""
    current = session.get(
        f"{YOUTUBE_API}/videos",
        params={"part": "status", "id": video_id},
        timeout=30,
    )
    current.raise_for_status()
    status = current.json()["items"][0]["status"]
    status["privacyStatus"] = "unlisted"
    updated = session.put(
        f"{YOUTUBE_API}/videos",
        params={"part": "status"},
        json={"id": video_id, "status": status},
        timeout=60,
    )
    updated.raise_for_status()


def publish_and_confirm(session, base_url, token, item_id, video_id, metadata):
    """Hace público el video y confirma el cierre server-side.

    Si la confirmación falla, revierte el video a no listado para preservar el
    invariante "un fallo mantiene YouTube no listado y el recurso sin publicar".
    Devuelve True solo si el conjunto quedó publicado.
    """
    publish_video(session, video_id, metadata)
    try:
        confirm_publication(base_url, token, item_id)
    except requests.HTTPError:
        set_video_unlisted(session, video_id)
        return False
    return True


def process(args):
    batch = load_batch(args.batch)
    root = Path(args.video_dir).resolve()
    session = youtube_session(args.youtube_token)
    state_path = args.state_file or f"{args.batch}.state.json"
    local_state = load_local_state(state_path)
    local_state["batch_id"] = batch["batch_id"]
    files_state = local_state.setdefault("files", {})
    youtube = batch.get("youtube") or {}
    playlist_id = local_state.get("playlist_id") or youtube.get("playlist_id") or ""
    if youtube.get("create_playlist"):
        new_playlist = youtube.get("new_playlist") or {}
        if not playlist_id:
            playlist_id = create_playlist(
                session,
                new_playlist["title"],
                new_playlist.get("description", ""),
            )
            local_state["playlist_id"] = playlist_id
            save_local_state(state_path, local_state)
    for filename in batch["files"]:
        path = (root / filename).resolve()
        if path.parent != root or not path.is_file():
            raise FileNotFoundError(path)
        record = files_state.setdefault(filename, {})
        video_id = record.get("video_id")
        if not video_id:
            video_id = upload_unlisted(
                session,
                path,
                Path(filename).stem,
                batch.get("instructions", ""),
            )
            record["video_id"] = video_id
            save_local_state(state_path, local_state)
            if playlist_id:
                add_to_playlist(session, playlist_id, video_id)
                record["playlist_added"] = True
                save_local_state(state_path, local_state)
        elif playlist_id and not record.get("playlist_added"):
            add_to_playlist(session, playlist_id, video_id)
            record["playlist_added"] = True
            save_local_state(state_path, local_state)
        transcript = fetch_transcript_with_retry(
            video_id,
            attempts=args.transcript_attempts,
            delay=args.transcript_delay,
        )
        item_id = register_item(args.base_url, args.api_token, batch, filename, video_id, transcript)
        record["publication_item_id"] = item_id
        save_local_state(state_path, local_state)
        state = wait_until_ready(args.base_url, args.api_token, item_id, args.poll_seconds)
        if state["state"] == "transcript_pending":
            print(f"[espera] {filename}: transcripción insuficiente; permanece no listado.")
            continue
        if state["state"] == "failed":
            print(f"[falló] {filename}: {state.get('last_error', '')}")
            continue
        if state["state"] == "published":
            print(f"[ok] {filename}: ya estaba publicado.")
            continue
        published = publish_and_confirm(
            session,
            args.base_url,
            args.api_token,
            item_id,
            video_id,
            state["metadata"],
        )
        if published:
            record["published"] = True
            save_local_state(state_path, local_state)
            print(f"[ok] {filename}: conjunto publicado.")
        else:
            print(
                f"[revertido] {filename}: la confirmación falló; "
                "el video volvió a no listado y el recurso sigue sin publicar."
            )


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True)
    parser.add_argument("--video-dir", required=True)
    parser.add_argument("--base-url", default=os.environ.get("PROFEONLINE_BASE_URL", ""))
    parser.add_argument("--api-token", default=os.environ.get("PROFEONLINE_API_TOKEN", ""))
    parser.add_argument("--youtube-token", required=True, help="authorized_user JSON local de OAuth")
    parser.add_argument("--state-file", default="", help="sidecar de reanudación; por defecto <batch>.state.json")
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--transcript-attempts", type=int, default=6)
    parser.add_argument("--transcript-delay", type=int, default=60)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    if not parsed.base_url or not parsed.api_token:
        raise SystemExit("Faltan --base-url/--api-token (o variables de entorno).")
    process(parsed)
