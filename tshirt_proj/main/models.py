from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified_account = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='static/user_profiles/', default='path/to/my/default/image.jpg')
    about = models.TextField(default='')

    def __str__(self):
        return f"Пользователь: {self.user}"
