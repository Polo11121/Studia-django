from django.conf import settings
from django.db import models
from django.db.models import Avg


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='game_images/', null=True, blank=True)
    players = models.ManyToManyField(Player, through='PlayerGameLink')

    def average_score(self):
        average = self.playergamelink_set.aggregate(Avg('score'))['score__avg']
        return round(average, 2) if average else "No ratings"


class PlayerProfile(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    bio = models.TextField()


class PlayerGameLink(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
