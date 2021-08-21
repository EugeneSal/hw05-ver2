# Generated by Django 2.2.6 on 2021-07-14 11:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0015_auto_20210713_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
