# Generated by Django 3.1.4 on 2021-02-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0017_scoreboard_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoringactivities',
            name='score',
            field=models.IntegerField(default=1),
        ),
    ]