# Generated by Django 3.2 on 2021-07-05 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('user', '0002_alter_userinfo_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blog'),
        ),
    ]
