from django.http import HttpResponse
from django.urls import reverse


SITEMAP_URL_NAMES = [
    "core:home",
    "content:resource_list",
    "content:area_list",
    "content:subject_list",
    "content:topic_list",
    "content:level_list",
    "content:module_list",
]


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("core:sitemap"))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /cuentas/",
        "Allow: /",
        f"Sitemap: {sitemap_url}",
        "",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    urls = []

    for url_name in SITEMAP_URL_NAMES:
        location = request.build_absolute_uri(reverse(url_name))
        urls.append(
            "  <url>\n"
            f"    <loc>{location}</loc>\n"
            "    <changefreq>weekly</changefreq>\n"
            "    <priority>0.7</priority>\n"
            "  </url>"
        )

    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )

    return HttpResponse(content, content_type="application/xml")
