# Generated by Django 5.1.6 on 2025-02-13 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_alter_userprofile_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(blank=True, default=18, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='biography',
            field=models.TextField(blank=True, default='Biography', max_length=2000, null=True),
        ),
    ]
