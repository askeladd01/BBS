from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from read.models import ReadDetail


# Create your models here.
class Blog(models.Model):
    site_name = models.CharField(max_length=32, verbose_name='站点名称')
    site_title = models.CharField(max_length=32, verbose_name='站点标题')
    site_theme = models.CharField(max_length=64, verbose_name='站点主题', null=True, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name_plural = '个人站点表'


class ArticleType(models.Model):
    type_name = models.CharField(max_length=32, verbose_name='文章分类')
    blog = models.ForeignKey(to=Blog, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章分类表'

    def __str__(self):
        return self.type_name


class ArticleTag(models.Model):
    tag_name = models.CharField(max_length=32, verbose_name='文章标签')
    blog = models.ForeignKey(to=Blog, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章标签表'

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章简介')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    read_detail = GenericRelation(ReadDetail)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE, null=True)
    article_type = models.ForeignKey(to=ArticleType, on_delete=models.CASCADE, verbose_name='文章分类', null=True)
    tags = models.ManyToManyField(to=ArticleTag, through='Article2ArticleTag', through_fields=('article', 'tag'), verbose_name='文章标签')

    class Meta:
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title


class Article2ArticleTag(models.Model):
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='ArticleTag', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章对应标签表'



