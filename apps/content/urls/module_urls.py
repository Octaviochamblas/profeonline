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
    path("modules/", ModuleListView.as_view(), name="module_list"),
    path("modules/create/", ModuleCreateView.as_view(), name="module_create"),
    path("modules/<int:pk>/edit/", ModuleUpdateView.as_view(), name="module_update"),
    path("modules/<int:pk>/delete/", ModuleDeleteView.as_view(), name="module_delete"),
    path("modules/<int:module_id>/resources/", module_resource_list, name="module_resource_list"),
    path("modules/<int:module_id>/resources/add/", module_resource_add, name="module_resource_add"),
    path("modules/<int:module_id>/resources/remove/", module_resource_remove, name="module_resource_remove"),
]