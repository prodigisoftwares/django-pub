from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Comment


class CommentAdmin(ModelAdmin):
    list_display = [
        'author',
        'created_at',
        'is_approved',
        'is_flagged',
        'parent'
    ]

    list_filter = ['is_approved', 'is_flagged', 'created_at',]
    search_fields = ['content', 'author__username', 'author__email',]
    list_editable = ['is_approved', 'is_flagged']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


admin.site.register(Comment, CommentAdmin)
