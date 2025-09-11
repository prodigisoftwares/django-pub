import unittest
from unittest.mock import Mock, patch

from django.test import Client, TestCase
from django.urls import reverse

from .client import generate_answer


class TestGenerateAnswer(unittest.TestCase):
    def test_empty_prompt(self):
        self.assertEqual(generate_answer(""), "")

    @patch("apps.llm.utils.request.requests.post")
    def test_successful_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test answer."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = generate_answer("What is AI?")
        self.assertEqual(result, "Test answer.")

    @patch(
        "apps.llm.utils.request.requests.post",
        side_effect=Exception("Something went wrong"),
    )
    def test_generic_exception(self, mock_post):
        result = generate_answer("Test")
        self.assertTrue(result.startswith("LLM error:"))

    @patch(
        "apps.llm.utils.request.requests.post",
        side_effect=Exception("Timeout"),
    )
    def test_timeout_exception(self, mock_post):
        # Simulate Timeout exception
        with patch(
            "apps.llm.utils.request.requests.post",
            side_effect=Exception("Timeout"),
        ):
            result = generate_answer("Test")
            self.assertTrue(result.startswith("LLM error:"))

    @patch(
        "apps.llm.utils.request.requests.post",
        side_effect=ConnectionError(),
    )
    def test_connection_error(self, mock_post):
        result = generate_answer("Test")
        self.assertIn("LLM error:", result)

    @patch("apps.llm.utils.request.requests.post")
    def test_with_conversation_context(self, mock_post):
        """
        Test that conversation context is properly formatted and included.
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Context-aware answer.",
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_conversation = Mock()
        mock_exchange1 = Mock()
        mock_exchange1.query = "What is Python?"
        mock_exchange1.raw_answer = "Python is a programming language."
        mock_exchange1.attachments.all.return_value = []  # No attachments

        mock_exchange2 = Mock()
        mock_exchange2.query = "How do I install it?"
        mock_exchange2.raw_answer = "You can download it from python.org."
        mock_exchange2.attachments.all.return_value = []  # No attachments

        mock_exchanges = Mock()
        mock_exchanges.exists.return_value = True
        mock_exchanges.__iter__ = Mock(
            return_value=iter([mock_exchange1, mock_exchange2])
        )

        mock_conversation.exchanges.select_related.return_value.prefetch_related.return_value.order_by.return_value.__getitem__ = Mock(  # noqa: E501
            return_value=mock_exchanges
        )

        result = generate_answer(
            "Tell me more about versions",
            conversation=mock_conversation,
        )

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        self.assertIn("Previous conversation:", payload["system"])
        self.assertIn("User: What is Python?", payload["system"])
        self.assertIn(
            "Assistant: Python is a programming language.",
            payload["system"],
        )
        self.assertEqual(result, "Context-aware answer.")

    @patch("apps.llm.utils.request.requests.post")
    def test_conversation_without_exchanges(self, mock_post):
        """Test that empty conversation doesn't add context."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "No context answer.",
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_conversation = Mock()
        mock_exchanges = Mock()
        mock_exchanges.exists.return_value = False

        mock_conversation.exchanges.select_related.return_value.prefetch_related.return_value.order_by.return_value.__getitem__ = Mock(  # noqa: E501
            return_value=mock_exchanges
        )

        result = generate_answer(
            "What is AI?",
            conversation=mock_conversation,
        )

        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        self.assertNotIn("Previous conversation:", payload["system"])
        self.assertEqual(result, "No context answer.")

    @patch("apps.llm.utils.request.requests.post")
    def test_no_conversation_parameter(self, mock_post):
        """Test that function works without conversation parameter."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Simple answer."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = generate_answer("What is AI?")

        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        from apps.llm.config import SYSTEM_PROMPT

        self.assertEqual(payload["system"], SYSTEM_PROMPT)
        self.assertNotIn(
            "Previous conversation:",
            payload["system"],
        )
        self.assertEqual(result, "Simple answer.")

    @patch("apps.llm.utils.request.requests.post")
    def test_context_formatting(self, mock_post):
        """Test that context is formatted correctly with proper spacing."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Formatted answer."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_conversation = Mock()
        mock_exchange = Mock()
        mock_exchange.query = "Hello"
        mock_exchange.raw_answer = "Hi there!"
        mock_exchange.attachments.all.return_value = []  # No attachments

        mock_exchanges = Mock()
        mock_exchanges.exists.return_value = True
        mock_exchanges.__iter__ = Mock(return_value=iter([mock_exchange]))

        mock_conversation.exchanges.select_related.return_value.prefetch_related.return_value.order_by.return_value.__getitem__ = Mock(  # noqa: E501
            return_value=mock_exchanges
        )

        generate_answer("How are you?", conversation=mock_conversation)

        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        expected_in_system = "\n\nPrevious conversation:\nUser: Hello\n\nAssistant: Hi there!\n\n"  # noqa: E501
        self.assertIn(expected_in_system, payload["system"])

    @patch("apps.llm.utils.request.requests.post")
    def test_with_file_content(self, mock_post):
        """Test that file content is properly included in prompt."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": "File-aware answer."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        file_content = "This is sample file content\nWith multiple lines"
        result = generate_answer(
            "What does this file contain?", file_content=file_content
        )

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        self.assertIn(
            "User query: What does this file contain?",
            payload["prompt"],
        )
        self.assertIn("[Attached file content]", payload["prompt"])
        self.assertIn(file_content, payload["prompt"])
        self.assertEqual(result, "File-aware answer.")

    @patch("apps.llm.utils.request.requests.post")
    def test_with_conversation_and_attachments(self, mock_post):
        """Test that conversation context includes attachment information."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Context with attachments.",
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_conversation = Mock()
        mock_exchange = Mock()
        mock_exchange.query = "Analyze this file"
        mock_exchange.raw_answer = "The file contains data."

        mock_attachment = Mock()
        mock_attachment.filename = "data.txt"
        mock_attachment.content = "Sample file content"
        mock_exchange.attachments.all.return_value = [mock_attachment]

        mock_exchanges = Mock()
        mock_exchanges.exists.return_value = True
        mock_exchanges.__iter__ = Mock(return_value=iter([mock_exchange]))

        mock_conversation.exchanges.select_related.return_value.prefetch_related.return_value.order_by.return_value.__getitem__ = Mock(  # noqa: E501
            return_value=mock_exchanges
        )

        result = generate_answer(
            "Tell me more",
            conversation=mock_conversation,
        )

        call_args = mock_post.call_args
        payload = call_args[1]["json"]

        self.assertIn("[Attached file: data.txt]", payload["system"])
        self.assertIn("File content:\nSample file content", payload["system"])
        self.assertEqual(result, "Context with attachments.")


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
