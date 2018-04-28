from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'', include('planner.urls')),
    path('django_admin/', admin.site.urls),
]
