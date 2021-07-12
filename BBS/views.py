from django.shortcuts import render
from django.core.cache import cache

from blog import models
from utils.utils import MyPaginator
from read import utils


def home(request):
    # 文章展示分页
    article_list = models.Article.objects.filter().all()
    content = MyPaginator(request, article_list, 10)
    # 热门文章展示, 利用cache缓存查询数据，减轻服务器压力
    week_hot_articles = cache.get('week_hot_article')
    if not week_hot_articles:
        week_hot_articles = utils.get_week_hot_article()
        cache.set('week_hot_article', week_hot_articles, 3600)

    content['today_hot_articles'] = utils.get_today_hot_article()
    content['yesterday_hot_articles'] = utils.get_yesterday_hot_article()
    content['week_hot_articles'] = week_hot_articles

    return render(request, 'home.html', content)
