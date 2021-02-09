# Generated by Django 3.1.4 on 2021-02-03 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yaratici', '0019_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='blogpost',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='yaratici.category'),
        ),
    ]