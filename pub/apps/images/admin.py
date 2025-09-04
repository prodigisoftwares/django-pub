from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Image


@admin.register(Image)
class ImageAdmin(UnfoldModelAdmin):
    list_display = ("title", "uploaded_at", "get_actions_column")
    search_fields = ("title",)

    class Media:
        js = ("js/copy_image_url.js",)

    def get_actions_column(self, obj):  # pragma: no cover
        if obj.image:
            html = f"""
                <span
                  class="
                    cursor-pointer text-base-400 px-3
                    hover:text-base-700 dark:text-base-500
                    dark:hover:text-base-200 p-1
                    copy-url-btn
                  "
                  data-url="{obj.image.url}"
                  title="Copy image URL"
                >
                  <span class="block material-symbols-outlined">
                    content_copy
                  </span>
                </span>
            """
            return mark_safe(html)
        return ""

    get_actions_column.short_description = "Actions"

    def change_view(
        self, request, object_id, form_url="", extra_context=None
    ):  # pragma: no cover
        extra_context = extra_context or {}

        if object_id:
            obj = self.get_object(request, object_id)

            if obj and obj.image:
                extra_context["image_url"] = obj.image.url

        return super().change_view(request, object_id, form_url, extra_context)
