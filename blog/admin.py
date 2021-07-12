from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_title')


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'article_type', 'create_time', 'last_edit_time')


@admin.register(models.ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'blog')


@admin.register(models.ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'blog')


@admin.register(models.Article2ArticleTag)
class Article2ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'article')
