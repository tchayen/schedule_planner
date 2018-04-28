from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from planner.forms import CustomAuthForm

urlpatterns = [
  path('', views.index, name='index'),
  url(r'^login/$', auth_views.login, name='login', kwargs={"authentication_form":CustomAuthForm}),
  url(r'^logout/$', auth_views.logout, name='logout'),
]
