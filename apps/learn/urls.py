from django.urls import path

from . import views

app_name = "learn"

urlpatterns = [
    path(
        "contenido/<int:node_id>/editar/",
        views.edit_node_content,
        name="edit_node_content",
    ),
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
    path(
        "<slug:asignatura_slug>/<slug:eje_slug>/<slug:bloque_slug>/<slug:tema_slug>/<slug:recurso_slug>/",
        views.node_view,
        name="recurso",
    ),
]
