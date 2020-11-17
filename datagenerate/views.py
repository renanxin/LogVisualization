from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect
import json
# Create your views here.


# 分析前端传过来的参数调用不同的分析函数
from datagenerate.methos.freAnalyse import freAnalyseLine,freAnalyseBox


def paramParse(request):
    fileName = request.POST.get('fileName')  # 获取解析文件名
    fileName = 'agents_1.json'
    featureType = int(request.POST.get('featureType', 0))  # 获取特征类型，默认为0(频率)
    windowsType = int(request.POST.get('windowsType', 0))  # 获取窗口类型，默认为0(时间窗口)
    viewObject = int(request.POST.get('viewObject', 0))  # 获取观察对象，默认为0(ip)
    viewTarget = request.POST.get('viewTarget', 'all')  # 获取目标，默认为all(全部目标）
    beginTime = int(request.POST.get('beginTime', 0))  # 开始时间，默认为0
    endTime = int(request.POST.get('endTime', -1))  # 结束时间，默认为-1(最大时间值）
    windowsSize = int(request.POST.get('windowsSize', 200))  # 特征窗口大小，默认为200

    res = {'error': 0}
    if beginTime >= endTime and endTime != -1:
        res['error'] = 1
        res['error_msg'] = '开始时间应小于结束时间'

    if res['error'] != 0:  # 传送的参数错误，直接返回
        return HttpResponse(json.dumps(res), content_type="application/json")

    if featureType == 0:
        res['lineData'] = freAnalyseLine(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
        res['boxData'] = freAnalyseBox(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
    else:
        pass

    return HttpResponse(json.dumps(res), content_type="application/json")
