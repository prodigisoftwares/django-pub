from django.contrib import admin
from unfold import admin as unfold_admin

from .models import Offering


@admin.register(Offering)
class OfferingAdmin(unfold_admin.ModelAdmin):
    list_display = ("name", "price", "per")
    search_fields = ("name", "description")
    list_filter = ("per",)
    ordering = ("name",)
