from django.contrib import admin
from .models import UserProfile, Image, UserItems


admin.site.register(UserProfile)
admin.site.register(UserItems)
admin.site.register(Image)
