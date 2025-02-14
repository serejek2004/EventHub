from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from profile.models import UserProfile


class Event(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField(null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(UserProfile, related_name='registered_events', blank=True)
    event_image = models.ImageField(upload_to='static/event_images', null=False)

    def __str__(self):
        return f"{self.title} ({self.date_time.strftime('%d-%m-%Y %H:%M')})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        self.save()
        return reverse('event_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.event} id {self.id}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class LikeDislikeComment(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES = (
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(EventComment, on_delete=models.CASCADE, related_name='likes_dislikes')
    value = models.SmallIntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('user', 'comment')
