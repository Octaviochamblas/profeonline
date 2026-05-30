import sys

from django.db import migrations
from django.utils.text import slugify


VIDEO_ID = "3iuyMwqAFbM"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
TITLE = "Mecánica: Dinámica en Plano Inclinado con Cuerda y Roce | DCL, Newton, m3 y Tensión Paso a Paso"


def unique_slug(model, value, instance_pk=None):
    base_slug = slugify(value) or "contenido"
    slug = base_slug
    counter = 1
    queryset = model.objects.all()
    if instance_pk:
        queryset = queryset.exclude(pk=instance_pk)

    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def ensure_slug(instance, model, value):
    if not instance.slug:
        instance.slug = unique_slug(model, value, instance.pk)
        instance.save(update_fields=["slug"])
    return instance


def get_or_create_named(model, name, defaults=None):
    defaults = defaults or {}
    instance = model.objects.filter(name__iexact=name).first()
    created = False
    if not instance:
        instance = model.objects.create(name=name, **defaults)
        created = True
    return instance, created


def add_mechanics_forces_video(apps, schema_editor):
    if "test" in sys.argv:
        return

    Area = apps.get_model("content", "Area")
    Subject = apps.get_model("content", "Subject")
    Topic = apps.get_model("content", "Topic")
    Level = apps.get_model("content", "Level")
    Resource = apps.get_model("content", "Resource")

    area, _created = get_or_create_named(
        Area,
        "Física",
        {
            "description": "Recursos, asignaturas y rutas de aprendizaje para estudiar fenomenos fisicos, fuerzas y movimiento.",
            "is_active": True,
            "order": 2,
            "slug": unique_slug(Area, "Física"),
        },
    )
    area.is_active = True
    if not area.description:
        area.description = "Recursos, asignaturas y rutas de aprendizaje para estudiar fenomenos fisicos, fuerzas y movimiento."
    ensure_slug(area, Area, area.name)
    area.save()

    subject, _created = get_or_create_named(
        Subject,
        "Mecánica",
        {
            "area": area,
            "description": "Contenidos de mecanica clasica para estudiar fuerzas, equilibrio, dinamica y movimiento.",
            "is_active": True,
            "slug": unique_slug(Subject, "Mecánica"),
        },
    )
    subject.area = area
    subject.is_active = True
    if not subject.description:
        subject.description = "Contenidos de mecanica clasica para estudiar fuerzas, equilibrio, dinamica y movimiento."
    ensure_slug(subject, Subject, subject.name)
    subject.save()

    topic = Topic.objects.filter(subject=subject, name__iexact="Fuerzas").first()
    if not topic:
        topic = Topic.objects.create(
            subject=subject,
            name="Fuerzas",
            slug=unique_slug(Topic, "Fuerzas"),
            description="Ruta de aprendizaje sobre diagramas de cuerpo libre, tension, roce y leyes de Newton.",
            resource_ordering_method="manual",
            is_active=True,
        )
    topic.subject = subject
    topic.is_active = True
    topic.resource_ordering_method = "manual"
    if not topic.description:
        topic.description = "Ruta de aprendizaje sobre diagramas de cuerpo libre, tension, roce y leyes de Newton."
    ensure_slug(topic, Topic, topic.name)
    topic.save()

    level, _created = get_or_create_named(
        Level,
        "Universitario",
        {
            "description": "Apoyo academico y materias avanzadas para educacion superior.",
            "is_active": True,
            "order": 3,
            "slug": unique_slug(Level, "Universitario"),
        },
    )
    level.is_active = True
    if not level.description:
        level.description = "Apoyo academico y materias avanzadas para educacion superior."
    ensure_slug(level, Level, level.name)
    level.save()

    description = (
        "Resuelve un problema de dinamica en plano inclinado con cuerda, roce, tension y diagrama de cuerpo libre, "
        "aplicando las leyes de Newton dentro del tema Fuerzas."
    )
    content = f"""### Sobre este recurso
Este recurso trabaja un problema de **dinamica en plano inclinado con cuerda y roce** dentro del tema **Fuerzas** en la asignatura **Mecánica**.

### Que aprenderas
- Construir diagramas de cuerpo libre para sistemas conectados por cuerda.
- Aplicar las leyes de Newton en ejes paralelos y perpendiculares al plano inclinado.
- Relacionar tension, roce y masa para resolver el sistema paso a paso.

### Video
[Ver este recurso en YouTube]({VIDEO_URL})
"""

    resource = Resource.objects.filter(video_url__contains=VIDEO_ID).first()
    if not resource:
        resource = Resource(slug=unique_slug(Resource, TITLE))

    resource.title = TITLE
    resource.subject = subject
    resource.topic = topic
    resource.video_url = VIDEO_URL
    resource.description = description
    resource.content = content
    resource.is_published = True
    resource.order = 1
    ensure_slug(resource, Resource, resource.title)
    resource.save()
    resource.levels.set([level])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_make_topic_slugs_globally_unique"),
    ]

    operations = [
        migrations.RunPython(add_mechanics_forces_video, noop_reverse),
    ]
