# Generated by Django 2.2.6 on 2021-08-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20210808_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_views', to='posts.Ip', verbose_name='просмотры'),
        ),
    ]
