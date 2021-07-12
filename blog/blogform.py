from django.forms import ModelForm, widgets

from .models import Blog, Article


class SiteForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['site_name', 'site_title', 'site_theme']
        widgets = {
            'site_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'site_title': widgets.TextInput(attrs={'class': 'form-control'}),
            'site_theme': widgets.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_site_name(self):
        site_name = self.cleaned_data.get('site_name')
        if Blog.objects.filter(site_name=site_name).exists():
            self.add_error('site_name', '个人站点名称已存在')
        return site_name


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'content': widgets.Textarea(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {'required': '标题不能为空哦~~~'},
            'content': {'required': '内容不能为空哦~~~'},
        }