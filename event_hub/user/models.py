from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def profile_image_tag(self):
        if self.profile_picture:
            return mark_safe(f'<img src="{self.profile_picture.url}" width="50" style="border-radius: 5px;" />')
        return "(No Image)"

    profile_image_tag.short_description = "Profile Picture"

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"