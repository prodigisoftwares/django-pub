from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
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


class ArticleListView(TemplateView):
    template_name = "core/article_list.html"
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        if request.headers.get("HX-Request"):
            return self.get_htmx_response(request)
        return super().get(request, *args, **kwargs)

    def get_htmx_response(self, request):
        all_articles = Article.objects.filter(
            is_published=True,
        ).order_by(
            "-published_at"
        )[1:]

        page_number = request.GET.get("page", 2)
        paginator = Paginator(all_articles, self.paginate_by)

        try:
            page_obj = paginator.get_page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.get_page(1)

        context = {
            "articles": page_obj.object_list,
            "has_next": page_obj.has_next(),
            "next_page_number": (
                page_obj.next_page_number() if page_obj.has_next() else None
            ),
        }

        html = render_to_string(
            "core/includes/_article_cards.html", context, request=request
        )
        return HttpResponse(html)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_articles = Article.objects.filter(
            is_published=True,
        ).order_by("-published_at")

        if all_articles.exists():
            featured_article = all_articles.first()
            remaining_articles = all_articles[1:]

            paginator = Paginator(remaining_articles, self.paginate_by)
            page_obj = paginator.get_page(1)

            context["featured_article"] = featured_article
            context["articles"] = page_obj.object_list
            context["has_next"] = page_obj.has_next()
            context["next_page_number"] = 2 if page_obj.has_next() else None
        else:
            context["featured_article"] = None
            context["articles"] = []
            context["has_next"] = False
            context["next_page_number"] = None

        return context
