from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # override model for the user
    pass


class Dialog(models.Model):
    """
    Is same for different messages in the same dialog
    """
    user_id = models.IntegerField(verbose_name='user identifier')

    class Meta:
        verbose_name = 'Dialog'
        verbose_name_plural = 'Dialogs'
        ordering = ['user_id']

    def __str__(self):
        name = User.objects.get(id=self.user_id).username
        return f"assistant - {name}"


class Message(models.Model):
    """
    model for storing message in the database
    """
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_mine = models.BooleanField(default=True, verbose_name='user\'s message')
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['date']
