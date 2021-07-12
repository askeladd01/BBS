from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from user.models import UserInfo
from . import models
from utils.utils import MyPaginator
from .blogform import SiteForm, ArticleForm
from read.utils import read_statistics_once_read


# Create your views here.


def site(request, username, **kwargs):
    user_obj = UserInfo.objects.filter(username=username).first()
    if user_obj:
        blog_obj = user_obj.blog
        if user_obj == request.user:
            if not blog_obj:
                return redirect('add_site')
        # 个人站点下所有的文章
        article_list = models.Article.objects.filter(blog=blog_obj).all().order_by('-create_time')
        # 侧边栏条件筛选
        if kwargs:
            condition = kwargs.get('condition')
            param = kwargs.get('param')
            if condition == 'type':
                article_list = article_list.filter(article_type_id=param)
            elif condition == 'tag':
                article_list = article_list.filter(tags__id=param)
            else:
                year, month = param.split('-')
                article_list = article_list.filter(create_time__year=year, create_time__month=month)
        # 分页器
        content = MyPaginator(request, article_list, 10)

        content['username'] = user_obj.get_name
        content['blog_obj'] = blog_obj
        return render(request, 'site.html', content)
    else:
        return render(request, '404.html')


def article_detail(request, username, article_id):
    article_obj = get_object_or_404(models.Article, pk=article_id, blog__userinfo__username=username)
    tag_obj = models.Article2ArticleTag.objects.filter(article_id=article_id)
    previous_article = models.Article.objects.filter(pk__lt=article_id).filter().last()
    next_article = models.Article.objects.filter(pk__gt=article_id).filter().first()

    # 设置cookie记录当前用户是否阅读此文章
    read_cookies_key = read_statistics_once_read(request, article_obj)
    response = render(request, 'article_detail.html',
                      {'article_obj': article_obj, 'username': username, 'previous_article': previous_article,
                       'next_article': next_article, 'tag_obj': tag_obj})
    response.set_cookie(read_cookies_key, 'True')
    return response


def add_site(request):
    if request.method == 'POST':
        form_obj = SiteForm(request.POST)
        back_dic = {'code': 1000, 'msg': ''}
        if form_obj.is_valid():
            cleaned_data = form_obj.cleaned_data
            site_obj = models.Blog.objects.create(**cleaned_data)
            site_obj.save()
            request.user.blog = site_obj
            request.user.save()
            back_dic['url'] = f'/blog/{request.user.username}'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    else:
        form_obj = SiteForm()
    return render(request, 'addsite.html', {'form_obj': form_obj})


def edit_type_and_tag(request):
    user_obj = request.user
    article_types = models.ArticleType.objects.filter(blog=user_obj.blog)
    article_tags = models.ArticleTag.objects.filter(blog=user_obj.blog)
    content = {'article_types': article_types, 'article_tags': article_tags}
    return render(request, 'types_tags.html', content)


def add_type_or_tag(request):
    if request.method == 'POST':
        blog_obj = request.user.blog
        article_type = request.POST.get('article_type')
        if article_type:
            models.ArticleType.objects.create(type_name=article_type, blog=blog_obj)
        article_tag = request.POST.get('article_tag')
        if article_tag:
            models.ArticleTag.objects.create(tag_name=article_tag, blog=blog_obj)
        return redirect('/blog/typeandtag/')


def delete_type_or_tag(request):
    if request.is_ajax():
        back_dic = {'code': 1000}
        del_obj = request.POST.get('delete_for')
        del_id = request.POST.get('delete_id')
        if del_obj == 'type':
            type_obj = models.ArticleType.objects.get(pk=del_id)
            if type_obj:
                type_obj.delete()
            else:
                back_dic['code'] = 2000
        elif del_obj == 'tag':
            tag_obj = models.ArticleTag.objects.get(pk=del_id)
            if tag_obj:
                tag_obj.delete()
            else:
                back_dic['code'] = 2000
        else:
            back_dic['code'] = 2001
        return JsonResponse(back_dic)


def delete_article(request):
    if request.is_ajax():
        back_dic = {'code': 1000}
        delete_id = request.POST.get('delete_id')
        article_obj = models.Article.objects.get(pk=delete_id)
        if article_obj:
            article_obj.delete()
        else:
            back_dic['code'] = 2000
        return JsonResponse(back_dic)


def edit_article(request, article_id):
    content = {}
    article_obj = models.Article.objects.get(id=article_id)
    blog_obj = request.user.blog

    content['user_types'] = models.ArticleType.objects.filter(blog=blog_obj)
    content['article_obj_type'] = article_obj.article_type
    content['user_tags'] = models.ArticleTag.objects.filter(blog=blog_obj)
    content['article_obj_tags'] = article_obj.tags.all()
    if request.method == 'POST':
        article_obj_form = ArticleForm(request.POST)
        if article_obj_form.is_valid():
            article_obj.title = article_obj_form.cleaned_data['title']
            article_obj.content = article_obj_form.cleaned_data['content']
            article_obj.article_type_id = request.POST.get('article_type')
            article_obj.tags.set(request.POST.getlist('tags'))
            article_obj.save()
            return redirect('backend')
    else:
        article_obj_form = ArticleForm(initial={'title': article_obj.title, 'content': article_obj.content})
    content['form_obj'] = article_obj_form
    return render(request, 'edit_article.html', content)
