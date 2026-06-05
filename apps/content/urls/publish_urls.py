from django.urls import path
from apps.content.views import (
    publish_studio,
    subject_options,
    module_options,
    publish_inline_create,
)

urlpatterns = [
    path("publicar/estudio/", publish_studio, name="publish_studio"),
    path("publicar/opciones/asignaturas/", subject_options, name="subject_options"),
    path("publicar/opciones/modulos/", module_options, name="module_options"),
    path("publicar/crear/<str:entity_type>/", publish_inline_create, name="publish_inline_create"),
]
