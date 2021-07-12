from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Comment
from ..commentform import CommentForm


register = template.Library()


@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form_obj = CommentForm(initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})
    return form_obj


@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    article_comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return article_comments