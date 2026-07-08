from django.urls import path

from . import views
from . import assessment_views

app_name = "learn"

urlpatterns = [
    path("", views.learn_home, name="home"),
    path("<slug:asignatura_slug>/", views.node_view, name="asignatura"),
    path("<slug:asignatura_slug>/<slug:eje_slug>/", views.node_view, name="eje"),
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/",
        views.node_view,
        name="bloque",
    ),
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/",
        views.node_view,
        name="tema",
    ),
    # Rutas de evaluación de nodo (deben ir ANTES de la ruta de recurso genérica)
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/<slug:recurso_slug>/evaluar/",
        assessment_views.node_assessment_status,
        name="assessment_status",
    ),
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/<slug:recurso_slug>/evaluar/<int:level>/",
        assessment_views.node_assessment_start,
        name="assessment_start",
    ),
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/<slug:recurso_slug>/evaluar/<int:level>/enviar/",
        assessment_views.node_assessment_submit,
        name="assessment_submit",
    ),
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/<slug:recurso_slug>/",
        views.node_view,
        name="recurso",
    ),
]
