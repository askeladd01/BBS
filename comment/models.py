from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from user.models import UserInfo


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.CharField(max_length=255, verbose_name='文章评论')
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=UserInfo, related_name='comments', on_delete=models.CASCADE, verbose_name='评论用户')

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    reply_to = models.ForeignKey(to=UserInfo, related_name='replies', null=True, on_delete=models.CASCADE,
                                 verbose_name='回复用户')

    class Meta:
        verbose_name_plural = '评论表'
        ordering = ['-comment_time']
