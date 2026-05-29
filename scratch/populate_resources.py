import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from apps.content.models import Area, Subject, Topic, Resource

# 1. Get or create Area
area, _ = Area.objects.get_or_create(
    name="Matemáticas",
    defaults={"is_active": True}
)

# 2. Get or create Subject
subject, _ = Subject.objects.get_or_create(
    name="Matemáticas Escolar",
    defaults={"area": area, "is_active": True}
)

# 3. Get or create Topics
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

# Videos list
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

    # Determine topic
    if title.startswith("1"):
        topic = topic_enteros
    elif title.startswith("2"):
        topic = topic_racionales
    else:
        continue # skip if doesn't match

    url = f"https://www.youtube.com/watch?v={video_id}"

    resource, created = Resource.objects.get_or_create(
        title=title,
        defaults={
            "subject": subject,
            "topic": topic,
            "video_url": url,
            "is_published": True,
            "content": f"Video explicativo paso a paso sobre: {title}. Suscríbete y aprende en ProfeOnline.cl.",
            "order": idx + 1
        }
    )
    if created:
        print(f"Created resource: {title}")
    else:
        print(f"Resource already exists: {title}")
