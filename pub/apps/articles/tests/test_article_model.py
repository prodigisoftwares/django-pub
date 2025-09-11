from django.test import TestCase

from ..models import Article


class ArticleModelTest(TestCase):
    def setUp(self):
        self.unpublished_article = Article(
            title="Test Title",
            content="Test Content",
        )
        self.published_article = Article(
            title="Published Title",
            content="Published Content",
            is_published=True,
        )

    def test_slug_is_generated_on_save(self):
        """
        Test that the slug is generated from the title when saving an article.
        """
        self.unpublished_article.save()
        self.assertEqual(self.unpublished_article.slug, "test-title")

    def test_unpublished_article_fields(self):
        """
        Test that an unpublished article has is_published=False
        and published_at=None.
        """
        self.unpublished_article.save()
        self.assertFalse(self.unpublished_article.is_published)
        self.assertIsNone(self.unpublished_article.published_at)

    def test_published_article_fields(self):
        """
        Test that a published article has is_published=True
        and published_at set.
        """
        self.published_article.save()
        self.assertTrue(self.published_article.is_published)
        self.assertIsNotNone(self.published_article.published_at)
