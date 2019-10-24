from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
from apps.operations.models import UserFavorite, Course, CourseComments
from apps.operations.forms import UserFavForm, CommentForm
from apps.organizations.models import CourseOrg, Teacher


class AddCommentView(View):
    """
    新增评论
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录',
            })
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误',
            })

class AddFavView(View):
    """
    用户收藏,取消收藏
    """
    def post(self, request, *args, **kwargs):
        #用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录',
            })
        user_fav_for = UserFavForm(request.POST)
        if user_fav_for.is_valid():
            fav_id = user_fav_for.cleaned_data['fav_id']
            fav_type = user_fav_for.cleaned_data['fav_type']

            #是否已收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    courseorg = CourseOrg.objects.get(id=fav_id)
                    courseorg.fav_nums -= 1
                    courseorg.save()
                elif fav_type == 3:
                    teacher  = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏',
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏',
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误',
            })

