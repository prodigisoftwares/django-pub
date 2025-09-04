from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from markdownx.models import MarkdownxField


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = MarkdownxField()
    summary = MarkdownxField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.pk:
            prev = Article.objects.get(pk=self.pk)
            if not prev.is_published and self.is_published:
                self.published_at = timezone.now()
            elif prev.is_published and not self.is_published:
                self.published_at = None
        else:
            if self.is_published and not self.published_at:
                self.published_at = timezone.now()
            elif not self.is_published:
                self.published_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
