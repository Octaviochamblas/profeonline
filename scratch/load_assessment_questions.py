"""Carga preguntas de NodeAssessmentQuestion desde JSON a la BD local (dev).

Uso:
    .venv/Scripts/python.exe scratch/load_assessment_questions.py <semantic_id> <ruta_json>

Fuerza settings.local (nunca production) y es idempotente por nivel: si el nivel
ya tiene >=7 preguntas publicadas, lo salta; si tiene menos de 7 (carga parcial previa),
borra esas preguntas parciales y recarga el nivel completo desde el JSON (evita duplicados
al reintentar sobre un nivel que quedó a medias).
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"
import django

django.setup()

from apps.content.models import KnowledgeNode, NodeAssessmentQuestion, NodeAssessmentChoice


def load_questions(semantic_id, json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    node = KnowledgeNode.objects.get(semantic_id=semantic_id)

    done_levels = set()
    for lvl in (1, 2, 3):
        existing = NodeAssessmentQuestion.objects.filter(node=node, level=lvl, status="publicada")
        if existing.count() >= 7:
            done_levels.add(lvl)
        elif existing.exists():
            existing.delete()  # carga parcial previa: se recarga completa desde el JSON

    created_count = 0
    for q_data in data:
        level = q_data.get("level", 1)
        if level in done_levels:
            continue
        q = NodeAssessmentQuestion.objects.create(
            node=node,
            level=level,
            text=q_data.get("text", ""),
            explanation=q_data.get("explanation", ""),
            status="publicada",
        )
        for choice_data in q_data.get("choices", []):
            NodeAssessmentChoice.objects.create(
                question=q,
                text=choice_data.get("text", ""),
                is_correct=choice_data.get("is_correct", False),
            )
        created_count += 1

    print(f"Loaded {created_count} questions for {semantic_id} (skipped levels: {sorted(done_levels)})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python load_assessment_questions.py <semantic_id> <json_path>")
        sys.exit(1)
    load_questions(sys.argv[1], sys.argv[2])
