from django.views.generic import DetailView

from apps.articles.models import Article


class ArticleView(DetailView):
    model = Article
    template_name = "core/article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        article.save()
        context["article"] = article
        return context
