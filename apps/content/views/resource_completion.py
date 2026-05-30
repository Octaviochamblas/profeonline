from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from apps.content.models import Resource, ResourceCompletion


@login_required
@require_POST
def toggle_resource_completion(request, slug):
    """Marca o desmarca un recurso como completado para el usuario actual."""
    resource = get_object_or_404(Resource, slug=slug, is_published=True)

    completion = ResourceCompletion.objects.filter(
        user=request.user, resource=resource
    ).first()

    if completion:
        completion.delete()
        completed = False
    else:
        ResourceCompletion.objects.get_or_create(user=request.user, resource=resource)
        completed = True

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "includes/completion_button.html",
            {"resource": resource, "completed": completed},
            request=request,
        )
        return HttpResponse(html)

    return redirect("content:resource_detail", slug=resource.slug)
