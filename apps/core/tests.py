from django.test import TestCase
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

