from django.db import models

from apps.users.models import BaeModel
from apps.organizations.models import Teacher


class Course(BaeModel):
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    learn_times = models.IntegerField(default=0, verbose_name='学习市场(分钟)')
    degree = models.CharField(max_length=20 , choices=(
                                             ('primary', '初级'),
                                             ('intermediate','中级'),
                                             ('advanced ', '高级'),),
                              verbose_name='难度')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(max_length=20, default=u'后端开发', verbose_name='课程类别')
    tag = models.CharField(max_length=20, default='', verbose_name='课程标签')
    youneed_know = models.CharField(max_length=300, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='', verbose_name='老师告诉你')
    detail = models.TextField(verbose_name='课程详情')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name='封面图')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='课程讲师')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(BaeModel):
    name = models.CharField(max_length=100, verbose_name='章节名称')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaeModel):
    name = models.CharField(max_length=50, verbose_name='视频名称')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    url = models.CharField(max_length=200, verbose_name='访问地址')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaeModel):
    name = models.CharField(max_length=100, verbose_name='资源名称')
    file = models.FileField(upload_to='course/resource/%Y/%m')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '资源名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name