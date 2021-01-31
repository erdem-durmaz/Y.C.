# Generated by Django 3.1.4 on 2021-01-30 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gamification', '0012_auto_20210126_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenominate',
            name='caption',
            field=models.CharField(blank=True, max_length=150, verbose_name='Fotoğrafınızın İsmi'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('bio', models.CharField(max_length=350)),
                ('profile_pic', models.ImageField(default='default_img.jpg', upload_to='ProfilePicture/')),
                ('profile_avatar', models.ImageField(blank=True, null=True, upload_to='AvatarPicture/')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]