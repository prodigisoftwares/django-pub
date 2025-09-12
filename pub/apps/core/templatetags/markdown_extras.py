import re

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter(name="markdownify")
def markdownify_filter(text):
    """
    Convert markdown text to HTML using django-markdownx's
    markdownify function. This preserves all the markdown formatting
    and converts it to proper HTML.
    """
    if not text:
        return ""

    html_content = markdownify(text)

    return mark_safe(html_content)


@register.filter(name="markdownify_summary")
def markdownify_summary_filter(text):
    """
    Convert markdown summary text to HTML, with special handling for summaries.
    """
    if not text:
        return ""

    html_content = markdownify(text)

    return mark_safe(html_content)


@register.filter(name="markdown_to_text")
def markdown_to_text_filter(text):
    """
    Convert markdown to plain text by first converting to HTML,
    then stripping tags. Useful for previews and excerpts.
    """
    if not text:
        return ""

    html_content = markdownify(text)
    plain_text = strip_tags(html_content)
    clean_text = re.sub(r"\s+", " ", plain_text).strip()

    return clean_text
