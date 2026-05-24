import json

from django.urls import reverse


def breadcrumb_schema(items):
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index + 1,
                    "name": item["label"],
                    "item": item["url"],
                }
                for index, item in enumerate(items)
                if item.get("url")
            ],
        },
        ensure_ascii=False,
    )


def article_schema(resource, canonical_url, subject_name=None):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": resource.title,
        "description": resource.description or "",
        "inLanguage": "es-CL",
        "datePublished": resource.created_at.isoformat(),
        "dateModified": resource.created_at.isoformat(),
        "mainEntityOfPage": canonical_url,
    }

    if subject_name:
        data["articleSection"] = subject_name

    keywords = []
    if resource.topic:
        keywords.append(resource.topic.name)
    keywords.extend(level.name for level in resource.levels.all())
    if keywords:
        data["keywords"] = keywords

    return json.dumps(data, ensure_ascii=False)


def build_breadcrumbs(request, *pairs):
    breadcrumbs = [
        {"label": "Inicio", "url": request.build_absolute_uri(reverse("core:home"))},
    ]

    for label, url_name, kwargs in pairs:
        breadcrumbs.append(
            {
                "label": label,
                "url": request.build_absolute_uri(reverse(url_name, kwargs=kwargs)) if url_name else None,
            }
        )

    return breadcrumbs
