# -*- coding: utf-8 -*-
import requests
import urllib.request
import time
import uuid
import hmac
import base64
import datetime
import json
import hashlib


def params(accesskeyid, mobiles, tpl_code, tpl_params, sign_name):
    p = [
        ["SignatureMethod", "HMAC-SHA1"],
        ["SignatureNonce", uuid.uuid4().hex],
        ["AccessKeyId", accesskeyid],
        ["SignatureVersion", "1.0"],
        ["Timestamp", time_now_fmt()],
        ["Format", "JSON"],

        ["Action", "SendSms"],
        ["Version", "2017-05-25"],
        ["RegionId", "cn-hangzhou"],
        ["PhoneNumbers", "{0}".format(mobiles)],
        ["SignName", sign_name],
        ["TemplateParam", json.dumps(tpl_params, ensure_ascii=False)],
        ["TemplateCode", tpl_code],
        ["OutId", "123"],
    ]
    return p


def time_now_fmt():
    r = datetime.datetime.utcfromtimestamp(time.time())
    r = time.strftime("%Y-%m-%dT%H:%M:%SZ", r.timetuple())
    return r


def special_url_encode(s):
    r = urllib.parse.quote_plus(s).replace(
        "+", "%20").replace("*", "%2A").replace("%7E", "~")
    return r


def encode_params(lst):
    s = "&".join(list(map(
        lambda p: "=".join(
            [special_url_encode(p[0]), special_url_encode(p[1])]),
        sorted(lst, key=lambda p: p[0])
    )))
    return s


def prepare_sign(s):
    r = "&".join(["GET", special_url_encode("/"), special_url_encode(s)])
    return r


def sign(access_secret,  prepare_str):
    k = "{0}{1}".format(access_secret, "&")
    r = hmac.new(k.encode(), prepare_str.encode(), hashlib.sha1).digest()
    base_str = base64.b64encode(r).decode()
    return special_url_encode(base_str)


def send_sms_ali(mobiles, accesskeyid, accesskeysecret, signature, template_id, code):
    prefix_url = "https://dysmsapi.aliyuncs.com/?"
    params_lst = params(accesskeyid, mobiles, template_id, code, signature)
    eps = encode_params(params_lst)
    prepare_str = prepare_sign(eps)
    sign_str = sign(accesskeysecret, prepare_str)

    url = f"{prefix_url}Signature={sign_str}&{eps}"
    response_data = requests.get(url)
    return json.loads(response_data.text)


if __name__ == "__main__":
    # 签名校验测试，与测试样例一致，待拿到正式参数时再做测试修改
    _accesskeyid = "*"
    _accesskeysecret = "*"
    _signature = "雪山飞狐"
    _template_id = "SMS_172740103"
    _code = {"code": "0000"}

    response_json = send_sms_ali("手机号", _accesskeyid, _accesskeysecret, _signature, _template_id, _code)
    code = response_json['Code']
    message = response_json['Message']
    print(response_json)
