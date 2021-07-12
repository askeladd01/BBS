import json

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from .models import LikeCount, LikeRecord


# Create your views here.
def up_down(request):
    user = request.user
    if user.is_authenticated:
        content_type = ContentType.objects.get(model=request.GET.get('content_type'))
        object_id = request.GET.get('object_id')
        is_up = json.loads(request.GET.get('is_up'))
        # 先判断用户是否有点赞记录
        like_record = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).first()
        if like_record:
            like_count, i = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if like_record.is_up:
                # 已经点赞过则取消点赞
                like_count.up_num -= 1
                if is_up:
                    like_record.delete()
                else:
                    like_count.down_num += 1
                    like_record.is_up = 0
                    like_record.save()
            else:
                # 已经点踩则取消点踩
                like_count.down_num -= 1
                if is_up:
                    like_count.up_num += 1
                    like_record.is_up = 1
                    like_record.save()
                else:
                    like_record.delete()
            like_count.save()
        else:
            # 判断用户点赞还是点踩
            like_count, i = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if is_up:
                like_count.up_num += 1
            else:
                like_count.down_num += 1
            like_count.save()
            LikeRecord.objects.create(content_type=content_type, object_id=object_id, user=user, is_up=is_up)
        back_dic = {'code': 1000, 'up_num': like_count.up_num, 'down_num': like_count.down_num}
    else:
        back_dic = {'code': 2000, 'msg': '请先登录'}

    return JsonResponse(back_dic)
