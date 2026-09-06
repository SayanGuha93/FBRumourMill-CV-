from django.db import models


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

class TransferRumour(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    from_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='outgoing_rumours'
    )
    to_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='incoming_rumours'
    )
    source = models.CharField(max_length=200)
    probability = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} to {self.to_club.name}"