import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.urls import reverse

from apps.content.models import Area, Level, Resource, Subject, Topic


YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


def extract_playlist_id(value):
    parsed = urlparse(value)
    query = parse_qs(parsed.query)
    if query.get("list"):
        return query["list"][0]
    return value.strip()


def extract_video_id(value):
    patterns = [
        r"(?:youtube\.com\/watch\?.*v=)([^&\s]+)",
        r"(?:youtube\.com\/embed\/)([^?&\/\s]+)",
        r"(?:youtube\.com\/shorts\/)([^?&\/\s]+)",
        r"(?:youtu\.be\/)([^?&\/\s]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value.strip()):
        return value.strip()
    return None


def youtube_get(endpoint, params):
    url = f"{YOUTUBE_API_URL}/{endpoint}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise CommandError(f"YouTube API respondio con HTTP {exc.code}") from exc
    except URLError as exc:
        raise CommandError(f"No se pudo conectar con YouTube API: {exc.reason}") from exc


def fetch_playlist_videos(playlist_id, api_key, limit=None):
    videos = []
    page_token = None

    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        data = youtube_get("playlistItems", params)
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            content_details = item.get("contentDetails", {})
            resource_id = snippet.get("resourceId", {})
            video_id = content_details.get("videoId") or resource_id.get("videoId")
            title = snippet.get("title", "").strip()
            if not video_id or title in {"Deleted video", "Private video"}:
                continue
            videos.append(
                {
                    "id": video_id,
                    "title": title,
                    "description": snippet.get("description", "").strip(),
                    "position": snippet.get("position", len(videos)),
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )
            if limit and len(videos) >= limit:
                return videos

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return videos


def fetch_single_video(video_id, api_key):
    data = youtube_get(
        "videos",
        {
            "part": "snippet",
            "id": video_id,
            "key": api_key,
        },
    )
    items = data.get("items", [])
    if not items:
        raise CommandError(f"No se encontro el video de YouTube {video_id}")
    snippet = items[0].get("snippet", {})
    return {
        "id": video_id,
        "title": snippet.get("title", "").strip(),
        "description": snippet.get("description", "").strip(),
        "position": 0,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
    }


from apps.content.services.resource_copy import build_resource_copy, clean_video_title


def get_or_create_area(name, description=""):
    area = Area.objects.filter(name__iexact=name).first()
    if area:
        changed = False
        if not area.description and description:
            area.description = description
            changed = True
        if not area.is_active:
            area.is_active = True
            changed = True
        if changed:
            area.save()
        return area, False
    return Area.objects.create(
        name=name,
        description=description or f"Recursos, asignaturas y rutas de aprendizaje de {name}.",
        is_active=True,
    ), True


def get_or_create_subject(name, area, description=""):
    subject = Subject.objects.filter(name__iexact=name).first()
    if subject:
        changed = False
        if subject.area_id != area.id:
            subject.area = area
            changed = True
        if not subject.description and description:
            subject.description = description
            changed = True
        if not subject.is_active:
            subject.is_active = True
            changed = True
        if changed:
            subject.save()
        return subject, False
    return Subject.objects.create(
        name=name,
        area=area,
        description=description or f"Recursos y temas de {name} organizados para clases particulares.",
        is_active=True,
    ), True


def get_or_create_topic(name, subject, description=""):
    topic = Topic.objects.filter(subject=subject, name__iexact=name).first()
    if topic:
        changed = False
        if not topic.description and description:
            topic.description = description
            changed = True
        if topic.resource_ordering_method != "manual":
            topic.resource_ordering_method = "manual"
            changed = True
        if not topic.is_active:
            topic.is_active = True
            changed = True
        if changed:
            topic.save()
        return topic, False
    return Topic.objects.create(
        name=name,
        subject=subject,
        description=description or f"Ruta de aprendizaje con recursos sobre {name}.",
        resource_ordering_method="manual",
        is_active=True,
    ), True


class Command(BaseCommand):
    help = "Importa videos o playlists de YouTube y crea area, asignatura, tema y recursos asociados."

    def add_arguments(self, parser):
        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument("--playlist-url")
        source.add_argument("--playlist-id")
        source.add_argument("--video-url", action="append", default=[])
        parser.add_argument("--area", required=True)
        parser.add_argument("--subject", required=True)
        parser.add_argument("--topic", required=True)
        parser.add_argument("--area-description", default="")
        parser.add_argument("--subject-description", default="")
        parser.add_argument("--topic-description", default="")
        parser.add_argument("--level", action="append", default=[])
        parser.add_argument("--youtube-api-key", default="")
        parser.add_argument("--limit", type=int)
        parser.add_argument("--draft", action="store_true")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--keep-existing-copy", action="store_true")

    def handle(self, *args, **options):
        api_key = options["youtube_api_key"] or os.environ.get("YOUTUBE_API_KEY", "")
        if not api_key:
            raise CommandError("Configura YOUTUBE_API_KEY o usa --youtube-api-key.")

        if options["playlist_url"] or options["playlist_id"]:
            playlist_id = extract_playlist_id(options["playlist_url"] or options["playlist_id"])
            videos = fetch_playlist_videos(playlist_id, api_key, limit=options["limit"])
        else:
            videos = []
            for video_url in options["video_url"]:
                video_id = extract_video_id(video_url)
                if not video_id:
                    raise CommandError(f"URL de video invalida: {video_url}")
                videos.append(fetch_single_video(video_id, api_key))

        if not videos:
            raise CommandError("No se encontraron videos importables.")

        if options["dry_run"]:
            self.stdout.write(f"Dry run: se importarian {len(videos)} recursos.")
            for video in videos:
                self.stdout.write(f"- {clean_video_title(video['title'])} ({video['video_url']})")
            return

        with transaction.atomic():
            area, area_created = get_or_create_area(
                options["area"],
                options["area_description"],
            )
            subject, subject_created = get_or_create_subject(
                options["subject"],
                area,
                options["subject_description"],
            )
            topic, topic_created = get_or_create_topic(
                options["topic"],
                subject,
                options["topic_description"],
            )

            levels = []
            for level_name in options["level"]:
                level, _created = Level.objects.get_or_create(
                    name=level_name,
                    defaults={"is_active": True},
                )
                levels.append(level)

            created_count = 0
            updated_count = 0
            for index, video in enumerate(videos, start=1):
                existing_resource = Resource.objects.filter(video_url__contains=video["id"]).first()
                description, content = build_resource_copy(video, subject, topic)

                defaults = {
                    "title": video["title"],
                    "subject": subject,
                    "topic": topic,
                    "video_url": video["video_url"],
                    "is_published": not options["draft"],
                    "order": video.get("position", index - 1) + 1,
                }
                if not options["keep_existing_copy"] or not existing_resource:
                    defaults["description"] = description
                    defaults["content"] = content

                if existing_resource:
                    for field, value in defaults.items():
                        setattr(existing_resource, field, value)
                    existing_resource.save()
                    resource = existing_resource
                    updated_count += 1
                else:
                    resource = Resource.objects.create(**defaults)
                    created_count += 1

                if levels:
                    resource.levels.set(levels)

        self.stdout.write(self.style.SUCCESS("Importacion completada."))
        self.stdout.write(f"Area: {area.name} ({reverse('content:area_detail', args=[area.slug])})")
        self.stdout.write(f"Asignatura: {subject.name} ({reverse('content:subject_detail', args=[subject.slug])})")
        self.stdout.write(f"Tema: {topic.name} ({reverse('content:topic_detail', args=[topic.slug])})")
        self.stdout.write(
            f"Creados: {created_count}. Actualizados: {updated_count}. "
            f"Area nueva: {area_created}. Asignatura nueva: {subject_created}. Tema nuevo: {topic_created}."
        )
