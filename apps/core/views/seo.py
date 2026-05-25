from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("core:sitemap"))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /cuentas/",
        "Disallow: */crear/",
        "Disallow: */editar/",
        "Disallow: */eliminar/",
        "Disallow: */opciones/",
        "Allow: /",
        f"Sitemap: {sitemap_url}",
        "",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")
