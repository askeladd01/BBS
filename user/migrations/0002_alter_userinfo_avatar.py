# Generated by Django 3.2 on 2021-07-04 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='user/avatar/default.png', upload_to='user/avatar', verbose_name='用户头像'),
        ),
    ]
