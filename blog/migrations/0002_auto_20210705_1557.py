# Generated by Django 3.2 on 2021-07-05 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': '文章表'},
        ),
        migrations.AlterModelOptions(
            name='articletag',
            options={'verbose_name_plural': '文章标签表'},
        ),
        migrations.AlterModelOptions(
            name='articletype',
            options={'verbose_name_plural': '文章分类表'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name_plural': '个人站点表'},
        ),
    ]
