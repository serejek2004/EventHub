# Generated by Django 5.1.6 on 2025-02-11 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_profile_slug_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile',
            new_name='user',
        ),
    ]
