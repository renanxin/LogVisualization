import os
import json
import numpy as np


# 基于频率的分析
def freAnalyseLine(name, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    # baseDir = 'C:\\Users\\renwei\\Desktop\\日志可视化\\LogVisualization'
    fileName = os.path.join(baseDir, 'tmp', name)
    metainfo = os.path.join(baseDir, 'tmp', 'meta', name)

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

    if windowsType == 0:  # 使用的是时间窗口


        tmp = {}  # 节点历史访问时间
        timeStr = {}  # 每次访问的格式化时间
        count = {}  # 每次访问的时间窗口内频数
        state = {}  # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
        flag = {}  # 记录tmp中是否出现过时间跨度大于windowsSize
        ignore = {}  # 记录每个ip是否处于连续访问封禁中

        for key in viewTarget:
            tmp[key] = []
            timeStr[key] = []
            count[key] = []
            state[key] = []
            flag[key] = False
            ignore[key] = False


        with open(fileName) as file:
            infos = json.load(file)  # 加载日志信息
            if endTime == -1:  # 如果结束时间没有设置
                endTime = infos[-1]['time']
            for info in infos:
                if info['time'] > endTime:
                    break
                tmp_key = info[viewobject]
                if tmp_key not in viewTargets:
                    continue
                tmp[tmp_key].append(info['time'])
                if info['time'] - windowsSize > tmp[tmp_key][0]:
                    flag[tmp_key] = True
                    while info['time'] - windowsSize > tmp[tmp_key][0]:
                        del tmp[tmp_key][0]

                if info['time'] >= beginTime:
                    if flag[tmp_key]:
                        code = info['status']['code']  # 得到此次访问的状态码
                        if code >=0 and code < 3  and not (code == 2 and ignore[info[viewobject]]):
                            timeStr[tmp_key].append(info['timeStr'])
                            count[tmp_key].append(len(tmp[tmp_key]))

                            if code == 0:
                                ignore[tmp_key] = False
                                state[tmp_key].append(0)
                            elif code == 1:
                                ignore[tmp_key] = False
                                state[tmp_key].append(1)
                            else:
                                ignore[tmp_key] = True
                                state[tmp_key].append(2)
        for key in viewTarget:
            res[key] = {'time':timeStr[key],'count':count[key],'state':state[key]}

    else:  # 使用的是次数窗口
        tmp = {}  # 节点历史访问时间
        timeStr = {}  # 每次访问的格式化时间
        count = {}  # 每次访问的时间窗口内频数
        state = {}  # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
        ignore = {}

        for key in viewTarget:
            tmp[key] = []
            timeStr[key] = []
            count[key] = []
            state[key] = []
            ignore[key] = False


        with open(fileName) as file:
            infos = json.load(file)  # 加载日志信息
            if endTime == -1:  # 如果结束时间没有设置
                endTime = infos[-1]['time']
            for info in infos:
                if info['time'] > endTime:
                    break
                if info[viewobject] not in viewTargets:
                    continue
                tmp[info[viewobject]].append(info['time'])
                if len(tmp[info[viewobject]]) == windowsSize:
                    if info['time'] >= beginTime:
                        code = info['status']['code']  # 得到此次访问的状态码
                        if code >=0 and code < 3  and not (code == 2 and ignore[info[viewobject]]):
                            timeStr[info[viewobject]].append(info['timeStr'])
                            count[info[viewobject]].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                            if code == 0:
                                ignore[info[viewobject]] = False
                                state[info[viewobject]].append(0)
                            elif code == 1:
                                ignore[info[viewobject]] = False
                                state[info[viewobject]].append(1)
                            else:
                                ignore[info[viewobject]] = True
                                state[info[viewobject]].append(2)
                    del tmp[info[viewobject]][0]

        for key in state.keys():
            res[key] = {'time': timeStr[key], 'count': count[key], 'state': state[key]}

    for key in viewTarget:
        tmp = np.concatenate((np.array(res[key]['time']).reshape((-1,1)),np.array(res[key]['count']).reshape((-1,1)),np.array(res[key]['state']).reshape((-1,1))),axis=1).tolist()
        combine = []


        idx = 0
        for i in range(len(res[key]['time']) + 1):
            if i == len(res[key]['time']) or res[key]['state'][i] == 2:
                k = 1
                if i == len(res[key]['time']):
                    k=0
                combine.append(tmp[idx:i + k])
                idx = i + 1
        res[key] = combine
    return res

# print(freAnalyseLine('agents_1.json',1,0,'192.168.1.5',3000,20000,1000)['192.168.1.5']['count'])







# 基于频率分析的盒线图
""" count中5个数组对应的5种状态变化
0   安全->怀疑
1   安全->封禁
2   怀疑->安全
3   封禁->安全
4   怀疑->封禁
"""


def freAnalyseBox(name, windowsType, viewObject, viewTarget, beginTime, endTime, windowsSize):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    # baseDir = 'C:\\Users\\renwei\\Desktop\\日志可视化\\LogVisualization'
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


    if windowsType == 1:  # 使用的是次数窗口
        tmp = {}
        count = {}  # 记录每次状态转变时的特征
        preState = {}  # 前一次访问的状态
        for key in viewTarget:
            tmp[key] = []
            count[key] = [[], [], [], [], []]
            preState[key] = -1

        with open(fileName) as file:
            infos = json.load(file)
        if endTime == -1:  # 如果结束时间没有设置
            endTime = infos[-1]['time']
        for info in infos:
            if info['time'] > endTime:
                break
            if info[viewobject] not in viewTargets:
                continue
            tmp[info[viewobject]].append(info['time'])
            code = info['status']['code']  # 得到此次访问的状态码
            # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
            if code == 0:
                state = 0
            elif code == 1:
                state = 1
            else:
                state = 2
            if len(tmp[info[viewobject]]) == windowsSize:
                if state != preState[info[viewobject]] and info['time'] > beginTime and preState[
                    info[viewobject]] != -1:  # 发生状态变化且时间符合条件
                    if state == 0:
                        if preState[info[viewobject]] == 1:  # 怀疑->安全
                            count[info[viewobject]][2].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                        else:  # 封禁->安全
                            count[info[viewobject]][3].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                    elif state == 1:
                        if preState[info[viewobject]] == 0:  # 安全->怀疑
                            count[info[viewobject]][0].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                    elif state == 2:
                        if preState[info[viewobject]] == 0:  # 安全->封禁
                            count[info[viewobject]][1].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                        else:  # 怀疑->封禁
                            count[info[viewobject]][4].append(tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                del tmp[info[viewobject]][0]  # 清除首记录
            preState[info[viewobject]] = state  # 记录前一次状态
        res = count


    else:  # 使用的是时间窗口
        tmp = {}
        count = {}  # 记录每次状态转变时的特征
        preState = {}  # 前一次访问的状态
        flag = {}
        for key in viewTarget:
            tmp[key] = []
            count[key] = [[], [], [], [], []]
            preState[key] = -1
            flag[key] = False

        with open(fileName) as file:
            infos = json.load(file)
        if endTime == -1:  # 如果结束时间没有设置
            endTime = infos[-1]['time']
        for info in infos:
            if info['time'] > endTime:
                break
            if info[viewobject] not in viewTargets:
                continue
            tmp[info[viewobject]].append(info['time'])
            if info['time'] - tmp[info[viewobject]][0] >= windowsSize:
                flag[info[viewobject]] = True
                while info['time'] - tmp[info[viewobject]][0] > windowsSize:
                    del tmp[info[viewobject]][0]
            code = info['status']['code']  # 得到此次访问的状态码
            # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
            if code == 0:
                state = 0
            elif code == 1:
                state = 1
            else:
                state = 2
            if flag[info[viewobject]]:  # 满足记录条件
                if state != preState[info[viewobject]] and info['time'] > beginTime and preState[
                    info[viewobject]] != -1:  # 发生状态变化且时间符合条件
                    if state == 0:
                        if preState[info[viewobject]] == 1:  # 怀疑->安全
                            count[info[viewobject]][2].append(
                                tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                        else:  # 封禁->安全
                            count[info[viewobject]][3].append(
                                tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                    elif state == 1:
                        if preState[info[viewobject]] == 0:  # 安全->怀疑
                            count[info[viewobject]][0].append(
                                tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                    elif state == 2:
                        if preState[info[viewobject]] == 0:  # 安全->封禁
                            count[info[viewobject]][1].append(
                                tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
                        else:  # 怀疑->封禁
                            count[info[viewobject]][4].append(
                                tmp[info[viewobject]][-1] - tmp[info[viewobject]][0])
            preState[info[viewobject]] = state  # 记录前一次状态
        res = count
    for key in res.keys():
        for i in range(len(res[key])):
            tmp = []
            if len(res[key][i])>0:
                tmp.append(np.min(np.array(res[key][i],dtype=float)))
                tmp.append(np.mean(np.array(res[key][i],dtype=float)))
                tmp.append(np.max(np.array(res[key][i],dtype=float)))
                tmp.append(np.std(np.array(res[key][i],dtype=float)))
            res[key][i] = tmp
    return res

# print(freAnalyseBox('agents_1.json',0,1,'255.168.89.5',0,-1,200))
