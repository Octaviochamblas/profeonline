from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import Profile


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