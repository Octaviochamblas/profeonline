from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required



def register_view(request):
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

            login(request, user)
            return redirect("core:home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "alumno"},
    )
    return render(request, "accounts/profile.html", {"profile": profile})

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
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, "accounts/profile_form.html", {"form": form})