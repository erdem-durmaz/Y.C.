# Generated by Django 3.1.5 on 2021-02-07 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yaratici', '0024_imaginequestion'),
        ('gamification', '0026_comment_imaginequestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreboard',
            name='imaginequestion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yaratici.imaginequestion'),
        ),
    ]
