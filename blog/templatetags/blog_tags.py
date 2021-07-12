from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth

from ..models import ArticleType, ArticleTag, Article
from user.models import UserInfo

register = template.Library()


@register.inclusion_tag('right_menu.html')
def right_menu(username):
    blog_obj = UserInfo.objects.get(username=username).blog
    # 个人站点下文章分类与量级
    article_types = ArticleType.objects.filter(blog=blog_obj).annotate(article_count=Count('article__pk')) \
        .values_list('pk', 'type_name', 'article_count')

    article_tags = ArticleTag.objects.filter(blog=blog_obj).annotate(article_count=Count('article__pk')) \
        .values_list('pk', 'tag_name', 'article_count')

    # 临时创建月份字段用于分组统计
    article_dates = Article.objects.filter(blog=blog_obj).annotate(month=TruncMonth('create_time')).values('month') \
        .annotate(article_count=Count('id')).values_list('month', 'article_count')

    content = {'article_types': article_types, 'article_tags': article_tags,
               'article_dates': article_dates, 'username': username}

    return content
