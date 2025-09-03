from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
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
