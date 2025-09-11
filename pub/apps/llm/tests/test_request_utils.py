from unittest.mock import patch

import requests
from django.test import TestCase

from ..utils.request import post_prompt


class PostPromptTestCase(TestCase):

    @patch("apps.llm.utils.request.requests.post")
    def test_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "response": "test response"
        }  # noqa: E501
        result = post_prompt("prompt", "url", {})
        self.assertEqual(result, "test response")

    @patch("apps.llm.utils.request.requests.post")
    def test_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        result = post_prompt("prompt", "url", {})
        self.assertEqual(result, "LLM request timed out.")
