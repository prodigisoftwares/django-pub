from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Image


@admin.register(Image)
class ImageAdmin(UnfoldModelAdmin):
    list_display = ("title", "uploaded_at")
    search_fields = ("title",)
