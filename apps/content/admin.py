from django.contrib import admin
from apps.content.models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    search_fields = ("title",)
    list_filter = ("is_published",)