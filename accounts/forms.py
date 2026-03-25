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

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label="Nombre")
    last_name = forms.CharField(max_length=150, required=False, label="Apellido")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "institution",
            "education_level",
        ]
        labels = {
            "phone": "Teléfono",
            "city": "Ciudad",
            "institution": "Institución",
            "education_level": "Nivel educativo",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email