# Generated by Django 3.2 on 2021-07-05 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userinfo_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='手机号'),
        ),
    ]
