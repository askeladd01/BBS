import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum

from .models import ReadNum, ReadDetail
from blog.models import Article


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    cookies_key = f'{ct.model}_{obj.pk}_read'
    if not request.COOKIES.get(cookies_key):
        read_obj, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        read_obj.read_num += 1
        read_obj.save()

        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date,
                                                                user=obj.blog.userinfo.username)
        read_detail.read_num += 1
        read_detail.save()
    return cookies_key


def get_week_read_data(content_type, user):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))

        read_data = ReadDetail.objects.filter(content_type=content_type, date=date, user=user)
        res = read_data.aggregate(read_date_sum=Sum('read_num'))
        read_nums.append(res['read_date_sum'] or 0)
    return dates, read_nums


def get_today_hot_article():
    today = timezone.now().date()
    hot_article = Article.objects.filter(read_detail__date=today).values('id', 'title', 'blog__userinfo__username') \
        .annotate(hot_article_num=Sum('read_detail__read_num')).order_by('-hot_article_num')
    return hot_article[:7]


def get_yesterday_hot_article():
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    hot_article = Article.objects.filter(read_detail__date=yesterday).values('id', 'title', 'blog__userinfo__username') \
        .annotate(hot_article_num=Sum('read_detail__read_num')).order_by('-hot_article_num')
    return hot_article[:7]


def get_week_hot_article():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    hot_article = Article.objects.filter(read_detail__date__lt=today, read_detail__date__gte=date) \
        .values('id', 'title', 'blog__userinfo__username') \
        .annotate(hot_article_num=Sum('read_detail__read_num')).order_by('-hot_article_num')
    return hot_article[:7]


def get_user_yesterday_hot_article(blog):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    hot_article = Article.objects.filter(read_detail__date=yesterday, blog=blog).values('id', 'title',
                                                                                        'blog__userinfo__username') \
        .annotate(hot_article_num=Sum('read_detail__read_num')).order_by('-hot_article_num')
    return hot_article[:7]


def get_user_week_hot_article(blog):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    hot_article = Article.objects.filter(read_detail__date__lt=today, read_detail__date__gte=date, blog=blog) \
        .values('id', 'title', 'blog__userinfo__username') \
        .annotate(hot_article_num=Sum('read_detail__read_num')).order_by('-hot_article_num')
    return hot_article[:7]
