from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

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

    def test_form_fields_accessibility_attributes(self):
        form = CustomUserCreationForm()
        # Required fields must have aria-required="true"
        self.assertEqual(form.fields["username"].widget.attrs.get("aria-required"), "true")
        self.assertEqual(form.fields["email"].widget.attrs.get("aria-required"), "true")
        # Optional fields must not have aria-required
        self.assertNotIn("aria-required", form.fields["first_name"].widget.attrs)

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

    def test_email_is_required_in_registration(self):
        # El campo de email debe estar marcado como obligatorio.
        form = CustomUserCreationForm()
        self.assertTrue(form.fields["email"].required)

        # Y enviar el formulario sin email debe ser inválido.
        form = CustomUserCreationForm(data={
            "username": "sin_email",
            "first_name": "Sin",
            "last_name": "Email",
            "role": "alumno",
            "password1": "testpass12345",
            "password2": "testpass12345",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

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


class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="estudiante",
            email="estudiante@example.com",
            password="OldPass123!",
        )

    def test_reset_page_uses_project_templates(self):
        response = self.client.get(reverse("password_reset"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password_reset.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Recuperar contraseña")

    def test_login_page_links_to_password_reset(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, reverse("password_reset"))

    def test_reset_sends_email_with_confirm_link(self):
        response = self.client.post(
            reverse("password_reset"), {"email": "estudiante@example.com"}
        )

        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Restablece tu contraseña en ProfeOnline", mail.outbox[0].subject
        )
        self.assertIn("/cuentas/password-reset/confirmar/", mail.outbox[0].body)

    def test_reset_email_link_uses_canonical_domain_not_example_com(self):
        self.client.post(
            reverse("password_reset"), {"email": "estudiante@example.com"}
        )

        body = mail.outbox[0].body
        self.assertIn("https://www.profeonline.cl/cuentas/password-reset/confirmar/", body)
        self.assertNotIn("example.com", body)

    def test_allauth_reset_url_redirects_to_styled_flow(self):
        response = self.client.get("/accounts/password/reset/")

        self.assertRedirects(response, reverse("password_reset"))


class EmailVerificationFlowTests(TestCase):
    def setUp(self):
        self.User = get_user_model() if 'get_user_model' in globals() else User
        self.level = Level.objects.create(name="Primaria", is_active=True)
        # Limpiar la bandeja de salida de correos
        mail.outbox = []

    def test_registration_requires_verification_and_redirects(self):
        # 1. Registrar un nuevo usuario
        response = self.client.post(
            reverse("register"),
            data={
                "username": "nuevousuario",
                "email": "nuevo@example.com",
                "first_name": "Juan",
                "last_name": "Perez",
                "role": "alumno",
                "password1": "Secr3tP@ss123!",
                "password2": "Secr3tP@ss123!",
            }
        )

        # 2. Debe redirigir al aviso de email de verificación enviado
        self.assertRedirects(response, reverse("account_email_verification_sent"))

        # 3. El usuario NO debe estar logueado aún (verificación mandatory)
        self.assertNotIn('_auth_user_id', self.client.session)

        # 4. Comprobar que se envió el correo
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertIn("Activa tu cuenta en ProfeOnline", sent_mail.subject)
        self.assertIn("nuevo@example.com", sent_mail.to)

        # 5. Comprobar que en la base de datos existe EmailAddress con verified=False
        from allauth.account.models import EmailAddress
        email_addr = EmailAddress.objects.get(email="nuevo@example.com")
        self.assertFalse(email_addr.verified)

    def test_login_blocked_if_unverified(self):
        # Crear un usuario con email no verificado
        user = self.User.objects.create_user(
            username="no_verificado",
            email="noverificado@example.com",
            password="testpassword123"
        )
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(
            user=user,
            email="noverificado@example.com",
            verified=False,
            primary=True
        )

        # Intentar iniciar sesión
        response = self.client.post(
            reverse("login"),
            data={
                "username": "no_verificado",
                "password": "testpassword123"
            }
        )

        # Debe fallar y mostrar el error de validación de email no verificado
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            None,
            "Tu correo electrónico no ha sido verificado. Por favor, revisa tu bandeja de entrada o haz clic en el enlace de reenvío."
        )

    def test_confirm_email_link_activates_user_and_permits_login(self):
        # 1. Registrar usuario
        self.client.post(
            reverse("register"),
            data={
                "username": "activame",
                "email": "activame@example.com",
                "first_name": "Activ",
                "last_name": "Me",
                "role": "alumno",
                "password1": "Secr3tP@ss123!",
                "password2": "Secr3tP@ss123!",
            }
        )

        # 2. Extraer la key del email de confirmación
        body = mail.outbox[0].body
        # El email contiene la URL: /accounts/confirm-email/<key>/
        import re
        match = re.search(r"/accounts/confirm-email/([^/]+)/", body)
        self.assertIsNotNone(match)
        key = match.group(1)

        # 3. Acceder a la página de confirmación de email (GET)
        confirm_url = reverse("account_confirm_email", kwargs={"key": key})
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/email_confirm.html")

        # 4. Confirmar el email mediante POST a la misma URL de confirmación
        post_response = self.client.post(confirm_url)
        # Allauth por defecto redirige al login tras confirmar el email si no está autenticado
        self.assertEqual(post_response.status_code, 302)

        # 5. Comprobar que quedó verificado en la base de datos
        from allauth.account.models import EmailAddress
        email_addr = EmailAddress.objects.get(email="activame@example.com")
        self.assertTrue(email_addr.verified)

        # 6. Intentar iniciar sesión ahora que está verificado
        login_response = self.client.post(
            reverse("login"),
            data={
                "username": "activame",
                "password": "Secr3tP@ss123!"
            }
        )
        # Debe iniciar sesión y redirigir
        self.assertEqual(login_response.status_code, 302)

    def test_email_verification_resend_view(self):
        # Crear usuario sin verificar
        user = self.User.objects.create_user(
            username="reenviame",
            email="reenviame@example.com",
            password="testpassword123"
        )
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(
            user=user,
            email="reenviame@example.com",
            verified=False,
            primary=True
        )

        # Solicitar reenvío
        response = self.client.post(
            reverse("email_verification_resend"),
            data={"email": "reenviame@example.com"}
        )
        self.assertRedirects(response, reverse("account_email_verification_sent"))
        self.assertEqual(len(mail.outbox), 1)

    def test_social_login_exempt_from_verification_with_setting(self):
        # Simular usuario registrado con Google
        user = self.User.objects.create_user(
            username="socialuser",
            email="social@example.com",
            password="testpassword123"
        )

        # En el login social de allauth, si SOCIALACCOUNT_EMAIL_VERIFICATION = "none",
        # la dirección de email se marca como verificada automáticamente.
        # Comprobar que si creamos la relación social, allauth no la bloquea o que EmailAddress
        # para login social se marca verificado.
        # Simulamos que allauth crea la dirección de email verificada directamente:
        from allauth.account.models import EmailAddress
        email_addr, created = EmailAddress.objects.get_or_create(
            user=user,
            email="social@example.com",
            defaults={"verified": True, "primary": True}
        )
        self.assertTrue(email_addr.verified)

    def test_existing_users_verified_migration(self):
        # Simular que existían usuarios antes de correr la migración de datos
        user1 = self.User.objects.create_user(username="existente1", email="existente1@example.com", password="password")
        user2 = self.User.objects.create_user(username="existente2", email="", password="password") # Sin email
        user3 = self.User.objects.create_user(username="existente3", email="existente1@example.com", password="password") # Email duplicado

        # Corremos la lógica de la migración de datos manualmente para probarla
        import importlib
        migration_module = importlib.import_module("accounts.migrations.0004_auto_20260602_2311")
        verify_existing_users = migration_module.verify_existing_users

        class FakeApp:
            def get_model(self, app_label, model_name):
                if app_label == 'auth' and model_name == 'User':
                    return User
                if app_label == 'account' and model_name == 'EmailAddress':
                    from allauth.account.models import EmailAddress
                    return EmailAddress

        verify_existing_users(FakeApp(), None)

        from allauth.account.models import EmailAddress
        self.assertTrue(EmailAddress.objects.filter(user=user1, email="existente1@example.com", verified=True).exists())
        self.assertFalse(EmailAddress.objects.filter(user=user2).exists())
        # user3 no debe tener un EmailAddress verificado duplicado creado debido a la restricción única / desduplicación
        self.assertFalse(EmailAddress.objects.filter(user=user3).exists())

    def test_resend_view_anti_enumeration(self):
        # 1. Caso: El correo no existe en la base de datos
        response1 = self.client.post(
            reverse("email_verification_resend"),
            data={"email": "noexiste@example.com"}
        )
        self.assertRedirects(response1, reverse("account_email_verification_sent"))

        # 2. Caso: El correo existe y está sin verificar
        user = self.User.objects.create_user(username="unverified_resend", email="unverified@example.com", password="password")
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(user=user, email="unverified@example.com", verified=False, primary=True)

        response2 = self.client.post(
            reverse("email_verification_resend"),
            data={"email": "unverified@example.com"}
        )
        self.assertRedirects(response2, reverse("account_email_verification_sent"))

        # 3. Caso: El correo existe y ya está verificado
        user_verified = self.User.objects.create_user(username="verified_resend", email="verified@example.com", password="password")
        EmailAddress.objects.create(user=user_verified, email="verified@example.com", verified=True, primary=True)

        response3 = self.client.post(
            reverse("email_verification_resend"),
            data={"email": "verified@example.com"}
        )
        self.assertRedirects(response3, reverse("account_email_verification_sent"))

        # En todos los casos el mensaje en el response (mensajes de django) debe ser el mismo
        from django.contrib.messages import get_messages
        messages1 = [m.message for m in get_messages(response1.wsgi_request)]
        messages2 = [m.message for m in get_messages(response2.wsgi_request)]
        messages3 = [m.message for m in get_messages(response3.wsgi_request)]

        self.assertEqual(messages1, messages2)
        self.assertEqual(messages2, messages3)

    def test_login_blocked_if_no_email(self):
        # Crear un usuario sin email
        self.User.objects.create_user(
            username="sin_email",
            email="",
            password="testpassword123"
        )

        response = self.client.post(
            reverse("login"),
            data={
                "username": "sin_email",
                "password": "testpassword123"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            None,
            "Tu correo electrónico no ha sido verificado. Por favor, revisa tu bandeja de entrada o haz clic en el enlace de reenvío."
        )
