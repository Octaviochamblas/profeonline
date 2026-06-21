from django.db import migrations

from apps.content.services.title_cleanup_service import clean_resource_title_v1


def clean_existing_titles(apps, schema_editor):
    Resource = apps.get_model("content", "Resource")
    resources = Resource.objects.select_related("subject", "topic").all()

    for resource in resources.iterator():
        cleaned = clean_resource_title_v1(
            resource.title,
            subject_name=resource.subject.name if resource.subject else "",
            topic_name=resource.topic.name if resource.topic else "",
            topic_slug=resource.topic.slug if resource.topic else "",
        )
        if cleaned == resource.title:
            continue

        audit = dict(resource.editorial_audit or {})
        audit.setdefault("web", {})["title_audited"] = False
        audit.setdefault("youtube", {})["title_audited"] = False
        audit["requires_reaudit"] = True
        Resource.objects.filter(pk=resource.pk).update(
            title=cleaned,
            editorial_audit=audit,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0031_subject_education_level"),
    ]

    operations = [
        migrations.RunPython(
            clean_existing_titles,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
