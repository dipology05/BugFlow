from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import BugReport


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "component_label",
        "severity_label",
        "status",
        "created_at",
    )

    list_filter = (
        "component_label",
        "severity_label",
        "created_at",
    )

    search_fields = ("title", "description")
    ordering = ("-created_at",)

