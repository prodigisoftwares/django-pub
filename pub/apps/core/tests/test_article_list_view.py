from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.articles.models import Article
from apps.core.views.article_list import ArticleListView


class ArticleListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create some published and unpublished articles
        self.published1 = Article.objects.create(title="A1", is_published=True)
        self.published2 = Article.objects.create(title="A2", is_published=True)
        self.unpublished = Article.objects.create(
            title="A3",
            is_published=False,
        )

    def test_get_returns_200(self):
        url = (
            reverse("core:articles")
            if hasattr(reverse, "__call__")
            else "/"  # noqa: E501
        )
        request = self.factory.get(url)
        response = ArticleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_htmx_response_returns_200(self):
        url = (
            reverse("core:articles")
            if hasattr(reverse, "__call__")
            else "/"  # noqa: E501
        )
        request = self.factory.get(url, HTTP_HX_REQUEST="true")
        response = ArticleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_context_data_with_articles(self):
        view = ArticleListView()
        view.request = self.factory.get("/")
        context = view.get_context_data()
        self.assertIn("articles", context)
        self.assertIn("has_next", context)
        self.assertIn("next_page_number", context)
        self.assertIn("featured_article", context)

    def test_get_context_data_no_articles(self):
        Article.objects.all().delete()
        view = ArticleListView()
        view.request = self.factory.get("/")
        context = view.get_context_data()
        self.assertIn("articles", context)
        self.assertIn("has_next", context)
        self.assertIn("next_page_number", context)
        # self.assertIn("featured_article", context)

    def test_paginate_articles_returns_page(self):
        view = ArticleListView()
        request = self.factory.get("/", {"page": 1})
        articles = Article.objects.filter(is_published=True)
        page_obj = view.paginate_articles(request, articles)
        self.assertTrue(hasattr(page_obj, "object_list"))

    def test_get_articles_context_keys(self):
        view = ArticleListView()
        request = self.factory.get("/")
        articles = Article.objects.filter(is_published=True)
        page_obj = view.paginate_articles(request, articles)
        context = view.get_articles_context(
            page_obj,
            featured_article=self.published1,
        )
        self.assertIn("articles", context)
        self.assertIn("has_next", context)
        self.assertIn("next_page_number", context)
        self.assertIn("featured_article", context)
