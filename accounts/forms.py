from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from .models import Profile


from apps.content.models import Level
from apps.core.forms import apply_form_classes

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
    education_level = forms.ModelChoiceField(
        queryset=Level.objects.all(), required=False, label="Nivel educativo"
    )

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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower().strip()
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)

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
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email
        apply_form_classes(self)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower().strip()
            qs = User.objects.filter(email__iexact=email)
            if self.user:
                qs = qs.exclude(pk=self.user.pk)
            if qs.exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado por otro usuario.")
        return email



class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        apply_form_classes(self)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            from django.contrib.auth import authenticate
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                from django.contrib.auth import get_user_model
                from allauth.account.models import EmailAddress
                from django.db.models import Q

                User = get_user_model()
                # Buscamos al usuario por username o por email
                user = User.objects.filter(Q(username=username) | Q(email=username)).first()
                if user and user.check_password(password) and not user.is_superuser:
                    # El password es correcto, pero no autenticó. ¿Falta verificación?
                    has_verified_email = EmailAddress.objects.filter(user=user, verified=True).exists()
                    if not has_verified_email:
                        raise forms.ValidationError(
                            "Tu correo electrónico no ha sido verificado. Por favor, revisa tu bandeja de entrada o haz clic en el enlace de reenvío."
                        )

                raise self.get_invalid_login_error()
            else:
                if self.user_cache.email and not self.user_cache.is_superuser:
                    from allauth.account.models import EmailAddress
                    has_verified_email = EmailAddress.objects.filter(user=self.user_cache, verified=True).exists()
                    if not has_verified_email:
                        raise forms.ValidationError(
                            "Tu correo electrónico no ha sido verificado. Por favor, revisa tu bandeja de entrada o haz clic en el enlace de reenvío."
                        )
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)
