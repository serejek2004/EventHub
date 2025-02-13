from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age')
    search_fields = ('user__username', 'biography')
