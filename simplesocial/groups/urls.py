from django.urls import path
from django.conf.urls import url
from groups import views

app_name='groups'

urlpatterns=[
    path('',views.ListGroup.as_view(),name='all'),
    path('new/',views.CreateGroup.as_view(),name='create'),
    url(r'^update/group/(?P<slug>[-\w]+)/$',views.UpdateGroup.as_view(),name='update'),
    url(r'^posts/in/(?P<slug>[-\w]+)/$',views.SingleGroup.as_view(),name='single'),
    url(r'join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
    url(r'leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
    url(r'remove/(?P<slug>[-\w]+)/$',views.DeleteGroup.as_view(),name='remove'),
    url(r'kick/(?P<user>\d+)/(?P<group>\d+)/$',views.DeleteGroupMember.as_view(),name='kick'),

]