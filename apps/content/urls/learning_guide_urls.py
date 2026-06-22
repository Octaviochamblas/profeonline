from django.urls import path
from apps.content.views.learning_guide_student import (
    learning_guide_detail,
    start_visible_practice,
    submit_visible_practice,
)
from apps.content.views.structured_evaluation import (
    start_structured_evaluation,
    submit_structured_evaluation,
)

urlpatterns = [
    path("guias/<slug:slug>/", learning_guide_detail, name="learning_guide_detail"),
    path("practica-visible/<int:topic_id>/", start_visible_practice, name="start_visible_practice"),
    path("practica-visible/<int:topic_id>/enviar/", submit_visible_practice, name="submit_visible_practice"),
    path("evaluacion-estructurada/<int:topic_id>/", start_structured_evaluation, name="start_structured_evaluation"),
    path("evaluacion-estructurada/sesion/<int:session_id>/enviar/", submit_structured_evaluation, name="submit_structured_evaluation"),
]
