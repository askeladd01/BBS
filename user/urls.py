from django.urls import path, re_path
from django.views.static import serve

from . import views
from BBS import settings

urlpatterns = [
    path('login/', views.login, name='login'),
    path('loginModal/', views.login_for_modal, name='login_for_modal'),
    path('getcode/', views.get_code, name='get_code'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('article/add/', views.add_article, name='add_article'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('userinfo/setting/', views.setting, name='setting'),
    path('userinfo/setting/change_nickname', views.change_nickname, name='change_nickname'),
    path('userinfo/setting/change_email', views.bind_email, name='change_email'),
    path('userinfo/setting/forget_psd/', views.forget_password, name='forget_password'),
    path('userinfo/backend/', views.backend, name='backend'),
    path('userinfo/data-center/', views.data_center, name='data-center'),
    path('setpassword/', views.set_password, name='set_password'),
    path('setavatar/', views.set_avatar, name='set_avatar'),
    path('sendcode/', views.send_verification_code, name='send_email_code'),
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.base.MEDIA_ROOT})
]
