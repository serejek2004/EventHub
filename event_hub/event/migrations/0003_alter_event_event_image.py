# Generated by Django 5.1.6 on 2025-02-12 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_event_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_image',
            field=models.ImageField(upload_to='static/event_images'),
        ),
    ]
