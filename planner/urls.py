from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from planner.forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^(?P<first_day>([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])))/$',
        views.calendar, name='calendar'),

    url(r'^change_request/(?P<id>(\d+))/(?P<decision>(accept|decline))/$',
        views.change_request, name='change_request'),

    url(r'^admin/$', views.admin, name='admin'),

    url(r'^login/$', auth_views.login, name='login',
        kwargs={'authentication_form': CustomAuthenticationForm}),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset',
        kwargs={'password_reset_form': CustomPasswordResetForm}),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm',
        kwargs={"set_password_form":CustomSetPasswordForm}),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
]
