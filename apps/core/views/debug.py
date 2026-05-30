from django.http import HttpResponse


def trigger_error(request):
    """TEMPORAL: diagnóstico de Sentry. Eliminar tras verificar.

    - Sin SENTRY_DSN activo: avisa que falta la variable.
    - Con SENTRY_DSN activo: muestra a qué host/proyecto apunta el DSN
      (datos no secretos) para verificar que sea el proyecto correcto.
    - Con ?raise=1: además lanza un error de prueba real.
    """
    import sentry_sdk

    client = sentry_sdk.get_client()
    if not client.is_active():
        return HttpResponse(
            "Sentry NO esta inicializado: falta la variable SENTRY_DSN.",
            content_type="text/plain; charset=utf-8",
        )

    try:
        parsed = client.transport.parsed_dsn
        host = parsed.host
        project_id = parsed.project_id
    except Exception as exc:  # pragma: no cover
        host, project_id = "desconocido", f"error: {exc}"

    if request.GET.get("raise"):
        sentry_sdk.capture_message("debug-sentry: mensaje de prueba")
        raise Exception("Error de prueba para Sentry (debug-sentry)")

    return HttpResponse(
        f"Sentry ACTIVO.\nhost={host}\nproject_id={project_id}\n\n"
        f"(Anade ?raise=1 a la URL para lanzar un error de prueba.)",
        content_type="text/plain; charset=utf-8",
    )
