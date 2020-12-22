import os
import json
import numpy as np


# 基于时间间隔的分析

def onlineAnalyseLine(name, deltaTime, viewObject, viewTarget, beginTime, endTime):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    fileName = os.path.join(baseDir, 'tmp', name)  # 日志文件路径
    metainfo = os.path.join(baseDir, 'tmp', 'meta', name)  # 元信息文件路径

    viewobject = 'ip'  # 默认统计ip
    if viewObject == 1:  # 统计账户
        viewobject = 'account'

    # 如果未传入观察对象，则设定为全部对象
    if len(viewTarget) == 0:
        with open(metainfo) as file:  # 根据元数据进行观察目标初始化
            metas = json.load(file)
            detail = 'ipDetail'
            if viewObject == 1:
                detail = 'accountDetail'
            for key in metas[detail].keys():
                viewTarget.append(key)

    viewTargets = set()
    for target in viewTarget:
        viewTargets.add(target)

    timeAcculate = {}  # 每个观察对象上一个访问时连续在线时长
    preAccess = {}  # 每个观察对象上一次的访问时间
    preState = {}  # 上一次访问的状态

    onlineTime = {}  # 每次访问时连续在线时长
    state = {}  # 每次访问的结果
    timeStr = {}  # 观察目标每次访问的时间

    for target in viewTarget:
        timeAcculate[target] = 0
        preAccess[target] = -1
        onlineTime[target] = []
        state[target] = []
        preState[target] = 0
        timeStr[target] = []

    with open(fileName) as file:
        infos = json.load(file)
        for info in infos:
            if info['time'] > endTime:
                break
            tmp_key = info[viewobject]  # 此次访问对象 ip/账户
            code = info['status']['code']  # 此次访问结果状态码
            if tmp_key not in viewTargets:
                continue
            if preAccess[tmp_key] == -1:  # 此对象第一次访问
                preAccess[tmp_key] = info['time']
                preState[tmp_key] = code
                continue

            if info['time'] - preAccess[tmp_key] > deltaTime:  # 中途下线了
                timeAcculate[tmp_key] = 0
            else:
                timeAcculate[tmp_key] += (info['time'] - preAccess[tmp_key])
            if code == 2:
                if preState[tmp_key] == 2:  # 不是第一次封禁
                    preAccess[tmp_key] = info['time']
                    continue
            preState[tmp_key] = code
            preAccess[tmp_key] = info['time']
            if info['time'] < beginTime:  # 为进入观察范围
                continue
            onlineTime[tmp_key].append(timeAcculate[tmp_key])
            timeStr[tmp_key].append(info['timeStr'])
            state[tmp_key].append(code)

    for key in viewTarget:
        res[key] = {'time': timeStr[key], 'feature': timeAcculate[key], 'state': state[key]}

    for key in viewTarget:
        tmp = np.concatenate(
            (np.array(res[key]['time']).reshape((-1, 1)), np.array(res[key]['feature']).reshape((-1, 1)),
             np.array(res[key]['state']).reshape((-1, 1))), axis=1).tolist()
        combine = []

        idx = 0
        for i in range(len(res[key]['time']) + 1):
            if i == len(res[key]['time']) or res[key]['state'][i] == 2:
                k = 1
                if i == len(res[key]['time']):
                    k = 0
                combine.append(tmp[idx:i + k])
                idx = i + 1
        res[key] = combine
    return res


# 基于频率分析的盒线图
""" count中5个数组对应的5种状态变化
0   安全->怀疑
1   安全->封禁
2   怀疑->安全
3   封禁->安全
4   怀疑->封禁
"""


def onlineAnalyseBox(name, deltaTime, viewObject, viewTarget, beginTime, endTime):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    fileName = os.path.join(baseDir, 'tmp', name)  # 原始文件路径
    metainfo = os.path.join(baseDir, 'tmp', 'meta', name)  # 元信息文件路径

    viewobject = 'ip'  # 默认统计ip
    if viewObject == 1:  # 统计账户
        viewobject = 'account'

    # 如果未传入观察对象，则设定为全部对象
    if len(viewTarget) == 0:
        with open(metainfo) as file:  # 根据元数据进行观察目标初始化
            metas = json.load(file)
            detail = 'ipDetail'
            if viewObject == 1:
                detail = 'accountDetail'
            for key in metas[detail].keys():
                viewTarget.append(key)

    viewTargets = set()
    for target in viewTarget:
        viewTargets.add(target)

    timeAcculate = {}  # 每个观察对象上一个访问时连续在线时长
    preAccess = {}  # 每个观察对象上一次的访问时间
    preState = {}  # 上一次访问的状态

    onlineTime = {}  # 每次访问时连续在线时长

    for key in viewTargets:
        timeAcculate[key] = 0
        preAccess[key] = -1
        preState[key] = 0

        onlineTime[key] = [[], [], [], [], []]

    with open(fileName) as file:
        infos = json.load(file)
    for info in infos:
        if info['time'] > endTime:
            break
        tmp_key = info[viewobject]
        if tmp_key not in viewTargets:
            continue
        code = info['status']['code']
        # 该观察对象的第一次访问
        if preAccess[tmp_key] == -1:
            preAccess[tmp_key] = info['time']
            preState[tmp_key] = code
            continue

        if info['time'] - preAccess[tmp_key] > deltaTime:  # 间隔访问时间过长，判断为下线
            timeAcculate[tmp_key] = 0
        else:
            timeAcculate[tmp_key] += (info['time'] - preAccess[tmp_key])
        # 发生状态改变且在目标时间范围内
        if code != preState[tmp_key] and info['time']>beginTime:
            if preAccess[tmp_key] == 0:
                if code == 1:
                    preAccess[tmp_key][0].append(timeAcculate[tmp_key])
                else:
                    preAccess[tmp_key][1].append(timeAcculate[tmp_key])
            elif preAccess[tmp_key] == 1:
                if code==0:
                    preAccess[tmp_key][2].append(timeAcculate[tmp_key])
                else:
                    preAccess[tmp_key][4].append(timeAcculate[tmp_key])
            else:
                preAccess[tmp_key][3].append(timeAcculate[tmp_key])
        preState[tmp_key] = code
    for key in preState.keys():
        res[key] = []
        for i in range(5):
            res[key].append([np.min(preState[key][i]), np.mean(preState[key][i]), np.max(preState[key][i]), np.std(preState[key][i])])
    return res
