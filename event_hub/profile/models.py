from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True, default=18)
    biography = models.TextField(null=True, blank=True, max_length=2000, default='Biography')
    profile_picture = models.ImageField(upload_to='static/profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
