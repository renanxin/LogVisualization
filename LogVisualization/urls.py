"""LogVisualization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from filemanager.views import index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles import views


urlpatterns = [
    path('polls/',include('polls.urls')),
    path('',index, name="home"),
    path('filemanager/',include("filemanager.urls")),
    path('admin/', admin.site.urls),
    re_path(r'static/(?P<path>.*)',views.serve)          #   配置静态资源访问
]
