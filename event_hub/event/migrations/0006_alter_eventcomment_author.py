# Generated by Django 5.1.6 on 2025-02-13 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_eventcomment_delete_comment'),
        ('profile', '0006_alter_userprofile_age_alter_userprofile_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.userprofile'),
        ),
    ]
