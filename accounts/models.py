from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlayerRecord(models.Model):
    username = models.CharField(max_length=100)
    time_taken = models.FloatField()
    level_reached = models.IntegerField()
    input_used = models.CharField(max_length=20)
    date_played = models.DateTimeField(auto_now_add=True)

class GameSession(models.Model):
    username = models.CharField(max_length=150)
    time_taken = models.FloatField()
    level_reached = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username