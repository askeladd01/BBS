# Generated by Django 3.2 on 2021-07-05 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210705_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article2articletag',
            options={'verbose_name_plural': '文章对应标签表'},
        ),
    ]
