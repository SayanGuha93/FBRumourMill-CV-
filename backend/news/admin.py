from django.contrib import admin
from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "source_type",
        "initial_reliability",
        "total_rumours",
        "confirmed_rumours",
        "failed_rumours",
        "reliability_score",
    )