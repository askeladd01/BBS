from django.db import models
from django.contrib.auth.models import AbstractUser

from blog.models import Blog


# Create your models here.
class UserInfo(AbstractUser):
    nickname = models.CharField(max_length=15, verbose_name='昵称', null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='手机号', null=True, blank=True)
    avatar = models.FileField(upload_to='user/avatar', default='user/avatar/default.png', verbose_name='用户头像')
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(Blog, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname if self.nickname else self.username


def get_name(self):
    if self.nickname:
        return self.nickname
    else:
        return self.username


UserInfo.get_name = get_name
