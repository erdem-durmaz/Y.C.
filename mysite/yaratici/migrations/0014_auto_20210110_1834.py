# Generated by Django 3.1.4 on 2021-01-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yaratici', '0013_choices_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choices',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
