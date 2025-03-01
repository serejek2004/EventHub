# Generated by Django 5.1.6 on 2025-02-12 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_event_image'),
        ('profile', '0005_alter_userprofile_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='registered_events', to='profile.userprofile'),
        ),
    ]
