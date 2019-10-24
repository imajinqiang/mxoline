from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from apps.users.forms import (
    LoginForm,
    DynamicLoginForm,
    DynamicLoginPostForm,
    RegisterGetForm,
    RegisterPostForm,)
from extra_apps.utils.sms import send_sms_ali
from extra_apps.utils.random_str import generate_random
from mxonline.settings.base import (
    aliyunsms_accesskeyid,
    aliyunsms_accesskeysecret,
    aliyunsms_signature,
    aliyunsms_template_id,
    REDIS_HOST,
    REDIS_PORT,)
from apps.users.models import UserProfile
import redis
# Create your views here.


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form})

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']
            # 新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, 'register.html', {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form,
            })

class DynamicLoginView(View):
    """
    动态登录
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        next_url = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
            'next_url': next_url
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            mobile = login_form.cleaned_data['mobile']
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get('next', '')
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            verification = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form, 'dynamic_login': dynamic_login, 'verification': verification})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class SenSmsView(View):
    def post(self, request, *args, **kwargs):
        response_dict = {}
        send_sms_from = DynamicLoginForm(request.POST)
        if send_sms_from.is_valid():
            mobile = send_sms_from.cleaned_data['mobile']

            code = {'code': f'{generate_random(4, 0)}'}
            response_json = send_sms_ali(mobile, aliyunsms_accesskeyid, aliyunsms_accesskeysecret, aliyunsms_signature, aliyunsms_template_id, code)
            if response_json['Code'] == 'OK':
                response_dict['status'] = 'success'
                db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                db.set(str(mobile), code['code'])
                db.expire(str(mobile), 60*5)  #设置验证码5分钟过期
            else:
                response_dict['message'] = response_json['Message']
        else:
            for key, value in send_sms_from.errors.items():
                response_dict[key] = value[0]
        return JsonResponse(response_dict)

class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        next_url = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
            'next_url': next_url
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', '')
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {'message': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


