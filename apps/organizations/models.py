from django.db import models

from apps.users.models import BaeModel

class City(BaeModel):
    name = models.CharField(max_length=10, verbose_name='城市名称')
    desc = models.CharField(max_length=50, verbose_name='描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaeModel):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    tag = models.CharField(max_length=10, default='全国知名', verbose_name='机构标签')
    category = models.CharField(max_length=20, choices=(
                                                ('institutions', '培训机构'),
                                                ('personal', '个人'),
                                                ('universities', '高校'),), verbose_name='类型')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=100, upload_to='org/%Y/%m', verbose_name='logo')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所在城市')
    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    def courses(self):
        courses = self.course_set.all()
        return courses

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaeModel):
    name = models.CharField(max_length=10, verbose_name='姓名')
    age = models.IntegerField(default=18, verbose_name='年龄')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=100, upload_to='teacher/%Y/%m', verbose_name='头像')
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    class Meta:
        verbose_name = '讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()
