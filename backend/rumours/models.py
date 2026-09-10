from django.db import models


class Rumour(models.Model):
    player_name = models.CharField(max_length=100)
    current_club = models.CharField(max_length=100)
    linked_club = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    reliability = models.IntegerField(default=50)
    description = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} → {self.linked_club}"