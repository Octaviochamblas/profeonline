from django.contrib import admin
from apps.content.models import Level, Resource, Subject, Topic


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_active")
    search_fields = ("name", "description")
    list_filter = ("subject", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "topic", "resource_type", "is_published", "created_at")
    search_fields = ("title", "description", "content_body")
    list_filter = ("subject", "topic", "resource_type", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("levels",)