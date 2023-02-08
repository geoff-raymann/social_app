from django.db import models
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

# from django.contrib.auth.models import User

# def store_facebook_access_token(user, access_token):
#     user.facebook_access_token = access_token
#     user.save()

# def get_facebook_access_token(user):
#     return user.facebook_access_token

# class FacebookProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     facebook_access_token = models.TextField(blank=True, null=True)

# def get_or_create_facebook_profile(user):
#     try:
#         return FacebookProfile.objects.get(user=user)
#     except FacebookProfile.DoesNotExist:
#         return FacebookProfile.objects.create(user=user)
