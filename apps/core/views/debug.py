from django.http import HttpResponse


def trigger_error(request):
    """TEMPORAL: diagnóstico de Sentry.

    - Si Sentry NO está inicializado (falta SENTRY_DSN), devuelve un mensaje
      claro en vez de un 500, para saber que el problema es la variable.
    - Si SÍ está inicializado, envía un mensaje de prueba y lanza un error
      para que aparezca en Sentry.

    Eliminar esta vista y su URL una vez confirmado que Sentry funciona.
    """
    import sentry_sdk

    client = sentry_sdk.get_client()
    if not client.is_active():
        return HttpResponse(
            "Sentry NO esta inicializado: la variable SENTRY_DSN no esta "
            "configurada o no se esta leyendo en este deploy.",
            content_type="text/plain; charset=utf-8",
        )

    sentry_sdk.capture_message("debug-sentry: mensaje de prueba")
    raise Exception("Error de prueba para Sentry (debug-sentry)")
