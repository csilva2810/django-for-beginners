from django.test import SimpleTestCase
from django.urls import reverse


# Create your tests here.
class HomePageViewTest(SimpleTestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")
