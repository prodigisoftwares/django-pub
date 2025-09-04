from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article


class ArticleAdmin(MarkdownxModelAdmin):
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


admin.site.register(Article, ArticleAdmin)
