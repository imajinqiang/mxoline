from mxonline.settings.base import (
    aliyunsms_accesskeyid,
    aliyunsms_accesskeysecret,
    aliyunsms_template_id,
    aliyunsms_signature)
from extra_apps.utils.sms import send_sms_ali
from extra_apps.utils.new_random import codes

import json
response_dict = {}
code = {'code': f'{codes(4)}'}
response_json = send_sms_ali('17600122677', aliyunsms_accesskeyid, aliyunsms_accesskeysecret, aliyunsms_signature, aliyunsms_template_id, code)
print(response_json)
# response_json = response_data.text
# if response_json['Code'] == 'OK':
#     response_dict['status'] = 'success'
# print(response_json)
# print(response_dict)
