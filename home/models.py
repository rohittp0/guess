import random

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    name = models.CharField(max_length=30, default="Player")
    value = models.IntegerField(default=random.randint(1, 100))
    guess = models.IntegerField(default=-1)

    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='payer_game')
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return "Winner" if self.is_winner else "Loser"


class Game(models.Model):
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

    total = models.IntegerField(default=0)
    players = models.IntegerField(default=0)


@receiver(post_save, sender=Player)
def on_player_save(sender, instance: Player, created: bool, **kwargs):
    if created:
        instance.game.players += 1
        instance.game.save()
