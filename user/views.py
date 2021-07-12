import os
import uuid
import string
import time

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from bs4 import BeautifulSoup

from . import models
from . import userforms
from blog.models import Article, ArticleType, Article2ArticleTag, ArticleTag
from utils.utils import MyPaginator
from BBS.settings.base import BASE_DIR
from read.utils import get_week_read_data, get_user_week_hot_article, get_user_yesterday_hot_article


# Create your views here.
def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    img_obj = Image.new('RGB', (344, 34), get_random())
    img_draw = ImageDraw.Draw(img_obj)
    img_font = ImageFont.truetype('static/font/Regular.ttf', 30)

    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_int = str(random.randint(0, 9))
        tmp = random.choice([random_int, random_upper])
        img_draw.text((i * 60 + 60, -2), tmp, get_random(), img_font)
        code += tmp
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def login(request):
    if request.method == 'POST':
        form_obj = userforms.LoginForm(request.POST)
        back_dic = {'code': 1000, 'msg': ''}
        code = request.POST.get('code')
        if request.session.get('code') == code.upper():
            if form_obj.is_valid():
                user = form_obj.cleaned_data['user']
                auth.login(request, user)

                back_dic['url'] = request.GET.get('next', reverse('home'))
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = form_obj.errors
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    else:
        form_obj = userforms.LoginForm()
    return render(request, 'user/login.html', {'form_obj': form_obj})


def login_for_modal(request):
    form_obj = userforms.LoginForm(request.POST)
    back_dic = {'code': 1000, 'msg': ''}
    if form_obj.is_valid():
        user = form_obj.cleaned_data['user']
        auth.login(request, user)
    else:
        back_dic['code'] = 2000
        back_dic['msg'] = form_obj.errors
    return JsonResponse(back_dic)


def send_verification_code(request):
    email = request.POST.get('email', '')
    send_for = request.POST.get('send_for')
    data = {}
    if email:
        code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        send_time = request.session.get('send_time', 0)
        if time.time() - send_time < 30:
            data['status'] = 'ERROR_time'
        else:
            request.session[send_for] = code
            request.session['send_time'] = time.time()
            send_mail(f'{send_for}', f'验证码:{code}', '1073418959@qq.com', [email], fail_silently=False, )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        form_obj = userforms.RegForm(request.POST, request=request)
        back_dic = {'code': 1000, 'msg': ''}
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data
            clean_data.pop('re_password')
            clean_data.pop('verification_code')
            user = models.UserInfo.objects.create_user(**clean_data)
            user.save()

            del request.session['注册账号']

            auth.login(request, user)
            back_dic['url'] = request.GET.get('next', reverse('home'))
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    else:
        RegForm_obj = userforms.RegForm()
    return render(request, 'user/register.html', {'RegForm_obj': RegForm_obj})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', reverse('home')))


@login_required
def userinfo(request):
    return render(request, 'user/userinfo.html')


@login_required
def set_password(request):
    if request.method == 'POST':
        form_obj = userforms.SetPasswordForm(request.POST, user=request.user)
        if form_obj.is_valid():
            user = request.user
            password = form_obj.cleaned_data.get('new_password')
            user.set_password(password)
            user.save()

            auth.logout(request)
            return redirect(reverse('home'))
    else:
        form_obj = userforms.SetPasswordForm()
    context = {'page_title': '修改密码',
               'form_title': '修改密码',
               'submit_text': '修改',
               'form_obj': form_obj,
               'redirect_url': reverse('userinfo')}

    return render(request, 'forms.html', context)


@login_required
def setting(request):
    return render(request, 'user/setting.html')


@login_required
def backend(request):
    article_list = Article.objects.filter(blog=request.user.blog).order_by('-create_time')
    content = MyPaginator(request, article_list, 20)
    content['username'] = request.user.username
    return render(request, 'user/backend.html', content)


@login_required
def add_article(request):
    content = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        context = request.POST.get('content')
        article_type = request.POST.get("article_type")
        tag_id_list = request.POST.getlist('tags')
        # 删除script标签
        soup = BeautifulSoup(context, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[1:150]

        article_obj = Article.objects.create(
            title=title,
            content=str(soup),
            desc=desc,
            article_type_id=article_type,
            blog=request.user.blog
        )
        article_obj_tags = []
        for i in tag_id_list:
            tag_obj = Article2ArticleTag(article=article_obj, tag_id=i)
            article_obj_tags.append(tag_obj)
        Article2ArticleTag.objects.bulk_create(article_obj_tags)
        return redirect('backend')

    article_types = ArticleType.objects.filter(blog=request.user.blog)
    tags = ArticleTag.objects.filter(blog=request.user.blog)
    content['article_types'] = article_types
    content['tags'] = tags
    return render(request, 'user/addarticle.html', content)


@xframe_options_sameorigin
def upload_img(request):
    back_dic = {'error': 0, }
    if request.method == 'POST':
        file_obj = request.FILES.get('imgFile')
        file_dir = os.path.join(BASE_DIR, 'media', 'article_img')
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        file_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_obj.name)) + file_obj.name
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, 'wb')as f:
            for line in file_obj:
                f.write(line)
        back_dic['url'] = f'/user/media/article_img/{file_name}'
    return JsonResponse(back_dic)


@login_required
def set_avatar(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar')
        request.user.avatar = file_obj
        request.user.save()
    return redirect('/user/userinfo/setting/')

@login_required
def data_center(request):
    blog = request.user.blog
    article_content_type = ContentType.objects.get_for_model(Article)
    dates, read_nums = get_week_read_data(article_content_type, request.user)
    yesterday_hot_articles = get_user_yesterday_hot_article(blog)
    week_hot_articles = get_user_week_hot_article(blog)
    return render(request, 'user/data_center.html', {'dates': dates, 'read_nums': read_nums,
                                                     'yesterday_hot_articles': yesterday_hot_articles,
                                                     'week_hot_articles': week_hot_articles})


@login_required
def change_nickname(request):
    redirect_url = '/user/userinfo/setting/'
    context = {}
    if request.method == 'POST':
        form_obj = userforms.ChangeNicknameForm(request.POST)
        if form_obj.is_valid():
            new_nickname = form_obj.cleaned_data['new_nickname']
            request.user.nickname = new_nickname
            request.user.save()
            return redirect(redirect_url)
    else:
        form_obj = userforms.ChangeNicknameForm()

    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form_obj'] = form_obj
    context['redirect_url'] = redirect_url

    return render(request, 'forms.html', context)


def bind_email(request):
    redirect_url = '/user/userinfo/setting/'
    context = {}
    if request.method == 'POST':
        form_info = userforms.BindEmailForm(request.POST, request=request)
        if form_info.is_valid():
            email = form_info.cleaned_data['email']
            request.user.email = email
            request.user.save()

            del request.session['绑定邮箱']
            return redirect(redirect_url)
    else:
        form_info = userforms.BindEmailForm()

    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form_obj'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'user/bind_email.html', context)


def forget_password(request):
    redirect_url = reverse('home')
    context = {}
    if request.method == 'POST':
        form_info = userforms.ForgetPasswordForm(request.POST, request=request)
        if form_info.is_valid():
            email = form_info.cleaned_data['email']
            password = form_info.cleaned_data['password']
            user = models.UserInfo.objects.get(email=email)
            user.set_password(password)
            user.save()

            del request.session['忘记密码']
            return redirect(redirect_url)
    else:
        form_info = userforms.ForgetPasswordForm()

    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form_obj'] = form_info
    context['redirect_url'] = redirect_url

    return render(request, 'user/forget_psd.html', context)
