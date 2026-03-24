from django.contrib import admin
from apps.content.models import Resource, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "resource_type", "is_published", "created_at")
    search_fields = ("title", "description", "content_body")
    list_filter = ("subject", "resource_type", "is_published")
    prepopulated_fields = {"slug": ("title",)}