from django.views.generic import TemplateView

from apps.articles.models import Article


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["published_articles"] = Article.objects.filter(
            is_published=True,
        ).order_by("-published_at")[:7]

        return context
