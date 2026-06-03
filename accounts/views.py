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
