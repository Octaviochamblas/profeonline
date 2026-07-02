from io import StringIO
import json
import os
import tempfile
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from apps.content.models import Level, Resource, Subject


class SeoTechnicalViewTests(TestCase):
    def setUp(self):
        from django.contrib.sites.models import Site
        Site.objects.filter(pk=1).update(domain="testserver", name="testserver")
        self.subject = Subject.objects.create(name="Matematica", is_active=True)
        self.inactive_subject = Subject.objects.create(name="Historia", is_active=False)
        self.level = Level.objects.create(name="Primaria", is_active=True)
        self.inactive_level = Level.objects.create(name="Secundaria", is_active=False)
        self.resource = Resource.objects.create(
            title="Guia de funciones",
            subject=self.subject,
            is_published=True,
        )
        self.inactive_resource = Resource.objects.create(
            title="Guia de historia",
            subject=self.inactive_subject,
            is_published=False,
        )
        self.inactive_resource.levels.add(self.inactive_level)

    def test_home_includes_canonical_og_url_and_structured_data(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/">')
        self.assertContains(response, '<meta property="og:url" content="http://testserver/">')
        self.assertContains(response, 'type="application/ld+json"')
        self.assertContains(response, '"@type": "WebSite"')
        self.assertContains(response, '"@type": "LocalBusiness"')
        self.assertContains(response, '"@type": "Person"')
        self.assertContains(response, '"name": "Octavio Chamblas Navarrete"')
        self.assertContains(response, '"addressLocality": "Concepción"')

    def test_home_highlights_public_content(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.subject.name)
        self.assertContains(response, self.level.name)
        self.assertContains(response, self.resource.title)

        self.assertNotContains(response, self.inactive_subject.name)
        self.assertNotContains(response, self.inactive_resource.title)

    def test_robots_txt_points_to_sitemap_and_blocks_private_paths(self):
        response = self.client.get(reverse("core:robots"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Disallow: /cuentas/")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")

    def test_favicon_redirects_to_svg_asset(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/static/img/favicon.svg", response["Location"])

    def test_sitemap_xml_lists_public_pages(self):
        response = self.client.get(reverse("core:sitemap"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<loc>http://testserver/</loc>")
        self.assertContains(response, "<loc>http://testserver/recursos/</loc>")
        self.assertContains(response, "<loc>http://testserver/temas/</loc>")
        self.assertContains(
            response,
            f"<loc>http://testserver/asignaturas/{self.subject.slug}/</loc>",
        )
        self.assertContains(
            response,
            f"<loc>http://testserver/niveles/{self.level.slug}/</loc>",
        )
        self.assertContains(
            response,
            f"<loc>http://testserver/recursos/{self.resource.slug}/</loc>",
        )
        self.assertContains(response, "<loc>http://testserver/terminos/</loc>")
        self.assertContains(response, "<loc>http://testserver/privacidad/</loc>")
        self.assertContains(response, "<loc>http://testserver/contacto/</loc>")
        self.assertNotContains(response, "/cuentas/")
        self.assertNotContains(response, "/admin/")
        self.assertNotContains(response, self.inactive_subject.slug)
        self.assertNotContains(response, self.inactive_level.slug)
        self.assertNotContains(response, self.inactive_resource.slug)

    def test_static_pages_render_correctly(self):
        terminos_res = self.client.get(reverse("core:terminos"))
        privacidad_res = self.client.get(reverse("core:privacidad"))
        contacto_res = self.client.get(reverse("core:contacto"))

        self.assertEqual(terminos_res.status_code, 200)
        self.assertEqual(privacidad_res.status_code, 200)
        self.assertEqual(contacto_res.status_code, 200)
        self.assertContains(terminos_res, "Términos de Uso")
        self.assertContains(privacidad_res, "Política de Privacidad")
        self.assertContains(contacto_res, "Contacto")


class KatexWiringTests(TestCase):
    """KaTeX se carga self-host en todo el sitio para renderizar fórmulas."""

    def test_base_template_loads_katex_assets(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        # CSS y JS servidos desde el propio dominio (self-host, no CDN).
        self.assertContains(response, "vendor/katex/katex.min.css")
        self.assertContains(response, "vendor/katex/katex.min.js")
        self.assertContains(response, "vendor/katex/contrib/auto-render.min.js")
        self.assertContains(response, "js/katex-init.js")
        self.assertNotContains(response, "cdn.jsdelivr.net")


class AdminNavigationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username="nav-admin",
            email="nav-admin@example.com",
            password="testpass123",
        )
        self.student = User.objects.create_user(
            username="nav-student",
            password="testpass123",
        )

    def test_admin_tools_are_grouped_in_one_disclosure(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, 'class="admin-nav"', count=1)
        self.assertContains(response, "Opciones de Administrador", count=1)
        for url_name in (
            "content:publish_studio",
            "content:question_studio",
            "content:bank_coverage",
            "content:bank_results",
            "content:bank_effectiveness",
            "content:quiz_guides",
            "core:analytics_dashboard",
        ):
            self.assertContains(response, f'href="{reverse(url_name)}"', count=1)

    def test_admin_disclosure_is_hidden_from_regular_users(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("core:home"))

        self.assertNotContains(response, "Opciones de Administrador")
        self.assertNotContains(response, 'class="admin-nav"')


class EnsureAdminCommandTests(TestCase):
    def test_creates_superuser_from_env(self):
        User = get_user_model()
        env = {
            "DJANGO_ADMIN_USERNAME": "root",
            "DJANGO_ADMIN_EMAIL": "root@example.com",
            "DJANGO_ADMIN_PASSWORD": "Sup3rS3cret!",
        }
        with mock.patch.dict("os.environ", env, clear=False):
            call_command("ensure_admin")

        user = User.objects.get(username="root")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password("Sup3rS3cret!"))

    def test_does_not_reset_existing_password(self):
        User = get_user_model()
        user = User.objects.create_superuser("admin", "admin@example.com", "OriginalPass1!")

        env = {"DJANGO_ADMIN_USERNAME": "admin", "DJANGO_ADMIN_PASSWORD": "AttemptedReset1!"}
        with mock.patch.dict("os.environ", env, clear=False):
            call_command("ensure_admin")

        user.refresh_from_db()
        self.assertTrue(user.check_password("OriginalPass1!"))
        self.assertFalse(user.check_password("AttemptedReset1!"))

    def test_restores_privileges_for_existing_user(self):
        User = get_user_model()
        user = User.objects.create_user("admin", "admin@example.com", "OriginalPass1!")
        self.assertFalse(user.is_superuser)

        with mock.patch.dict("os.environ", {"DJANGO_ADMIN_USERNAME": "admin"}, clear=False):
            call_command("ensure_admin")

        user.refresh_from_db()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_does_not_create_user_without_password(self):
        User = get_user_model()
        # clear=True guarantees DJANGO_ADMIN_PASSWORD is absent for this block.
        with mock.patch.dict("os.environ", {"DJANGO_ADMIN_USERNAME": "ghost"}, clear=True):
            call_command("ensure_admin")

        self.assertFalse(User.objects.filter(username="ghost").exists())


class EnsureSiteCommandTests(TestCase):
    @override_settings(CANONICAL_BASE_URL="https://www.profeonline.cl")
    def test_sets_domain_from_canonical_base_url(self):
        from django.contrib.sites.models import Site

        call_command("ensure_site")

        site = Site.objects.get(pk=settings.SITE_ID)
        self.assertEqual(site.domain, "www.profeonline.cl")
        self.assertEqual(site.name, "ProfeOnline")


class BrevoApiEmailBackendTests(TestCase):
    def _backend(self, **kwargs):
        from apps.core.email_backends import BrevoApiEmailBackend

        return BrevoApiEmailBackend(**kwargs)

    @override_settings(
        BREVO_API_KEY="test-key",
        DEFAULT_FROM_EMAIL="no-reply@profeonline.cl",
    )
    def test_build_payload_maps_message_fields(self):
        from django.core.mail import EmailMultiAlternatives

        msg = EmailMultiAlternatives(
            subject="Hola",
            body="Texto plano",
            from_email="ProfeOnline <no-reply@profeonline.cl>",
            to=["dest@example.com"],
        )
        msg.attach_alternative("<p>HTML</p>", "text/html")

        payload = self._backend()._build_payload(msg)

        self.assertEqual(payload["sender"]["email"], "no-reply@profeonline.cl")
        self.assertEqual(payload["sender"]["name"], "ProfeOnline")
        self.assertEqual(payload["to"], [{"email": "dest@example.com"}])
        self.assertEqual(payload["subject"], "Hola")
        self.assertEqual(payload["textContent"], "Texto plano")
        self.assertEqual(payload["htmlContent"], "<p>HTML</p>")

    @override_settings(BREVO_API_KEY="")
    def test_send_without_api_key_raises(self):
        from django.core.mail import EmailMessage

        backend = self._backend(fail_silently=False)
        with self.assertRaises(ValueError):
            backend.send_messages(
                [EmailMessage(subject="x", body="y", to=["a@b.com"])]
            )

    @override_settings(BREVO_API_KEY=" test-key ")
    def test_send_messages_posts_to_brevo_api(self):
        from django.core.mail import EmailMessage

        backend = self._backend()
        captured = {}

        class FakeResponse:
            status_code = 201
            text = "{}"

        def fake_post(url, json=None, headers=None, timeout=None):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            return FakeResponse()

        with mock.patch("apps.core.email_backends.requests.post", fake_post):
            sent = backend.send_messages(
                [
                    EmailMessage(
                        subject="Asunto",
                        body="Cuerpo",
                        from_email="no-reply@profeonline.cl",
                        to=["dest@example.com"],
                    )
                ]
            )

        self.assertEqual(sent, 1)
        self.assertEqual(captured["url"], "https://api.brevo.com/v3/smtp/email")
        # El header debe ir en minúsculas y la clave recortada (sin espacios).
        self.assertEqual(captured["headers"]["api-key"], "test-key")
        self.assertEqual(captured["json"]["subject"], "Asunto")

    @override_settings(BREVO_API_KEY="bad-key")
    def test_send_raises_with_brevo_error_body(self):
        from django.core.mail import EmailMessage

        backend = self._backend(fail_silently=False)

        class FakeResponse:
            status_code = 401
            text = '{"code":"unauthorized","message":"Key not found"}'

        with mock.patch(
            "apps.core.email_backends.requests.post",
            lambda *a, **k: FakeResponse(),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                backend.send_messages(
                    [EmailMessage(subject="x", body="y", to=["a@b.com"])]
                )

        self.assertIn("401", str(ctx.exception))
        self.assertIn("Key not found", str(ctx.exception))


class ContentSecurityPolicyTests(TestCase):
    def test_script_src_uses_nonce_without_unsafe_directives(self):
        response = self.client.get(reverse("core:home"))
        csp = response.headers["Content-Security-Policy"]

        self.assertIn("script-src 'self' 'nonce-", csp)
        # The script portion must not rely on unsafe-inline / unsafe-eval.
        script_portion = csp.split("style-src")[0]
        self.assertNotIn("unsafe-inline", script_portion)
        self.assertNotIn("unsafe-eval", csp)

    def test_inline_scripts_carry_the_request_nonce(self):
        import re

        response = self.client.get(reverse("core:home"))
        csp = response.headers["Content-Security-Policy"]
        content = response.content.decode()

        match = re.search(r"'nonce-([^']+)'", csp)
        self.assertIsNotNone(match)
        nonce = match.group(1)
        # The inline JSON-LD block on the home page must carry the same nonce.
        self.assertIn(f'nonce="{nonce}"', content)


class MarkdownSecurityFilterTests(TestCase):
    def test_markdown_filter_escapes_dangerous_html(self):
        from django.template import Template, Context

        # Test case: normal markdown formatting works
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")
        rendered = template_to_test.render(Context({"content": "This is **bold** text."}))
        self.assertIn("<strong>bold</strong>", rendered)

        # Test case: raw <script> tag is escaped
        rendered = template_to_test.render(Context({"content": "Hello <script>alert(1)</script> World"}))
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered)

        # Test case: raw <iframe> is escaped
        rendered = template_to_test.render(Context({"content": '<iframe src="http://malicious.com"></iframe>'}))
        self.assertNotIn("<iframe", rendered)
        self.assertIn("&lt;iframe src=\"http://malicious.com\"&gt;&lt;/iframe&gt;", rendered)

    def test_markdown_filter_neutralizes_javascript_links(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        # Test case: markdown javascript link is neutralized
        rendered = template_to_test.render(Context({"content": "[XSS](javascript:alert(1))"}))
        self.assertNotIn("href=\"javascript:", rendered)
        self.assertIn("<a>XSS</a>", rendered)

    def test_markdown_filter_keeps_safe_links(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": "[Guia](https://example.com/guia)"})
        )

        self.assertIn('<a href="https://example.com/guia">Guia</a>', rendered)

    def test_markdown_filter_allows_static_images(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": "![Ángulo agudo](/static/img/geometria/angulos/agudo.svg)"})
        )

        self.assertIn('<img alt="Ángulo agudo" src="/static/img/geometria/angulos/agudo.svg">', rendered)

    def test_markdown_filter_strips_javascript_image_src(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": '<img src="javascript:alert(1)" onerror="alert(1)">'})
        )

        self.assertNotIn("javascript:", rendered)
        self.assertNotIn("onerror", rendered)

    def test_markdown_filter_preserves_latex_inline_delimiters(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": r"Simplificar \(\frac{a}{b}\) por \(k\)."})
        )

        self.assertIn(r"\(\frac{a}{b}\)", rendered)
        self.assertIn(r"\(k\)", rendered)

    def test_markdown_filter_preserves_latex_block_and_dollar_delimiters(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": r"$$x^2$$ y también $y^2$ y \[z^2\]."})
        )

        self.assertIn(r"$$x^2$$", rendered)
        self.assertIn(r"$y^2$", rendered)
        self.assertIn(r"\[z^2\]", rendered)

    def test_markdown_filter_keeps_headings_around_math(self):
        from django.template import Template, Context
        template_to_test = Template("{% load markdown_tags %}{{ content|markdown }}")

        rendered = template_to_test.render(
            Context({"content": "### Definición formal\n\nUsa \\(\\frac{a}{b}\\) aquí."})
        )

        self.assertIn("<h3>Definición formal</h3>", rendered)
        self.assertIn(r"\(\frac{a}{b}\)", rendered)


class CacheBackendCheckTests(TestCase):
    @override_settings(
        DEBUG=False,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    def test_warning_when_locmem_and_not_debug(self):
        from apps.core.checks import cache_backend_check
        warnings = cache_backend_check(None)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0].id, "core.W001")
        self.assertIn("Producción sin cache compartida", warnings[0].msg)

    @override_settings(
        DEBUG=False,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/1",
            }
        }
    )
    def test_no_warning_when_redis_and_not_debug(self):
        from apps.core.checks import cache_backend_check
        warnings = cache_backend_check(None)
        self.assertEqual(len(warnings), 0)

    @override_settings(
        DEBUG=True,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    def test_no_warning_when_locmem_and_debug_true(self):
        from apps.core.checks import cache_backend_check
        warnings = cache_backend_check(None)
        self.assertEqual(len(warnings), 0)


class BackupRestoreCommandTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.backup_file = os.path.join(self.temp_dir.name, "test_backup.sqlite3")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_backup_db_creates_file(self):
        stdout = StringIO()
        call_command("backup_db", "--file", self.backup_file, stdout=stdout)

        self.assertTrue(os.path.exists(self.backup_file))
        self.assertGreater(os.path.getsize(self.backup_file), 0)
        self.assertIn("Respaldo SQLite exitoso", stdout.getvalue())

    def test_restore_db_restores_data(self):
        stdout_backup = StringIO()
        call_command("backup_db", "--file", self.backup_file, stdout=stdout_backup)

        stdout_restore = StringIO()
        db_name = settings.DATABASES["default"]["NAME"]
        call_command(
            "restore_db",
            "--file", self.backup_file,
            "--confirmar",
            "--destino", db_name,
            stdout=stdout_restore
        )
        self.assertIn("Restauración SQLite exitosa", stdout_restore.getvalue())

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "prod_db",
                "HOST": "production-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    def test_restore_db_aborts_on_production_without_confirmation(self):
        dummy_file = os.path.join(self.temp_dir.name, "dummy.dump")
        with open(dummy_file, "w") as f:
            f.write("dummy")

        with self.assertRaises(CommandError) as ctx:
            call_command("restore_db", "--file", dummy_file)

        self.assertIn("Operación abortada por seguridad", str(ctx.exception))

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "prod_db",
                "HOST": "production-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    def test_restore_db_aborts_on_production_with_wrong_destination(self):
        dummy_file = os.path.join(self.temp_dir.name, "dummy.dump")
        with open(dummy_file, "w") as f:
            f.write("dummy")

        with self.assertRaises(CommandError) as ctx:
            call_command("restore_db", "--file", dummy_file, "--confirmar", "--destino", "wrong_db")

        self.assertIn("Operación abortada por seguridad", str(ctx.exception))

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "prod_db",
                "HOST": "production-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    def test_restore_db_aborts_on_production_without_explicit_remote_permission(self):
        dummy_file = os.path.join(self.temp_dir.name, "dummy.dump")
        with open(dummy_file, "w") as f:
            f.write("dummy")

        with self.assertRaises(CommandError) as ctx:
            call_command("restore_db", "--file", dummy_file, "--confirmar", "--destino", "prod_db")

        self.assertIn("Operación abortada por seguridad", str(ctx.exception))

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "prod_db",
                "HOST": "production-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    def test_restore_db_succeeds_mocked_on_production_with_all_safety_flags(self):
        dummy_file = os.path.join(self.temp_dir.name, "dummy.dump")
        with open(dummy_file, "w") as f:
            f.write("dummy")

        import subprocess
        from unittest.mock import patch

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
            stdout = StringIO()
            call_command(
                "restore_db",
                "--file", dummy_file,
                "--confirmar",
                "--destino", "prod_db",
                "--permitir-remoto",
                stdout=stdout
            )
            self.assertIn("Restauración PostgreSQL exitosa", stdout.getvalue())
            mock_run.assert_called_once()


class CheckEnvironmentCommandTests(TestCase):
    @override_settings(DEBUG=True)
    def test_check_environment_development(self):
        stdout = StringIO()
        call_command("check_environment", stdout=stdout)

        output = stdout.getvalue()
        self.assertIn("=== Diagnóstico del Entorno ===", output)
        self.assertIn("Entorno detectado: DESARROLLO (DEBUG=True)", output)
        self.assertIn("DEBUG: True", output)

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "staging_db",
                "HOST": "staging-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    @mock.patch.dict(os.environ, {"SENTRY_ENVIRONMENT": "staging"})
    def test_check_environment_staging(self):
        stdout = StringIO()
        call_command("check_environment", stdout=stdout)

        output = stdout.getvalue()
        self.assertIn("Entorno detectado: STAGING (DEBUG=False, indicios de staging)", output)
        self.assertIn("DEBUG: False", output)
        self.assertIn("SENTRY_ENVIRONMENT: staging", output)

    @override_settings(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "prod_db",
                "HOST": "production-db.railway.app",
                "USER": "postgres",
                "PASSWORD": "password",
            }
        }
    )
    @mock.patch.dict(os.environ, {"SENTRY_ENVIRONMENT": "production"})
    def test_check_environment_production(self):
        stdout = StringIO()
        call_command("check_environment", stdout=stdout)

        output = stdout.getvalue()
        self.assertIn("Entorno detectado: PRODUCCIÓN (DEBUG=False, DB remota)", output)


class AnalyticsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.staff_user = self.User.objects.create_user(
            username="staff_admin",
            email="staff@example.com",
            password="securepassword",
            is_staff=True
        )
        self.regular_user = self.User.objects.create_user(
            username="student_user",
            email="student@example.com",
            password="securepassword",
            is_staff=False
        )
        # Cliente que valida CSRF estrictamente
        self.csrf_client = Client(enforce_csrf_checks=True)

    def test_analytics_post_valid_event(self):
        # El endpoint requiere un token CSRF. En TestCase, el cliente de pruebas
        # tiene la opción de deshabilitar la verificación CSRF (por defecto para tests)
        # o podemos pasarla normalmente.
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click", "path": "/recursos/"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

        from apps.core.models import AnalyticsEvent
        self.assertEqual(AnalyticsEvent.objects.filter(name="whatsapp_click").count(), 1)

    def test_analytics_post_invalid_event(self):
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "invalid_event_not_in_allowlist", "path": "/"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_analytics_post_missing_path(self):
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_analytics_post_rejects_missing_csrf(self):
        # Al usar enforce_csrf_checks=True, la petición POST sin token CSRF debe retornar 403.
        response = self.csrf_client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click", "path": "/"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_analytics_post_accepts_valid_csrf(self):
        # 1. Hacemos GET para establecer la cookie CSRF
        self.csrf_client.get(reverse("core:home"))
        csrf_token = self.csrf_client.cookies.get("csrftoken")
        self.assertIsNotNone(csrf_token)

        # 2. Hacemos POST con el token en la cabecera HTTP_X_CSRFTOKEN
        response = self.csrf_client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click", "path": "/"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token.value
        )
        self.assertEqual(response.status_code, 204)

    def test_analytics_post_sanitizes_metadata_and_limits_keys(self):
        # Enviamos metadata con claves prohibidas (PII) y con más de 5 claves
        payload = {
            "name": "whatsapp_click",
            "path": "/",
            "metadata": {
                "safe_key_1": "value1",
                "safe_key_2": 123,
                "email": "pii@example.com",  # PII, se omitirá
                "user_username": "pii_user",  # PII, se omitirá
                "safe_key_3": True,
                "safe_key_4": "value4",
                "safe_key_5": "value5",
                "safe_key_6": "value6",       # Excede el límite de 5 claves
            }
        }
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

        from apps.core.models import AnalyticsEvent
        event = AnalyticsEvent.objects.filter(name="whatsapp_click").first()
        self.assertIsNotNone(event)

        # Comprobar que no hay PII
        self.assertEqual(event.metadata, {})

        # Eventos sin metadata permitida quedan sin payload persistido.
        self.assertEqual(len(event.metadata), 0)

    def test_analytics_post_drops_sensitive_client_metadata_and_querystrings(self):
        payload = {
            "name": "whatsapp_click",
            "path": "/?utm_source=ad&email=pii@example.com",
            "metadata": {
                "href": "https://wa.me/56911112222?text=hola",
                "file_url": "/media/private/guia.pdf",
                "text": "Escribenos a alumno@example.com",
                "email": "pii@example.com",
                "phone": "+56911112222",
            }
        }
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

        from apps.core.models import AnalyticsEvent
        event = AnalyticsEvent.objects.filter(name="whatsapp_click").first()
        self.assertIsNotNone(event)
        self.assertEqual(event.path, "/")
        self.assertEqual(event.metadata, {})

    def test_analytics_post_allows_only_valid_video_id_metadata(self):
        payload = {
            "name": "video_play",
            "path": "https://www.profeonline.cl/recursos/demo/?email=pii@example.com",
            "metadata": {
                "video_id": "abcDEF_123-",
                "title": "Titulo con posible PII",
                "href": "https://youtube-nocookie.com/embed/abcDEF_123-",
            }
        }
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

        from apps.core.models import AnalyticsEvent
        event = AnalyticsEvent.objects.filter(name="video_play").first()
        self.assertIsNotNone(event)
        self.assertEqual(event.path, "/recursos/demo/")
        self.assertEqual(event.metadata, {"video_id": "abcDEF_123-"})

    def test_analytics_post_rejects_non_local_path(self):
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click", "path": "not-a-path"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    @override_settings(ANALYTICS_RATE_LIMIT_ATTEMPTS=3, ANALYTICS_RATE_LIMIT_WINDOW=10)
    def test_analytics_post_rate_limiting(self):
        # Limpiar caché para evitar interferencia entre tests
        from django.core.cache import cache
        cache.clear()

        # Hacer 3 peticiones (límite configurado a 3)
        for _ in range(3):
            response = self.client.post(
                reverse("core:analytics_post"),
                data=json.dumps({"name": "whatsapp_click", "path": "/"}),
                content_type="application/json",
                HTTP_X_FORWARDED_FOR="192.168.1.100"
            )
            self.assertEqual(response.status_code, 204)

        # La 4ta petición de la misma IP debe ser rechazada con 429
        response = self.client.post(
            reverse("core:analytics_post"),
            data=json.dumps({"name": "whatsapp_click", "path": "/"}),
            content_type="application/json",
            HTTP_X_FORWARDED_FOR="192.168.1.100"
        )
        self.assertEqual(response.status_code, 429)

    def test_login_google_signal_logs_event_for_existing_user(self):
        from allauth.account.signals import user_logged_in
        from apps.core.models import AnalyticsEvent
        from django.test import RequestFactory

        # Simulamos un request de test con RequestFactory
        factory = RequestFactory()
        request = factory.get('/')

        class FakeSocialAccount:
            provider = "google"

        class FakeSocialLogin:
            account = FakeSocialAccount()

        # Emitimos la señal con un usuario existente y pasamos sociallogin en los kwargs
        user_logged_in.send(
            sender=self.User,
            request=request,
            user=self.regular_user,
            sociallogin=FakeSocialLogin()
        )

        # Comprobamos que el evento fue guardado
        event = AnalyticsEvent.objects.filter(name="login_google", user=self.regular_user).first()
        self.assertIsNotNone(event)
        self.assertEqual(event.metadata.get("provider"), "google")

    def test_dashboard_accessible_only_by_staff(self):
        # 1. Anónimos deben ser redirigidos (staff_member_required -> login)
        response = self.client.get(reverse("core:analytics_dashboard"))
        self.assertEqual(response.status_code, 302)

        # 2. Usuarios comunes (no-staff) deben ser redirigidos
        self.client.force_login(self.regular_user)
        response = self.client.get(reverse("core:analytics_dashboard"))
        self.assertEqual(response.status_code, 302)

        # 3. Usuarios staff acceden exitosamente (200)
        self.client.force_login(self.staff_user)

        # Crear un ResourceView para que el dashboard rinda sin lanzar errores de datos vacíos
        from apps.content.models.resource import Resource
        from apps.content.models.completion import ResourceView

        # Creamos un recurso ficticio para la prueba
        from apps.content.models import Subject
        subj = Subject.objects.create(name="Matemática", is_active=True)
        res = Resource.objects.create(title="Prueba", slug="prueba", subject=subj, is_published=True)
        ResourceView.objects.create(user=self.staff_user, resource=res)

        response = self.client.get(reverse("core:analytics_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/panel_analitica.html")
