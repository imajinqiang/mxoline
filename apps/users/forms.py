from django import forms
from captcha.fields import CaptchaField
import redis
from mxonline.settings.base import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile

class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.data.get('mobile')
        # 验证手机号码是否已经注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("手机号已注册")
        return mobile
    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = db.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        return code


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = db.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data


    # def clean(self):
    #     mobile = self.cleaned_data['mobile']
    #     code = self.cleaned_data['code']
    #
    #     db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
    #     redis_code = db.get(str(mobile))
    #     if redis_code != code:
    #         raise forms.ValidationError("验证码不正确")
    #     return self.cleaned_data