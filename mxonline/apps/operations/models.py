from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import BaeModel
from apps.courses.models import Course
UserProfile = get_user_model()


class UserAsk(BaeModel):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名称')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(BaeModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name='课程')
    comments = models.CharField(max_length=200, verbose_name='评论内容')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(BaeModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    fav_id = models.IntegerField(verbose_name='数据ID')
    fav_type = models.IntegerField(choices=((1, '课程'),
                                            (2, '机构'),
                                            (3, '讲师'),), default=1, verbose_name='收藏类型')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(BaeModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    message = models.CharField(max_length=200, verbose_name='消息内容')
    has_red = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(BaeModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name