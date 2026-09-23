from django.db import models


class Source(models.Model):
    SOURCE_TYPES = [
        ("MEDIA", "Media"),
        ("JOURNALIST", "Journalist"),
        ("OFFICIAL", "Official"),
    ]

    name = models.CharField(max_length=200)
    url = models.URLField()

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default="MEDIA",
    )

    initial_reliability = models.FloatField(default=50.0)

    total_rumours = models.IntegerField(default=0)
    confirmed_rumours = models.IntegerField(default=0)
    failed_rumours = models.IntegerField(default=0)

    reliability_score = models.FloatField(default=50.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name