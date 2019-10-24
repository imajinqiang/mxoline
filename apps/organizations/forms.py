from django import forms
from apps.operations.models import UserAsk
import re

class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = '^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码格式错误', code='mobile_invalid')
