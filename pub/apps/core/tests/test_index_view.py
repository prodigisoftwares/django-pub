from django.test import Client, TestCase
from django.urls import reverse

from apps.catalog.models import Offering


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("core:index")

        # Create some test offerings
        Offering.objects.create(
            name="Service 1",
            description="Description 1",
            price=100,
            is_active=True,
        )
        Offering.objects.create(
            name="Service 2",
            description="Description 2",
            price=200,
            is_active=True,
        )

    def test_index_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("offerings", response.context)
        self.assertEqual(len(response.context["offerings"]), 2)
