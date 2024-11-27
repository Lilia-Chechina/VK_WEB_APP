from django.db import models


class Profile(models.Model):
    # id создаётся автоматически
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    # будет сохраняться в папке avatar


def __str__(self):
    return self.nickname

