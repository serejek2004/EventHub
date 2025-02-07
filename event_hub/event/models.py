from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Event(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, related_name='registered_events', blank=True)
    event_image = models.ImageField(upload_to='event_images', blank=True)

    def __str__(self):
        return f"{self.title} ({self.date_time.strftime('%d-%m-%Y %H:%M')})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.event}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"