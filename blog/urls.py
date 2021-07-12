from django.urls import path, re_path

from . import views


urlpatterns = [
    path('addsite/', views.add_site, name='add_site'),
    path('typeandtag/', views.edit_type_and_tag, name='edit_type_and_tag'),
    path('type_or_tag/add', views.add_type_or_tag, name='add_type_or_tag'),
    path('type_or_tag/del', views.delete_type_or_tag, name='delete_type_or_tag'),
    path('article/delete/', views.delete_article, name='delete_article'),
    path('article/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('<str:username>/', views.site, name='site'),
    re_path(r'^(?P<username>\w+)/(?P<condition>type|tag|date)/(?P<param>.*)/', views.site, name='site_filter'),
    path('<str:username>/article/<int:article_id>/', views.article_detail, name='article_detail'),
]