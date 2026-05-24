from django.contrib.auth.models import User
from django.test import TestCase

from apps.content.models import Level

from .forms import CustomUserCreationForm, ProfileUpdateForm, StyledAuthenticationForm
from .models import Profile


class AccountFormTests(TestCase):
    def setUp(self):
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.user = User.objects.create_user(
            username="profesor",
            password="testpass123",
            first_name="Ana",
            last_name="Perez",
            email="ana@example.com",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            role="profesor",
            phone="+56 9 1111 2222",
            city="Santiago",
            institution="Colegio ProfeOnline",
            education_level=self.level,
        )

    def test_custom_user_creation_form_applies_shared_classes(self):
        form = CustomUserCreationForm()

        self.assertIn("form-control", form.fields["username"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["email"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["education_level"].widget.attrs["class"])

    def test_profile_update_form_prefills_user_data_and_styles_fields(self):
        form = ProfileUpdateForm(instance=self.profile, user=self.user)

        self.assertEqual(form.fields["first_name"].initial, "Ana")
        self.assertEqual(form.fields["email"].initial, "ana@example.com")
        self.assertIn("form-control", form.fields["city"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["education_level"].widget.attrs["class"])

    def test_authentication_form_applies_shared_classes(self):
        form = StyledAuthenticationForm()

        self.assertIn("form-control", form.fields["username"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["password"].widget.attrs["class"])

    def test_custom_user_creation_form_unique_email_case_insensitive(self):
        form = CustomUserCreationForm(data={
            "username": "new_user",
            "email": "ANA@example.com",
            "first_name": "New",
            "last_name": "User",
            "role": "alumno",
            "password1": "testpass12345",
            "password2": "testpass12345",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"][0], "Este correo electrónico ya está en uso.")

    def test_profile_update_form_unique_email_case_insensitive(self):
        other_user = User.objects.create_user(
            username="other_profesor",
            password="testpass123",
            email="other@example.com",
        )
        form = ProfileUpdateForm(
            data={
                "first_name": "Ana",
                "last_name": "Perez",
                "email": "OTHER@example.com",
                "phone": "+56 9 1111 2222",
                "city": "Santiago",
                "institution": "Colegio ProfeOnline",
                "education_level": self.level.pk,
            },
            instance=self.profile,
            user=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"][0], "Este correo electrónico ya está registrado por otro usuario.")

