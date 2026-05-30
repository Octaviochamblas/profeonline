import json
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
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

    @override_settings(BREVO_API_KEY="test-key")
    def test_send_messages_posts_to_brevo_api(self):
        from django.core.mail import EmailMessage

        backend = self._backend()
        captured = {}

        class FakeResponse:
            status = 201

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(request, timeout=None):
            captured["url"] = request.full_url
            captured["api_key"] = request.headers.get("Api-key")
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse()

        with mock.patch("urllib.request.urlopen", fake_urlopen):
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
        self.assertEqual(captured["api_key"], "test-key")
        self.assertEqual(captured["body"]["subject"], "Asunto")


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
