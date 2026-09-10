from django.contrib import admin
from .models import Rumour


@admin.register(Rumour)
class RumourAdmin(admin.ModelAdmin):
    list_display = (
        "player_name",
        "current_club",
        "linked_club",
        "source",
        "reliability",
        "published_at",
    )
    list_filter = ("reliability", "source")
    search_fields = ("player_name", "current_club", "linked_club")