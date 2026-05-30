def trigger_error(request):
    """TEMPORAL: lanza un error a propósito para verificar que Sentry captura
    los errores en producción. Eliminar esta vista y su URL una vez confirmado
    que Sentry funciona.
    """
    division_by_zero = 1 / 0  # noqa: F841
    return None
