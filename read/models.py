from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class ReadNum(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    read_num = models.IntegerField(default=0, verbose_name='阅读量')

    class Meta:
        verbose_name_plural = '文章阅读量表'


class ReadDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    date = models.DateField(default=timezone.now, verbose_name='阅读日期')
    read_num = models.IntegerField(default=0, verbose_name='当日阅读量')
    user = models.CharField(max_length=15, verbose_name='作者')

    class Meta:
        verbose_name_plural = '每日阅读量表'
