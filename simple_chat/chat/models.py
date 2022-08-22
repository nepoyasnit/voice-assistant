from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Dialog(models.Model):
    user_id = models.IntegerField()


class Message(models.Model):
    text = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    is_mine = models.BooleanField(default=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)





