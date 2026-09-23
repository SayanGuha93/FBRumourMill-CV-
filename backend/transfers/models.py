from django.db import models
from news.models import Source


class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50)
    current_club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TransferClaim(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    destination_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="transfer_claims"
    )

    reliability_score = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.name} → {self.destination_club.name}"


class TransferRumour(models.Model):
    claim = models.ForeignKey(
        TransferClaim,
        on_delete=models.CASCADE,
        related_name="rumours",
        null=True,
        blank=True,
    )

    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="rumours"
    )

    from_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="outgoing_rumours"
    )

    to_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="incoming_rumours"
    )

    transfer_stage = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    article_title = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )

    article_url = models.URLField(
    unique=True,
    )

    evidence = models.TextField(
        null=True,
        blank=True,
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True
    )

    probability = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claim} - {self.source.name}"