from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required



def _safe_next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def register_view(request):
    next_url = _safe_next_url(request)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                phone=form.cleaned_data["phone"],
                city=form.cleaned_data["city"],
                institution=form.cleaned_data["institution"],
                education_level=form.cleaned_data["education_level"],
            )

            from apps.core.models import AnalyticsEvent
            AnalyticsEvent.objects.create(
                name="signup",
                path=request.path,
                user=user,
                metadata={"role": form.cleaned_data["role"]}
            )

            # Flujo de verificación de email: si es mandatory redirigimos a la página de verificación
            from allauth.account import app_settings
            from allauth.account.utils import setup_user_email
            email_address = setup_user_email(request, user, [])

            if app_settings.EMAIL_VERIFICATION == "mandatory":
                if email_address:
                    email_address.send_confirmation(request, signup=True)
                messages.success(request, "¡Registro inicial exitoso! Te hemos enviado un correo de verificación para activar tu cuenta.")
                return redirect("account_email_verification_sent")
            else:
                if app_settings.EMAIL_VERIFICATION == "optional" and email_address:
                    email_address.send_confirmation(request, signup=True)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "¡Registro completado con éxito! Bienvenido a ProfeOnline.")
                if next_url:
                    return redirect(next_url)
                return redirect("core:home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form, "next_url": next_url})


@login_required
def profile_view(request):
    from apps.content.selectors import get_resume_resource
    from apps.content.services.gamification_service import get_gamification_summary
    from apps.content.services.progress_service import get_profile_progress

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "alumno"},
    )

    last_resource, last_resource_completed = get_resume_resource(request.user)

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "last_resource": last_resource,
            "last_resource_completed": last_resource_completed,
            "gamification": get_gamification_summary(request.user),
            "progress_groups": get_profile_progress(request.user),
        },
    )

@login_required
def profile_update_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "alumno"},
    )

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()

            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, "accounts/profile_form.html", {"form": form})


# Vista y formulario de reenvío de correo de verificación
from django import forms
from django.contrib.auth import get_user_model
from apps.core.forms import apply_form_classes

class ResendEmailForm(forms.Form):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)

def email_verification_resend_view(request):
    if request.method == "POST":
        form = ResendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower().strip()
            User = get_user_model()
            user = User.objects.filter(email__iexact=email).first()

            if user:
                from allauth.account.models import EmailAddress
                email_address = EmailAddress.objects.filter(user=user, email__iexact=email).first()

                # Creamos el registro de EmailAddress de forma segura si no existe (evitamos setup_user_email)
                if not email_address:
                    if not EmailAddress.objects.filter(email__iexact=email).exists():
                        try:
                            has_primary = EmailAddress.objects.filter(user=user, primary=True).exists()
                            email_address = EmailAddress.objects.create(
                                user=user,
                                email=email,
                                verified=False,
                                primary=not has_primary
                            )
                        except Exception:
                            email_address = None

                if email_address and not email_address.verified:
                    email_address.send_confirmation(request, signup=False)

            # Respuesta uniforme anti-enumeración para todos los casos (existentes, no existentes, verificados y no verificados)
            messages.success(request, "Si el correo electrónico está registrado, hemos enviado el enlace de verificación. Por favor, revisa tu bandeja de entrada.")
            return redirect("account_email_verification_sent")
    else:
        form = ResendEmailForm()

    return render(request, "accounts/email_verification_resend.html", {"form": form})
