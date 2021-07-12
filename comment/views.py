from django.http import JsonResponse

from .models import Comment
from .commentform import CommentForm


# Create your views here.

def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    back_dic = {'code': 1000, 'msg': ''}
    if comment_form.is_valid():
        comment_obj = Comment()

        comment_obj.user = comment_form.cleaned_data['user']
        comment_obj.content = comment_form.cleaned_data['content']
        comment_obj.content_object = comment_form.cleaned_data['model_obj']
        parent = comment_form.cleaned_data['parent']

        if parent:
            comment_obj.root = parent.root if parent.root else parent
            comment_obj.parent = parent
            comment_obj.reply_to = parent.user
        comment_obj.save()

        # ajax提交返回数据
        back_dic['username'] = comment_obj.user.get_name()
        back_dic['comment_time'] = comment_obj.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        back_dic['content'] = comment_obj.content
        back_dic['pk'] = comment_obj.pk

    else:
        back_dic['status'] = 'ERROR'
        back_dic['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(back_dic)