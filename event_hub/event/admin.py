from django.contrib import admin
from .models import Event, EventComment, LikeDislikeComment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'max_participants', 'creator')
    list_filter = ('date_time', 'location')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('participants',)


@admin.register(EventComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'event', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'event__title', 'text')


@admin.register(LikeDislikeComment)
class LikeDislikeCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'value')
    list_filter = ('user',)
    search_fields = ('user__username', 'comment__event__title')