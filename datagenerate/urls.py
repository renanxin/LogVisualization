from django.urls import path
from . import views

urlpatterns = [
    path('frequencydata', views.frequencydata, name='获取频率数据'),
    path('intervaldata', views.intervaldata, name='获取时间间隔数据'),
]
