from django.conf.urls import patterns, url
from rango import views
from rango.views import ProfileView

urlpatterns = patterns('',

        url(r'^index/$', views.index, name='index'),
        url(r'^$', views.index, name='index'),
        url(r'^map/$', 'rango.views.ER_view'),
        
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^view/(?P<username>\w+)/$', ProfileView.as_view(), name="profile_view"),
        url(r'^edit/$', views.profile_edit, name="profile_edit"),
        url(r'^review/(\d+)/$', 'rango.views.review', name="review"),
        url(r'^post/(reply)/(\d+)/$', 'rango.views.post', name="post"),
        url(r'^reply/(\d+)/$', views.reply, name="reply"),
        url(r'^list/$', views.list, name="list"),

        )
