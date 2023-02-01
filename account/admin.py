from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdimni(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
