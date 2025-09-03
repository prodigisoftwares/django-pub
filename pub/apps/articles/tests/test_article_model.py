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
        self.unpublished_article.save()
        self.assertEqual(self.unpublished_article.slug, "test-title")

    def test_unpublished_article_fields(self):
        self.unpublished_article.save()
        self.assertFalse(self.unpublished_article.is_published)
        self.assertIsNone(self.unpublished_article.published_at)

    def test_published_article_fields(self):
        self.published_article.save()
        self.assertTrue(self.published_article.is_published)
        self.assertIsNotNone(self.published_article.published_at)
