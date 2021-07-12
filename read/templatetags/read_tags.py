from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ReadNum

register = template.Library()


@register.simple_tag
def get_read_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    read_count, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return read_count.read_num
