# Generated by Django 5.1.6 on 2025-02-11 22:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_rename_profile_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('biography', models.TextField(blank=True, max_length=500, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='static/profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
