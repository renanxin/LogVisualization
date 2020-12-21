from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.fileUpload, name='处理文件上传'),
    path('fileupload', views.upload, name='文件上传'),
    path('metadata', views.getAllMetaInfo, name="获取元信息")
]
