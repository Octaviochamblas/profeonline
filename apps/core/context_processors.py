from django.conf import settings

from apps.content.models import KnowledgeNode


def nav_subjects(request):
    """Asignaturas publicadas, para el menú 'Nodos de Materia'.

    Se arma dinámicamente desde el árbol de conocimiento: al agregar una asignatura
    (Química, Física) al árbol y publicarla, aparece sola en el menú.
    """
    asignaturas = list(
        KnowledgeNode.objects.filter(
            node_type=KnowledgeNode.NODE_ASIGNATURA, is_published=True
        ).order_by("order", "code")
    )
    return {"nav_subjects": asignaturas}


def canonical_settings(request):
    host = request.get_host()
    if settings.DEBUG or "testserver" in host:
        base_url = f"{request.scheme}://{host}"
    else:
        base_url = getattr(settings, "CANONICAL_BASE_URL", "https://www.profeonline.cl")

    return {
        "CANONICAL_BASE_URL": base_url
    }


def csp_nonce(request):
    return {"csp_nonce": getattr(request, "csp_nonce", "")}


def google_login(request):
    enabled = bool(
        getattr(settings, "GOOGLE_CLIENT_ID", "")
        and getattr(settings, "GOOGLE_CLIENT_SECRET", "")
    )
    return {"GOOGLE_LOGIN_ENABLED": enabled}
