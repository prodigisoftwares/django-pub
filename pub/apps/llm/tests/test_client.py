from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from ..client import generate_answer


class GenerateAnswerTest(TestCase):
    def test_generate_answer_returns_expected(self):
        prompt = "What is Django?"
        expected = "Django is a web framework."
        with patch(
            "apps.llm.client.post_prompt",
            return_value=expected,
        ) as mock_post:
            result = generate_answer(prompt)
            mock_post.assert_called_once()
            self.assertEqual(result, expected)


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
