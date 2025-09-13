from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField

from .utils.publishing import set_published_at


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = MarkdownxField()
    summary = MarkdownxField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    is_published = models.BooleanField(default=False)
    comments = models.ManyToManyField("comments.Comment", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Handle published_at logic
        if self.pk:
            prev = Article.objects.get(pk=self.pk)
            set_published_at(model=self, prev_instance=prev)
        else:
            set_published_at(model=self)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
