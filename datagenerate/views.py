from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect
import json
# Create your views here.


# 分析前端传过来的参数调用不同的分析函数
from datagenerate.methos.freAnalyse import freAnalyseLine,freAnalyseBox
from datagenerate.methos.intervalAnalyse import intervalAnalyseLine, intervalAnalyseBox


def paramParseByFre(request):
    fileName = request.POST.get('fileName')  # 获取解析文件名
    windowsType = int(request.POST.get('windowsType', 0))  # 获取窗口类型，默认为0(时间窗口)
    viewObject = int(request.POST.get('viewObject', 0))  # 获取观察对象，默认为0(ip)
    viewTarget = request.POST.getlist('viewTarget', [])  # 获取目标，默认为all(全部目标）
    beginTime = int(request.POST.get('beginTime', 0))  # 开始时间，默认为0
    endTime = int(request.POST.get('endTime', -1))  # 结束时间，默认为-1(最大时间值）
    windowsSize = int(request.POST.get('windowsSize', 200))  # 特征窗口大小，默认为200

    res = {'code': 200}
    if beginTime >= endTime and endTime != -1:
        res['code'] = 410

    if res['code'] != 200:  # 传送的参数错误，直接返回
        return HttpResponse(json.dumps(res), content_type="application/json")

    res['lineData'] = freAnalyseLine(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
    res['boxData'] = freAnalyseBox(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)

    return HttpResponse(json.dumps(res), content_type="application/json")



def paramParseByInterval(request):
    fileName = request.POST.get('fileName')  # 获取解析文件名
    windowsType = int(request.POST.get('windowsType', 0))  # 获取窗口类型，默认为0(时间窗口)
    viewObject = int(request.POST.get('viewObject', 0))  # 获取观察对象，默认为0(ip)
    viewTarget = request.POST.getlist('viewTarget', [])  # 获取目标，默认为all(全部目标）
    beginTime = int(request.POST.get('beginTime', 0))  # 开始时间，默认为0
    endTime = int(request.POST.get('endTime', -1))  # 结束时间，默认为-1(最大时间值）
    windowsSize = int(request.POST.get('windowsSize', 200))  # 特征窗口大小，默认为200

    res = {'code': 200}
    if beginTime >= endTime and endTime != -1:
        res['code'] = 410

    if res['code'] != 200:  # 传送的参数错误，直接返回
        return HttpResponse(json.dumps(res), content_type="application/json")

    res['lineData'] = intervalAnalyseLine(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
    # res['boxData'] = intervalAnalyseBox(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)

    return HttpResponse(json.dumps(res), content_type="application/json")