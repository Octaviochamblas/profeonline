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
from apps.content.views.item_review import (
    item_extraction,
    propose_items,
    edit_item_inline,
    set_item_status,
    merge_items,
    link_item_resource,
    unlink_item_resource,
    edit_practice_quota,
    edit_evaluation_quota,
    generate_visible_bank_drafts_view,
    generate_evaluation_bank_drafts_view,
)
from apps.content.views.learning_guide_review import (
    learning_guide_review,
    generate_guide_draft_view,
    edit_guide_draft_view,
    validate_originality_view,
    publish_learning_guide_view,
)
from apps.content.views.structured_activation import (
    activation_panel,
    set_staging,
    activate_structured_bank,
    deactivate_structured_bank,
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

    # Banco de Preguntas - Extracción y Aprobación de Ítems (Fase 1)
    path("publicar/items/", item_extraction, name="item_extraction"),
    path("publicar/items/proponer/", propose_items, name="propose_items"),
    path("publicar/items/editar/<int:item_id>/", edit_item_inline, name="edit_item_inline"),
    path("publicar/items/estado/<int:item_id>/", set_item_status, name="set_item_status"),
    path("publicar/items/fusionar/", merge_items, name="merge_items"),
    path("publicar/items/vincular/<int:item_id>/", link_item_resource, name="link_item_resource"),
    path("publicar/items/desvincular/<int:item_id>/", unlink_item_resource, name="unlink_item_resource"),
    path("publicar/items/cuota/<int:link_id>/", edit_practice_quota, name="edit_practice_quota"),
    path("publicar/items/cuota-evaluacion/<int:link_id>/", edit_evaluation_quota, name="edit_evaluation_quota"),
    path("publicar/items/generar-banco-visible/", generate_visible_bank_drafts_view, name="generate_visible_bank_drafts"),
    path("publicar/items/generar-pool-evaluacion/", generate_evaluation_bank_drafts_view, name="generate_evaluation_bank_drafts"),

    # Guías interactivas - Activación del piloto (Fase 7): staging + gate + flag
    path("publicar/items/activacion/", activation_panel, name="activation_panel"),
    path("publicar/items/activacion/preparar/", set_staging, name="set_staging"),
    path("publicar/items/activacion/activar/", activate_structured_bank, name="activate_structured_bank"),
    path("publicar/items/activacion/desactivar/", deactivate_structured_bank, name="deactivate_structured_bank"),

    # Banco de Preguntas - Guías ProfeOnline Originales + Originalidad (Fase 2)
    path("publicar/guias-profeonline/", learning_guide_review, name="learning_guide_review"),
    path("publicar/guias-profeonline/generar/", generate_guide_draft_view, name="generate_guide_draft_view"),
    path("publicar/guias-profeonline/editar/<int:guide_id>/", edit_guide_draft_view, name="edit_guide_draft_view"),
    path("publicar/guias-profeonline/validar/<int:guide_id>/", validate_originality_view, name="validate_originality_view"),
    path("publicar/guias-profeonline/publicar/<int:guide_id>/", publish_learning_guide_view, name="publish_learning_guide_view"),
]
