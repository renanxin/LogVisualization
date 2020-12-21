from django.urls import path
from . import views

urlpatterns = [
    path('getdata', views.paramParse, name='获取数据'),
]
