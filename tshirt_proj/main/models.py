from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20, default='')
    verified_account = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='user_profiles/', default='images/def_logo.jpg')
    about = models.TextField(default='')

    def __str__(self):
        return f"Пользователь: {self.user}"


class Image(models.Model):
    image_main = models.ImageField(upload_to='user_profiles/', default='images/def_logo.jpg')
    image_dop1 = models.ImageField(upload_to='user_profiles/', default='images/def_logo.jpg')
    image_dop2 = models.ImageField(upload_to='user_profiles/', default='images/def_logo.jpg')

    def __str__(self):
        return f"Фото товара: {self.image_main}-{self.image_dop1}-{self.image_dop2}"


class UserItems(models.Model):
    author = models.CharField(max_length=20, default='')
    item_name = models.CharField(max_length=40, default='')
    pictures = models.OneToOneField(Image, on_delete=models.CASCADE, default='', null=True)
    category = models.CharField(max_length=20, default='')
    description = models.TextField(default='')

    def __str__(self):
        return f"Товар пользователя: {self.author}"
