from django.test import TestCase

from ..utils import context


class AddFileContextTests(TestCase):
    def test_add_file_context_basic(self):
        prompt = "What is in the file?"
        file_content = "hello world"
        result = context.add_file_context(prompt, file_content)
        self.assertIn(prompt, result)
        self.assertIn(file_content, result)
        self.assertIn("[Attached file content]", result)

    def test_add_file_context_truncates_long_content(self):
        prompt = "Summarize"
        file_content = "a" * 30001
        result = context.add_file_context(prompt, file_content)
        self.assertIn("... [content truncated]", result)
        self.assertTrue(len(result) < 31000)


class AppendContextPartsTests(TestCase):
    class DummyAttachment:
        def __init__(self, filename, content):
            self.filename = filename
            self.content = content

    class DummyExchange:
        def __init__(self, query, raw_answer, attachments=None):
            self.query = query
            self.raw_answer = raw_answer
            self.attachments = attachments or []

    class DummyAttachmentsManager:
        def __init__(self, attachments):
            self._attachments = attachments

        def all(self):
            return self._attachments

    def test_append_context_parts_with_file_content(self):
        context_parts = []
        exchange = self.DummyExchange(
            "Q?",
            "A!",
            self.DummyAttachmentsManager([]),
        )
        result = context.append_context_parts(
            context_parts, exchange, file_content="abc"
        )
        self.assertIn("User: Q?", result)
        self.assertIn("Assistant: A!", result)
        self.assertEqual(len(result), 2)

    def test_append_context_parts_with_attachments(self):
        att = self.DummyAttachment("file.txt", "abc")
        attachments = self.DummyAttachmentsManager([att])
        exchange = self.DummyExchange("Q?", "A!", attachments)
        context_parts = []
        result = context.append_context_parts(
            context_parts, exchange, file_content=None
        )
        self.assertIn("[Attached file: file.txt]", result)
        self.assertIn("File content:\nabc", result)
        self.assertIn("Assistant: A!", result)

    def test_append_context_parts_truncates_attachment_content(self):
        long_content = "x" * 3001
        att = self.DummyAttachment("file.txt", long_content)
        attachments = self.DummyAttachmentsManager([att])
        exchange = self.DummyExchange("Q?", "A!", attachments)
        context_parts = []
        result = context.append_context_parts(
            context_parts, exchange, file_content=None
        )
        self.assertIn("... [content truncated]", "".join(result))
