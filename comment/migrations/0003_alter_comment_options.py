# Generated by Django 3.2 on 2021-07-05 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time'], 'verbose_name_plural': '评论表'},
        ),
    ]
