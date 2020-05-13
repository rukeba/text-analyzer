from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.staticfiles import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sentences.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]
