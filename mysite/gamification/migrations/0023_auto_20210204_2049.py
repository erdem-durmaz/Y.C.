# Generated by Django 3.1.4 on 2021-02-04 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0022_auto_20210204_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoreboard',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gamification.comment'),
        ),
    ]
