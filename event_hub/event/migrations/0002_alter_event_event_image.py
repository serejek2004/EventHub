# Generated by Django 5.1.6 on 2025-02-10 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_image',
            field=models.ImageField(blank=True, upload_to='static/event_images'),
        ),
    ]
