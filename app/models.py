from django.db import models


class Profile(models.Model):
    # id создаётся автоматически
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    # будет сохраняться в папке avatar

    # Метаданные
    class Meta:
        pass

    def __str__(self):
        return f"{self.nickname}"
        # return self.nickname

