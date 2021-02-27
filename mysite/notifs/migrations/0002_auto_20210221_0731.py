# Generated by Django 3.1.4 on 2021-02-21 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0030_auto_20210214_1131'),
        ('notifs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notif',
            name='emailed',
        ),
        migrations.RemoveField(
            model_name='notif',
            name='target_model_type',
        ),
        migrations.RemoveField(
            model_name='notif',
            name='target_object_id',
        ),
        migrations.RemoveField(
            model_name='notif',
            name='title',
        ),
        migrations.AddField(
            model_name='notif',
            name='challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.challenge'),
        ),
        migrations.AddField(
            model_name='notif',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.comment'),
        ),
    ]