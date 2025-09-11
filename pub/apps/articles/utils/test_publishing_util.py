from django.test import TestCase
from django.utils import timezone

from ..utils.publishing import set_published_at


class DummyModel:
    def __init__(self, is_published=False, published_at=None):
        self.is_published = is_published
        self.published_at = published_at


class SetPublishedAtTests(TestCase):
    def test_new_article_published_sets_published_at(self):
        model = DummyModel(is_published=True, published_at=None)
        set_published_at(model)
        self.assertIsNotNone(model.published_at)
        self.assertTrue(
            timezone.now() - model.published_at < timezone.timedelta(seconds=2)
        )

    def test_new_article_unpublished_sets_published_at_none(self):
        model = DummyModel(is_published=False, published_at=None)
        set_published_at(model)
        self.assertIsNone(model.published_at)

    def test_publish_existing_article_sets_published_at(self):
        prev = DummyModel(is_published=False, published_at=None)
        model = DummyModel(is_published=True, published_at=None)
        set_published_at(model, prev)
        self.assertIsNotNone(model.published_at)
        self.assertTrue(
            timezone.now() - model.published_at < timezone.timedelta(seconds=2)
        )

    def test_unpublish_existing_article_sets_published_at_none(self):
        prev = DummyModel(is_published=True, published_at=timezone.now())
        model = DummyModel(is_published=False, published_at=prev.published_at)
        set_published_at(model, prev)
        self.assertIsNone(model.published_at)

    def test_no_change_in_publish_status_leaves_published_at_unchanged(self):
        prev = DummyModel(is_published=True, published_at=timezone.now())
        model = DummyModel(is_published=True, published_at=prev.published_at)
        set_published_at(model, prev)
        self.assertEqual(model.published_at, prev.published_at)

        prev2 = DummyModel(is_published=False, published_at=None)
        model2 = DummyModel(is_published=False, published_at=None)
        set_published_at(model2, prev2)
        self.assertIsNone(model2.published_at)
