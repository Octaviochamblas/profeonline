import sys
from django.db import migrations
from django.utils.text import slugify

def populate_resources(apps, schema_editor):
    if 'test' in sys.argv:
        return

    Area = apps.get_model('content', 'Area')
    Subject = apps.get_model('content', 'Subject')
    Topic = apps.get_model('content', 'Topic')
    Resource = apps.get_model('content', 'Resource')

    area, _ = Area.objects.get_or_create(
        name="Matemáticas",
        defaults={"is_active": True}
    )

    subject, _ = Subject.objects.get_or_create(
        name="Matemáticas Escolar",
        defaults={"area": area, "is_active": True}
    )

    topic_enteros, _ = Topic.objects.get_or_create(
        name="Números Enteros",
        subject=subject,
        defaults={"is_active": True, "resource_ordering_method": "manual"}
    )

    topic_racionales, _ = Topic.objects.get_or_create(
        name="Números Racionales",
        subject=subject,
        defaults={"is_active": True, "resource_ordering_method": "manual"}
    )

    videos = [
      {"id": "rFwyRipjDOY", "title": "1.1 Qué son los Números"},
      {"id": "yfUsZZrL7PA", "title": "1.2 Conjuntos Numéricos"},
      {"id": "khau52eLlCQ", "title": "1.3 Números Enteros: Relaciones de Orden - Mayor, menor e igual"},
      {"id": "EkcPbQAz1I4", "title": "1.4 Valor Absoluto - Relaciones de orden"},
      {"id": "RVj8kW9QjSI", "title": "1.5 Regla de Signos para Sumas/Restas"},
      {"id": "vHWVe72pVc0", "title": "1.5a Ejercicios de Sumas y Restas - Aplicación de Regla de los Signos"},
      {"id": "GGc-UZRUD90", "title": "1.6 Regla de los signos en Multiplicación/División - Ejemplos"},
      {"id": "j1EyI6Or4vQ", "title": "1.7 Prioridad de Operaciones - Suma/Resta/Multiplicación/División Combinadas"},
      {"id": "UzkH1lrlJ6w", "title": "1.8 Números Primos - Múltiplos y divisores"},
      {"id": "2Kk55AKkvyw", "title": "1.9 Mínimo Común Múltiplo - Máximo Común Divisor"},
      {"id": "zb1m0mWyJCE", "title": "1.9a Ejercicios: Mínimo Común Múltiplo"},
      {"id": "rj4nGGjG6LI", "title": "2.0 Números Racionales, fraciones propias, impropias y  números mixtos"},
      {"id": "q6yVrqXxksI", "title": "2.01 Números Racionales - Conversión de decimales finitos, periodicos y semi-periodicos a Fracción"},
      {"id": "T-13XXsc6Yo", "title": "2.01a EJERCICIOS: Conversión de decimales finitos, periodicos y semi-periodicos a Fracción"},
      {"id": "E-ODudw9TyI", "title": "2.02 Números Racionales - Sumas y Restas de números decimales"},
      {"id": "Ud9_iYwVpXk", "title": "2.02A EJERCICIOS:  Números Racionales - Sumas y Restas de números decimales"},
      {"id": "ZZLf3ENqI3Y", "title": "2.03 Números Racionales: Multiplicacion de números decimales"},
      {"id": "8Bg-0hdKMF8", "title": "2.03a EJERCICIOS: Nodos Racionales: Multiplicación de Decimales"},
      {"id": "g8xtA3qJ_rY", "title": "2.04 Nodos Racionales: División de números Decimales"},
      {"id": "5GIVrWKXvnA", "title": "2.04a EJERCICIOS: Números Racionales - División de decimales"},
      {"id": "pRoEh3n-m9A", "title": "2.05 Números Racionales: Qué son las fracciones - Simplificación Fracciones"},
      {"id": "noyswbD3J5M", "title": "2.05A EJERCICIOS: Números Racionales - Operaciones Combinadas - ProfeOnline.cl"},
      {"id": "U9FgyQbsYn0", "title": "2.06 Números Racionales: Multiplicación y División de Fracciones"},
      {"id": "w12XrOiqX3Q", "title": "2.06a EJERCICIOS: Números Racionales: Multiplicación con simplificación - ProfeOnline.cl"},
      {"id": "McsEHWZprJM", "title": "2 07 Números Racionales Suma y Resta de Fracciones"},
      {"id": "HeTkV_MZDMk", "title": "2 07a EJERCICIOS: Suma y Resta de FRACCIONES | @ProfeOnline.cl"},
      {"id": "DTLA0HU2MJw", "title": "2.08 Números Racionales: Prioridad en las Operaciones"}
    ]

    for idx, video in enumerate(videos):
        video_id = video["id"]
        title = video["title"]

        if title.startswith("1"):
            topic = topic_enteros
        elif title.startswith("2"):
            topic = topic_racionales
        else:
            continue

        url = f"https://www.youtube.com/watch?v={video_id}"

        slug = slugify(title)
        base_slug = slug
        counter = 1
        while Resource.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Resource.objects.get_or_create(
            title=title,
            defaults={
                "subject": subject,
                "topic": topic,
                "video_url": url,
                "is_published": True,
                "content": f"Video explicativo paso a paso sobre: {title}. Suscríbete y aprende en ProfeOnline.cl.",
                "order": idx + 1,
                "slug": slug
            }
        )

def rollback_resources(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_alter_resource_order'),
    ]

    operations = [
        migrations.RunPython(populate_resources, rollback_resources),
    ]
