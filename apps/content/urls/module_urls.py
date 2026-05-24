from django.urls import path
from apps.content.views import (
    ModuleCreateView,
    ModuleDeleteView,
    ModuleListView,
    ModuleUpdateView,
    module_resource_add,
    module_resource_list,
    module_resource_remove,
)

urlpatterns = [
    path("modulos/", ModuleListView.as_view(), name="module_list"),
    path("modulos/crear/", ModuleCreateView.as_view(), name="module_create"),
    path("modulos/<int:pk>/editar/", ModuleUpdateView.as_view(), name="module_update"),
    path("modulos/<int:pk>/eliminar/", ModuleDeleteView.as_view(), name="module_delete"),
    path("modulos/<int:module_id>/recursos/", module_resource_list, name="module_resource_list"),
    path("modulos/<int:module_id>/recursos/agregar/", module_resource_add, name="module_resource_add"),
    path("modulos/<int:module_id>/recursos/quitar/", module_resource_remove, name="module_resource_remove"),
]
