from django.contrib import admin
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "cta",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "subtitle",
    )

    ordering = ("-created_at",)

    list_editable = ("is_active",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Banner Info", {
            "fields": ("title", "subtitle", "image")
        }),
        ("Button Settings", {
            "fields": ("cta", "href", "accent_color")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Meta", {
            "fields": ("created_at",)
        }),
    )