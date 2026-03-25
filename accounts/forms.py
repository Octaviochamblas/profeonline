from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False, label="Nombre")
    last_name = forms.CharField(max_length=150, required=False, label="Apellido")
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label="Tipo de usuario"
    )
    phone = forms.CharField(max_length=30, required=False, label="Teléfono")
    city = forms.CharField(max_length=100, required=False, label="Ciudad")
    institution = forms.CharField(max_length=150, required=False, label="Institución")
    education_level = forms.CharField(max_length=100, required=False, label="Nivel educativo")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "phone",
            "city",
            "institution",
            "education_level",
            "password1",
            "password2",
        ]