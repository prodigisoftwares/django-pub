from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Article


class ArticleAdmin(UnfoldModelAdmin, MarkdownxModelAdmin):
    readonly_fields = ("created_at", "updated_at", "published_at")
    fields = (
        "title",
        "content",
        "summary",
        "created_at",
        "updated_at",
        "is_published",
        "published_at",
    )

    class Media:
        css = {"all": ("css/markdownx_unfold.css",)}


admin.site.register(Article, ArticleAdmin)
