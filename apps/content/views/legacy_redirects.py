from django.shortcuts import get_object_or_404, redirect

from apps.content.models import Level, Resource, Subject


def legacy_subject_detail_redirect(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return redirect("content:subject_detail", slug=subject.slug, permanent=True)


def legacy_level_detail_redirect(request, pk):
    level = get_object_or_404(Level, pk=pk)
    return redirect("content:level_detail", slug=level.slug, permanent=True)


def legacy_resource_detail_redirect(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return redirect("content:resource_detail", slug=resource.slug, permanent=True)


def legacy_resource_update_redirect(request, pk):
    return redirect("content:resource_update", pk=pk, permanent=True)


def legacy_resource_delete_redirect(request, pk):
    return redirect("content:resource_delete", pk=pk, permanent=True)


def legacy_subject_update_redirect(request, pk):
    return redirect("content:subject_update", pk=pk, permanent=True)


def legacy_subject_delete_redirect(request, pk):
    return redirect("content:subject_delete", pk=pk, permanent=True)


def legacy_level_update_redirect(request, pk):
    return redirect("content:level_update", pk=pk, permanent=True)


def legacy_level_delete_redirect(request, pk):
    return redirect("content:level_delete", pk=pk, permanent=True)


def legacy_module_update_redirect(request, pk):
    return redirect("content:module_update", pk=pk, permanent=True)


def legacy_module_delete_redirect(request, pk):
    return redirect("content:module_delete", pk=pk, permanent=True)


def legacy_module_resources_redirect(request, module_id):
    return redirect("content:module_resource_list", module_id=module_id, permanent=True)


def legacy_module_resource_add_redirect(request, module_id):
    return redirect("content:module_resource_add", module_id=module_id, permanent=True)


def legacy_module_resource_remove_redirect(request, module_id):
    return redirect("content:module_resource_remove", module_id=module_id, permanent=True)


def legacy_topic_update_redirect(request, pk):
    return redirect("content:topic_update", pk=pk, permanent=True)


def legacy_topic_delete_redirect(request, pk):
    return redirect("content:topic_delete", pk=pk, permanent=True)
