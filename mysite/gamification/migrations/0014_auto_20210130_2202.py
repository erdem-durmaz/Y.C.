# Generated by Django 3.1.4 on 2021-01-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0013_auto_20210130_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_avatar',
        ),
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]