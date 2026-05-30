from urllib.parse import urlparse

from django.conf import settings
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .forms import (
    StyledAuthenticationForm,
    StyledPasswordResetForm,
    StyledSetPasswordForm,
)
from .views import register_view, profile_view, profile_update_view

# Construye el enlace del correo de reset desde CANONICAL_BASE_URL en vez de
# depender del dominio del framework Sites (que por defecto es example.com).
# extra_email_context sobreescribe 'domain' y 'protocol' en la plantilla.
_canonical = urlparse(getattr(settings, "CANONICAL_BASE_URL", "https://www.profeonline.cl"))
PASSWORD_RESET_EMAIL_CONTEXT = {
    "domain": _canonical.netloc or "www.profeonline.cl",
    "site_name": "ProfeOnline",
    "protocol": _canonical.scheme or "https",
}

urlpatterns = [
    path("registro/", register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=StyledAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="core:home"), name="logout"),
    path("perfil/", profile_view, name="profile"),
    path("perfil/editar/", profile_update_view, name="profile_update"),

    # Recuperación de contraseña (vistas de Django con plantillas propias)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            form_class=StyledPasswordResetForm,
            success_url=reverse_lazy("password_reset_done"),
            extra_email_context=PASSWORD_RESET_EMAIL_CONTEXT,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirmar/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=StyledSetPasswordForm,
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/completado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
