import re

def clean_video_title(title):
    if not title:
        return ""
    clean_title = re.sub(
        r"^\s*(?:clase\s*)?\d+(?:[.\s_-]\d+)*(?:[a-zA-Z])?[\s).:-]+",
        "",
        title,
        flags=re.IGNORECASE,
    )
    clean_title = re.sub(r"\s*(?:-|\|)?\s*@?ProfeOnline(?:\.cl)?\s*$", "", clean_title, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", clean_title).strip() or title.strip()


def build_resource_copy(video, subject, topic):
    clean_title = clean_video_title(video.get("title", ""))
    is_exercise = "ejercicio" in clean_title.lower() or "ejercicios" in clean_title.lower()

    subject_name = getattr(subject, "name", "")
    topic_name = getattr(topic, "name", "")

    if is_exercise:
        description = (
            f"Practica {clean_title} dentro del tema {topic_name}. "
            f"Recurso de {subject_name} enfocado en resolver procedimientos paso a paso."
        )
        focus = "ejercicios resueltos y estrategias de desarrollo"
    else:
        description = (
            f"Aprende {clean_title} dentro del tema {topic_name}. "
            f"Recurso de {subject_name} para comprender conceptos clave antes de avanzar."
        )
        focus = "conceptos principales, ejemplos y conexiones con el tema"

    content = f"""### Sobre este recurso
Este recurso aborda **{clean_title}** como parte del tema **{topic_name}** en la asignatura **{subject_name}**.

### Que encontraras
- Explicacion centrada en {focus}.
- Relacion directa con la ruta de aprendizaje de {topic_name}.
- Material pensado para reforzar el estudio antes o despues de una clase particular.
"""

    video_url = video.get("video_url")
    if video_url:
        content += f"""
### Video
[Ver este recurso en YouTube]({video_url})
"""

    return description, content
