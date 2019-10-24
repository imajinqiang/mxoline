from django.conf.urls import url

from apps.organizations.views import (
    Org_View,
    AddAskView,
    OrgHomeView,
    OrgTeacherView,
    OrgCourseView,
    OrgDescView,
    TeacherView,
    TeacherDetailView,
)

urlpatterns = [
    url(r'^list/$', Org_View.as_view(), name='list'),
    url(r'^add_ask/$', AddAskView.as_view(), name='add_ask'),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name='teacher'),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name='course'),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name='desc'),
    url(r'^teacher/$', TeacherView.as_view(), name='teacher'),
    url(r'^(?P<teacher_id>\d+)/detail/$', TeacherDetailView.as_view(), name='detail'),
]
