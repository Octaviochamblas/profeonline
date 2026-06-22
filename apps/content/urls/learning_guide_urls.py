from django.urls import path
from apps.content.views.learning_guide_student import (
    learning_guide_detail,
    start_visible_practice,
    submit_visible_practice,
)

urlpatterns = [
    path("guias/<slug:slug>/", learning_guide_detail, name="learning_guide_detail"),
    path("practica-visible/<int:topic_id>/", start_visible_practice, name="start_visible_practice"),
    path("practica-visible/<int:topic_id>/enviar/", submit_visible_practice, name="submit_visible_practice"),
]
