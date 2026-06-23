"""Editorial generation for the hidden structured evaluation pools."""

from apps.content.services.visible_bank_service import generate_visible_bank_questions

EVALUATION_SCOPES = {"evaluacion_nivel", "prueba_final"}


def generate_evaluation_bank_questions(
    *,
    exercise_item,
    resource,
    learning_guide,
    scope,
    count=None,
    api_key=None,
):
    """Generate draft questions for one hidden pool without duplicating AI plumbing."""
    if scope not in EVALUATION_SCOPES:
        raise ValueError("El ámbito debe ser evaluacion_nivel o prueba_final.")
    return generate_visible_bank_questions(
        exercise_item=exercise_item,
        resource=resource,
        learning_guide=learning_guide,
        count=count,
        api_key=api_key,
        scope=scope,
    )
