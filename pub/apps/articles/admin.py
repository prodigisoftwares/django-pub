from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Article


class ArticleAdmin(UnfoldModelAdmin, MarkdownxModelAdmin):
    fields = (
        "title",
        "content",
        "summary",
        "created_at",
        "updated_at",
        "is_published",
        "published_at",
    )

    list_display = (
        "title",
        "is_published",
        "published_at",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_published",)
    ordering = ("-published_at", "-created_at")
    readonly_fields = ("created_at", "updated_at", "published_at")
    search_fields = ("title", "content", "summary")

    class Media:
        css = {"all": ("css/markdownx_unfold.css",)}


admin.site.register(Article, ArticleAdmin)
