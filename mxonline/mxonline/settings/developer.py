from .base import *
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxonline',
        'USER': 'root',
        'PASSWORD': 'duanduan90',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
