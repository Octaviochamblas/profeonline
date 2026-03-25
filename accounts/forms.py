from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label="Tipo de usuario"
    )

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]