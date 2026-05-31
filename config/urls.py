"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Redirige las páginas de recuperación de contraseña de allauth (sin
    # estilo) al flujo propio con el diseño del sitio. Debe ir ANTES del
    # include de allauth para tener prioridad.
    path(
        "accounts/password/reset/",
        RedirectView.as_view(pattern_name="password_reset", permanent=False),
    ),
    path(
        "accounts/password/reset/done/",
        RedirectView.as_view(pattern_name="password_reset_done", permanent=False),
    ),
    # Las páginas de login/registro de allauth (sin estilo) también se
    # redirigen al flujo propio con el diseño del sitio.
    path(
        "accounts/login/",
        RedirectView.as_view(pattern_name="login", permanent=False),
    ),
    path(
        "accounts/signup/",
        RedirectView.as_view(pattern_name="register", permanent=False),
    ),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.content.urls")),
    path("content/", include("apps.content.urls_legacy")),
    path("cuentas/", include("accounts.urls")),
]
