from django.test import TestCase

from ..templatetags.markdown_extras import markdown_to_text_filter


class MarkdownExtrasTests(TestCase):

    def test_markdown_to_text_filter(self):
        """
        Test that the markdown_to_text_filter converts markdown to plain text
        """
        markdown_text = "# Heading This is a **bold** text."
        expected_text = "Heading This is a bold text."
        result = markdown_to_text_filter(markdown_text)
        self.assertEqual(result.strip(), expected_text.strip())
