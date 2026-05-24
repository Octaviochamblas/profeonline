from django.test import TestCase
from django.urls import reverse


class SeoTechnicalViewTests(TestCase):
    def test_home_includes_canonical_og_url_and_structured_data(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/">')
        self.assertContains(response, '<meta property="og:url" content="http://testserver/">')
        self.assertContains(response, 'type="application/ld+json"')
        self.assertContains(response, '"@type": "WebSite"')

    def test_robots_txt_points_to_sitemap_and_blocks_private_paths(self):
        response = self.client.get(reverse("core:robots"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Disallow: /cuentas/")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")

    def test_sitemap_xml_lists_public_pages(self):
        response = self.client.get(reverse("core:sitemap"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<loc>http://testserver/</loc>")
        self.assertContains(response, "<loc>http://testserver/recursos/</loc>")
        self.assertContains(response, "<loc>http://testserver/temas/</loc>")
        self.assertNotContains(response, "/cuentas/")
        self.assertNotContains(response, "/admin/")
