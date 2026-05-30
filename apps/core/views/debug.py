from django.http import Http404


def trigger_error(request):
    """TEMPORAL: lanza un error a propósito para verificar que Sentry captura
    los errores. Solo accesible para superusuarios; cualquier otro recibe 404.
    Eliminar esta vista y su URL una vez confirmado que Sentry funciona.
    """
    if not request.user.is_superuser:
        raise Http404

    division_by_zero = 1 / 0  # noqa: F841
    return None
