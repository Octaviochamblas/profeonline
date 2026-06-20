from datetime import datetime, timezone
import hashlib

from django.db import migrations, models


AUDITED_AT = datetime(2026, 6, 20, tzinfo=timezone.utc).isoformat()


def backfill_editorial_audit(apps, schema_editor):
    Resource = apps.get_model("content", "Resource")
    for resource in Resource.objects.filter(is_published=True).iterator():
        transcript = (resource.transcript or "").strip()
        has_transcript = len(transcript.split()) >= 50
        has_video = bool((resource.video_url or "").strip())
        resource.editorial_audit = {
            "schema_version": 1,
            "audited_at": AUDITED_AT,
            "audit_source": "global_transcript_audit_2026_06_20",
            "requires_reaudit": not (has_transcript and has_video),
            "transcript": {
                "available": has_transcript,
                "audited": has_transcript,
                "words": len(transcript.split()),
                "sha256": (
                    hashlib.sha256(transcript.encode("utf-8")).hexdigest()
                    if transcript
                    else ""
                ),
            },
            "web": {
                "title_audited": has_transcript,
                "description_audited": has_transcript
                and bool((resource.description or "").strip()),
            },
            "youtube": {
                "title_audited": has_transcript and has_video,
                "description_audited": has_transcript and has_video,
                "verified": has_transcript and has_video,
            },
        }
        resource.save(update_fields=["editorial_audit"])


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0029_publication_pipeline"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="editorial_audit",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text=(
                    "Estado verificable de transcripción, títulos y descripciones "
                    "de la web y YouTube."
                ),
                verbose_name="Auditoría editorial",
            ),
        ),
        migrations.RunPython(
            backfill_editorial_audit,
            migrations.RunPython.noop,
        ),
    ]
