from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # override model for the user
    pass


class Dialog(models.Model):
    """
    Is same for different messages in the same dialog
    """
    user_id = models.IntegerField()


class Message(models.Model):
    """
    model for storing message in the database
    """
    text = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    is_mine = models.BooleanField(default=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
