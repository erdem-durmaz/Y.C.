# Generated by Django 3.1.4 on 2021-01-09 20:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaratici', '0007_auto_20210109_2251'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='message',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
