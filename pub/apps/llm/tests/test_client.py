from django.test import Client, TestCase
from django.urls import reverse


class TestOllamaViewSimple(TestCase):
    def test_test_ollama(self):
        client = Client()
        response = client.get(reverse("llm:test_ollama"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("success", data)
        self.assertTrue(data["success"])
        self.assertIn("response", data)
        self.assertIsInstance(data["response"], str)
