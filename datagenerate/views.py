from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect
import json
import os
# Create your views here.


# 分析前端传过来的参数调用不同的分析函数
from datagenerate.methos.freAnalyse import freAnalyseLine,freAnalyseBox
from datagenerate.methos.intervalAnalyse import intervalAnalyseLine, intervalAnalyseBox
from filemanager.utils import strToTime


def frequencydata(request):
    fileName = request.POST.get('fileName')  # 获取解析文件名
    windowsType = int(request.POST.get('windowsType', 0))  # 获取窗口类型，默认为0(时间窗口)
    viewObject = int(request.POST.get('viewObject', 0))  # 获取观察对象，默认为0(ip)
    viewTarget = request.POST.getlist('viewTarget', [])  # 获取目标，默认为all(全部目标）
    beginTime = int(request.POST.get('beginTime', ''))  # 开始时间，默认为0
    endTime = int(request.POST.get('endTime', ''))  # 结束时间，默认为-1(最大时间值）
    windowsSize = int(request.POST.get('windowsSize', 200))  # 特征窗口大小，默认为200

    res = {'error': 0}

    # 将beginTime和endTime转化为数值型
    baseDir = os.path.dirname(os.path.abspath(__name__))
    with open(os.path.join(baseDir, 'tmp', 'meta', fileName)) as f:
        metaData = json.load(f)
    if len(beginTime)==0:
        beginTime = 0
    else:
        strToTime(metaData['beginTimeStr'],True)
        beginTime = strToTime(beginTime)

    if len(endTime) == 0:
        endTime = metaData['endTime']
    else:
        strToTime(metaData['beginTimeStr'], True)
        endTime = strToTime(endTime)


    if beginTime >= endTime and endTime != -1:
        res['error'] = 1
        res['error_msg'] = '开始时间应小于结束时间'

    if res['error'] != 0:  # 传送的参数错误，直接返回
        return HttpResponse(json.dumps(res), content_type="application/json")

    res['lineData'] = freAnalyseLine(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
    res['boxData'] = freAnalyseBox(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)

    return HttpResponse(json.dumps(res), content_type="application/json")



def intervaldata(request):
    fileName = request.POST.get('fileName')  # 获取解析文件名
    windowsType = int(request.POST.get('windowsType', 0))  # 获取窗口类型，默认为0(时间窗口)
    viewObject = int(request.POST.get('viewObject', 0))  # 获取观察对象，默认为0(ip)
    viewTarget = request.POST.getlist('viewTarget', [])  # 获取目标，默认为all(全部目标）
    beginTime = int(request.POST.get('beginTime', ''))  # 开始时间，默认为0
    endTime = int(request.POST.get('endTime', ''))  # 结束时间，默认为-1(最大时间值）
    windowsSize = int(request.POST.get('windowsSize', 200))  # 特征窗口大小，默认为200

    res = {'error': 0}

    # 将beginTime和endTime转化为数值型
    baseDir = os.path.dirname(os.path.abspath(__name__))
    with open(os.path.join(baseDir, 'tmp', 'meta', fileName)) as f:
        metaData = json.load(f)
    if len(beginTime)==0:
        beginTime = 0
    else:
        strToTime(metaData['beginTimeStr'],True)
        beginTime = strToTime(beginTime)

    if len(endTime) == 0:
        endTime = metaData['endTime']
    else:
        strToTime(metaData['beginTimeStr'], True)
        endTime = strToTime(endTime)


    if beginTime >= endTime and endTime != -1:
        res['error'] = 1
        res['error_msg'] = '开始时间应小于结束时间'

    if res['error'] != 0:  # 传送的参数错误，直接返回
        return HttpResponse(json.dumps(res), content_type="application/json")

    res['lineData'] = intervalAnalyseLine(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)
    res['boxData'] = intervalAnalyseBox(fileName, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize)

    return HttpResponse(json.dumps(res), content_type="application/json")
