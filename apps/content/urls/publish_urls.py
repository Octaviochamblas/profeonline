from django.urls import path
from apps.content.views import (
    publish_studio,
    subject_options,
    module_options,
    publish_inline_create,
)
from apps.content.views.question_studio import (
    question_studio,
    generate_questions_chunk,
)
from apps.content.views.question_review import (
    question_review,
    save_resource_quiz_config,
    edit_question_inline,
    edit_choice_inline,
    add_question_inline,
    add_choice_inline,
    delete_question,
    delete_choice,
    bulk_action_questions,
    generate_questions_inline,
)
from apps.content.views.quiz_guides import (
    quiz_guides,
    delete_quiz_guide,
    import_drive_guides,
)
from apps.content.views.bank_analytics import (
    bank_coverage,
    bank_effectiveness,
    bank_results,
)

urlpatterns = [
    path("publicar/estudio/", publish_studio, name="publish_studio"),
    path("publicar/opciones/asignaturas/", subject_options, name="subject_options"),
    path("publicar/opciones/modulos/", module_options, name="module_options"),
    path("publicar/crear/<str:entity_type>/", publish_inline_create, name="publish_inline_create"),

    # Banco de Preguntas - Estudio de generación
    path("publicar/preguntas/", question_studio, name="question_studio"),
    path("publicar/preguntas/generar-tanda/", generate_questions_chunk, name="generate_questions_chunk"),
    path("publicar/preguntas/resumen/", bank_coverage, name="bank_coverage"),
    path("publicar/preguntas/resultados/", bank_results, name="bank_results"),
    path(
        "publicar/preguntas/efectividad/",
        bank_effectiveness,
        name="bank_effectiveness",
    ),

    # Banco de Preguntas - Biblioteca de guías de referencia
    path("publicar/guias/", quiz_guides, name="quiz_guides"),
    path("publicar/guias/borrar/<int:guide_id>/", delete_quiz_guide, name="delete_quiz_guide"),
    path("publicar/guias/importar-drive/", import_drive_guides, name="import_drive_guides"),

    # Banco de Preguntas - Revisión y Configuración por Recurso
    path("publicar/preguntas/<slug:slug>/", question_review, name="question_review"),
    path("publicar/preguntas/config/<int:resource_id>/", save_resource_quiz_config, name="save_resource_quiz_config"),
    path("publicar/preguntas/editar/<int:question_id>/", edit_question_inline, name="edit_question_inline"),
    path("publicar/preguntas/alternativa/<int:choice_id>/", edit_choice_inline, name="edit_choice_inline"),
    path("publicar/preguntas/crear-pregunta/<int:resource_id>/", add_question_inline, name="add_question_inline"),
    path("publicar/preguntas/crear-alternativa/<int:question_id>/", add_choice_inline, name="add_choice_inline"),
    path("publicar/preguntas/borrar-pregunta/<int:question_id>/", delete_question, name="delete_question"),
    path("publicar/preguntas/borrar-alternativa/<int:choice_id>/", delete_choice, name="delete_choice"),
    path("publicar/preguntas/accion-lote/<int:resource_id>/", bulk_action_questions, name="bulk_action_questions"),
    path("publicar/preguntas/generar-inline/<int:resource_id>/", generate_questions_inline, name="generate_questions_inline"),
]
