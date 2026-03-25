from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import Profile


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            login(request, user)
            return redirect("core:home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})