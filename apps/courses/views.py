from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from apps.courses.models import Course, CoursesTag, CourseResource, Video
# Create your views here.


class VideoView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        获取课程章节信息
        :param request:
        :param course_id:
        :param args:
        :param kwargs:
        :return:
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        #查询用户是否已关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程所有同学
        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        related_courses = []
        for item in all_courses:
            if item.course_id != course_id:
                related_courses.append(item.course)
        #课程资料下载
        course_resources = CourseResource.objects.filter(course=course)


        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'video': video,
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        :param request:
        :param course_id:
        :param args:
        :param kwargs:
        :return:
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)
        # 查询用户是否已关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程所有同学
        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        related_courses = []
        for item in all_courses:
            if item.course_id != int(course_id):
                related_courses.append(item.course)
        # 课程资料下载
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'comments' : comments
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        :param request:
        :param course_id:
        :param args:
        :param kwargs:
        :return:
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        #查询用户是否已关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程所有同学
        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')[:5]
        #related_courses = [user_course.course for user_course in all_courses if user_course.course_id != course_id]
        related_courses = []
        for item in all_courses:
            if item.course_id != course_id:
                related_courses.append(item.course)
        #课程资料下载
        course_resources = CourseResource.objects.filter(course=course)


        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        :param request:
        :param course_id:
        :param args:
        :param kwargs:
        :return:
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        #通过tag推荐相关课程
        tags = course.coursestag_set.all()
        tag_list = [tag.tag for tag in tags]
        course_tag = CoursesTag.objects.filter(tag__in=tag_list).exclude(course__id=course_id)
        related_courses = set()
        for i in course_tag:
            related_courses.add(i.course)
        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'related_courses': related_courses,
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取课程列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        all_course = Course.objects.order_by('-add_time')
        hot_orgs = all_course.order_by('-click_nums')[:3]
        # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_course = all_course.order_by('-students')
        elif sort == 'hot':
            all_course = all_course.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, per_page=2, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_course': courses,
            'sort': sort,
            'hot_orgs': hot_orgs
        })


