from django.shortcuts import render
from django.http import request,HttpResponse,HttpResponseRedirect
import os
import json
# Create your views here.
from filemanager.utils import metaInfoCreate


# 跳转首页
def index(request):
    return HttpResponseRedirect("/static/html/index.html")

# 跳转文件上传页面
def upload(request):
    return HttpResponseRedirect("/static/html/fileUpload.html")

#   处理文件上传
def fileUpload(request):
    files = request.FILES.getlist('upload')
    baseDir = os.path.dirname(os.path.abspath(__name__))
    for file in files:
        with open(os.path.join(baseDir,'tmp',file.name),'wb') as f:
            for chrunk in file.chunks():
                f.write(chrunk)
            f.flush()
        metaInfoCreate(file.name)
    return HttpResponseRedirect("/")


# 获取所有的元信息
def getAllMetaInfo(request):
    baseDir = os.path.dirname(os.path.abspath(__name__))
    metaDir = os.path.join(baseDir, 'tmp', 'meta')
    filesName = os.listdir(metaDir)
    res = []
    for fileName in filesName:
        with open(os.path.join(metaDir, fileName)) as f:
            info = json.load(f)
        res.append(info)
    return HttpResponse(json.dumps(res), content_type="application/json")
