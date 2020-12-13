from django.urls import path
from . import views

urlpatterns = [
    path('frequencydata', views.paramParseByFre, name='获取频率特征数据'),
    path('intervaldata', views.paramParseByInterval, name='获取时间间隔特征数据'),
]
