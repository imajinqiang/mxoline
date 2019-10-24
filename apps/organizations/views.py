from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from pure_pagination import Paginator, PageNotAnInteger

from apps.organizations.models import CourseOrg, City
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite
from apps.courses.models import Teacher


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        all_teacher = Teacher.objects.all()
        teacher = Teacher.objects.get(id=int(teacher_id))
        hot_teacher = all_teacher.order_by('-click_nums')[:3]
        teacher_course = teacher.course_set.all()

        teacher.click_nums += 1
        teacher.save()
        has_fav_org = False
        teacher_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_fav_org = True
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
        return render(request, 'teacher-detail.html', {
            'all_teacher': all_teacher,
            'teacher': teacher,
            'teacher_course': teacher_course,
            'has_fav_org': has_fav_org,
            'hot_teacher': hot_teacher,
            'teacher_fav': teacher_fav,
        })


class TeacherView(View):
    def get(self, request, *args, **kwargs):
        all_teacher = Teacher.objects.all()
        hot_teacher = all_teacher.order_by('-click_nums')[:3]
        teacher_count = all_teacher.count()
        # 教师排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teacher = all_teacher.order_by('-click_nums')

        # 教师数据分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, per_page=1, request=request)
        teacher = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teacher': teacher,
            'sort' : sort,
            'hot_teacher': hot_teacher,
            'teacher_count': teacher_count,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 课程机构数据分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=1, request=request)
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'all_courses': courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'teacher'
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'home'
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddAskView(View):
    """
    处理用户咨询
    """
    def post(self, request, *args, **kwargs):
        user_ask_from = AddAskForm(request.POST)
        if user_ask_from.is_valid():
            user_ask_from.save(commit=True)
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '添加错误'
            })


class Org_View(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        #根据机构类型筛选机构
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category  )
        org_nums = all_orgs.count()

        #根据机构所在城市筛选机构
        city_id = request.GET.get('city', '')
        if city_id and city_id.isdigit():
                all_orgs = CourseOrg.objects.filter(city_id=int(city_id))

        #机构排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')


        # 课程机构数据分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=1, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html',{
                    'all_orgs': orgs,
                    'org_nums': org_nums,
                    'all_citys': all_citys,
                    'category': category,
                    'city_id': city_id,
                    'sort': sort,
                    'hot_orgs': hot_orgs
                    })


