from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Image


@admin.register(Image)
class ImageAdmin(UnfoldModelAdmin):
    list_display = ("title", "uploaded_at")
    search_fields = ("title",)

    class Media:
        js = ("js/copy_image_url.js",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            if obj and obj.image:
                extra_context["image_url"] = obj.image.url
        return super().change_view(request, object_id, form_url, extra_context)
