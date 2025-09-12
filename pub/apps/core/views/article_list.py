from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from apps.articles.models import Article


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

        page_obj = self.paginate_articles(request, all_articles)
        context = self.get_articles_context(page_obj)

        html = render_to_string(
            "core/includes/_article_cards.html", context, request=request
        )

        return HttpResponse(html)

    def get_articles_context(self, page_obj, featured_article=None) -> dict:
        context = {
            "articles": page_obj.object_list,
            "has_next": page_obj.has_next(),
            "next_page_number": (
                page_obj.next_page_number() if page_obj.has_next() else None
            ),
        }

        if featured_article is not None:
            context["featured_article"] = featured_article

        return context

    def paginate_articles(
        self, request, articles_queryset, default_page=2
    ) -> Paginator.page:
        page_number = request.GET.get("page", default_page)
        # Ensure queryset is ordered to avoid UnorderedObjectListWarning
        if not getattr(articles_queryset, "ordered", False):
            articles_queryset = articles_queryset.order_by("pk")
        paginator = Paginator(articles_queryset, self.paginate_by)

        try:
            page_obj = paginator.get_page(page_number)
        except (EmptyPage, PageNotAnInteger):  # pragma: no cover
            page_obj = paginator.get_page(1)

        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_articles = Article.objects.filter(
            is_published=True,
        ).order_by("-published_at")

        if all_articles.exists():
            featured_article = all_articles.first()
            remaining_articles = all_articles[1:]

            page_obj = self.paginate_articles(
                self.request, remaining_articles, default_page=1
            )

            context.update(
                self.get_articles_context(
                    page_obj,
                    featured_article=featured_article,
                )
            )

        else:
            context.update(
                self.get_articles_context(
                    page_obj=type(
                        "EmptyPage",
                        (),
                        {
                            "object_list": [],
                            "has_next": lambda s: False,
                            "next_page_number": lambda s: None,
                        },
                    )(),
                    featured_article=None,
                )
            )
        return context
