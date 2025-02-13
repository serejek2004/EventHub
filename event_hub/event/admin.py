from django.contrib import admin
from .models import Event, Comment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'max_participants', 'creator')
    list_filter = ('date_time', 'location')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('participants',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'event', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'event__title', 'text')