# Generated by Django 3.1.5 on 2021-02-07 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yaratici', '0024_imaginequestion'),
        ('gamification', '0025_scoreboard_totalscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='imaginequestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yaratici.imaginequestion'),
        ),
    ]
