# Generated by Django 3.2 on 2021-07-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('like', '0003_rename_up_num_likecount_up_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likerecord',
            name='is_up',
            field=models.BooleanField(null=True),
        ),
    ]
