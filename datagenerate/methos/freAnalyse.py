import os
import json


# 基于频率的分析
def freAnalyseLine(name,windowsType,viewObject,viewTarget,beginTime,endTime,windowsSize):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    # baseDir = 'C:\\Users\\renwei\\Desktop\\日志可视化\\LogVisualization'
    fileName = os.path.join(baseDir, 'tmp', name)
    metainfo = os.path.join(baseDir,'tmp','meta', name)

    viewobject = 'ip'  # 默认统计ip
    if viewObject == 1:  # 统计账户
        viewobject = 'account'

    if windowsType == 1:        # 使用的是时间窗口

        if viewTarget != 'all':         # 统计特定的目标
            tmp = []
            time = []           # 每次访问的时间节点
            count = []          # 每次访问的时间窗口内频数
            states = []         # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
            flag = False        # 记录tmp中是否出现过时间跨度大于windowsSize
            with open(fileName) as file:
                infos = json.load(file)     # 加载日志信息
                if endTime == -1:           # 如果结束时间没有设置
                    endTime = infos[-1]['time']
                for info in infos:
                    if info['time'] > endTime:
                        break
                    if info[viewobject] == viewTarget:
                        tmp.append(info['time'])
                        if  info['time'] - windowsSize > tmp[0]:
                            flag = True
                            while info['time'] - windowsSize > tmp[0]:
                                del tmp[0]

                        if info['time'] >= beginTime:
                            if flag:
                                time.append(info['time'])
                                count.append(len(tmp))
                                code = info['status']['code']       # 得到此次访问的状态码
                                if code == 0:
                                    states.append(0)
                                elif code == 1 or code == 3:
                                    states.append(1)
                                else:
                                    states.append(2)
            res[viewTarget] = {'time':time,'count':count,'state':states}
        else:                           # 统计所有的目标
            tmp = {}   # 节点历史访问时间
            time = {}  # 每次访问的时间节点
            count = {}  # 每次访问的时间窗口内频数
            states = {}  # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
            flag = {}
            with open(metainfo) as file:        # 根据元数据进行观察目标初始化
                metas = json.load(file)
                detail = 'ipDetail'
                if viewObject==1:
                    detail = 'accountDetail'
                for key in metas[detail].keys():
                    tmp[key] = []
                    time[key] = []
                    count[key] = []
                    states[key] = []
                    flag[key] = False

            with open(fileName) as file:
                infos = json.load(file)         # 加载日志信息
                if endTime == -1:               # 如果结束时间没有设置
                    endTime = infos[-1]['time']
                for info in infos:
                    if info['time'] > endTime:
                        break
                    tmp[info[viewobject]].append(info['time'])
                    if info['time'] - windowsSize > tmp[info[viewobject]][0]:
                        flag[info[viewobject]] = True
                        while info['time'] - windowsSize > tmp[info[viewobject]][0]:
                            del tmp[info[viewobject]][0]

                    if info['time'] >= beginTime:
                        if flag[info[viewobject]]:
                            time[info[viewobject]].append(info['time'])
                            count[info[viewobject]].append(len(tmp[info[viewobject]]))
                            code = info['status']['code']  # 得到此次访问的状态码
                            if code == 0:
                                states[info[viewobject]].append(0)
                            elif code == 1 or code == 3:
                                states[info[viewobject]].append(1)
                            else:
                                states[info[viewobject]].append(2)
            # 写入返回结果
            for key in states.keys():
                res[key] = {'time':time[key],'count':count[key],'state':states[key]}


    else:          # 使用的是次数窗口
        if viewTarget != 'all':         # 统计特定的目标
            tmp = []
            time = []           # 每次访问的时间节点
            count = []          # 每次访问的次数窗口时间跨度
            states = []         # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
            with open(fileName) as file:
                infos = json.load(file)     # 加载日志信息
                if endTime == -1:           # 如果结束时间没有设置
                    endTime = infos[-1]['time']
                for info in infos:
                    if info['time'] > endTime:
                        break
                    if info[viewobject] == viewTarget:
                        tmp.append(info['time'])
                        if len(tmp)==windowsSize:               # 暂存记录中
                            if info['time'] >= beginTime:
                                time.append(info['time'])
                                count.append(tmp[-1]-tmp[0])
                                code = info['status']['code']       # 得到此次访问的状态码
                                if code == 0:
                                    states.append(0)
                                elif code == 1 or code == 3:
                                    states.append(1)
                                else:
                                    states.append(2)
                            del tmp[0]
            res[viewTarget] = {'time':time,'count':count,'state':states}
        else:  # 统计所有的目标
            tmp = {}  # 节点历史访问时间
            time = {}  # 每次访问的时间节点
            count = {}  # 每次访问的时间窗口内频数
            states = {}  # 每次访问的状态 0表示通过 1表示怀疑 2表示封禁
            with open(metainfo) as file:  # 根据元数据进行观察目标初始化
                metas = json.load(file)
                detail = 'ipDetail'
                if viewObject == 1:
                    detail = 'accountDetail'
                for key in metas[detail].keys():
                    tmp[key] = []
                    time[key] = []
                    count[key] = []
                    states[key] = []

            with open(fileName) as file:
                infos = json.load(file)  # 加载日志信息
                if endTime == -1:  # 如果结束时间没有设置
                    endTime = infos[-1]['time']
                for info in infos:
                    if info['time'] > endTime:
                        break
                    tmp[info[viewobject]].append(info['time'])
                    if len(tmp[info[viewobject]]) == windowsSize:
                        if info['time'] >= beginTime:
                            time[info[viewobject]].append(info['time'])
                            count[info[viewobject]].append(tmp[info[viewobject]][-1]-tmp[info[viewobject]][0])
                            code = info['status']['code']  # 得到此次访问的状态码
                            if code == 0:
                                states[info[viewobject]].append(0)
                            elif code == 1 or code == 3:
                                states[info[viewobject]].append(1)
                            else:
                                states[info[viewobject]].append(2)
                        del tmp[info[viewobject]][0]
            # 写入返回结果
            for key in states.keys():
                res[key] = {'time': time[key], 'count': count[key], 'state': states[key]}
        print(res['192.168.1.5']['count'])
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
def freAnalyseBox(name,windowsType,viewObject,viewTarget,beginTime,endTime,windowsSize):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    # baseDir = 'C:\\Users\\renwei\\Desktop\\日志可视化\\LogVisualization'
    fileName = os.path.join(baseDir, 'tmp', name)       # 原始文件路径
    metainfo = os.path.join(baseDir, 'tmp', 'meta', name)       # 元信息文件路径

    viewobject = 'ip'  # 默认统计ip
    if viewObject == 1:  # 统计账户
        viewobject = 'account'

    if windowsType == 0:                # 使用的是次数窗口
        if viewTarget != 'all':         # 观察特定目标
            tmp = []
            count = [[],[],[],[],[]]  # 记录每次状态转变时的特征
            preState = -1  # 前一次访问的状态
            with open(fileName) as file:
                infos = json.load(file)
            if endTime == -1:  # 如果结束时间没有设置
                endTime = infos[-1]['time']
            for info in infos:
                if info['time']>endTime:
                    break
                if info[viewobject] == viewTarget:
                    tmp.append(info['time'])
                    code = info['status']['code']  # 得到此次访问的状态码
                    # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
                    if code == 0:
                        state = 0
                    elif code == 1 or code == 3:
                        state = 1
                    else:
                        state = 2
                    if len(tmp)==windowsSize:
                        if state != preState and info['time']>beginTime and preState!=-1:   # 发生状态变化且时间符合条件
                            if state==0:
                                if preState==1:     # 怀疑->安全
                                    count[2].append(tmp[-1]-tmp[0])
                                else:               # 封禁->安全
                                    count[3].append(tmp[-1]-tmp[0])
                            elif state==1:
                                if preState==0:     # 安全->怀疑
                                    count[0].append(tmp[-1]-tmp[0])
                            elif state==2:
                                if preState==0:     # 安全->封禁
                                    count[1].append(tmp[-1]-tmp[0])
                                else:               # 怀疑->封禁
                                    count[4].append(tmp[-1]-tmp[0])
                        del tmp[0]      # 清除首记录
                    preState = state    # 记录前一次状态

            res[viewTarget] = count


        else:                           # 观察所有目标
            tmp = {}
            count = {}  # 记录每次状态转变时的特征
            preState = {}  # 前一次访问的状态
            with open(metainfo) as file:  # 根据元数据进行观察目标初始化
                metas = json.load(file)
                detail = 'ipDetail'
                if viewObject == 1:
                    detail = 'accountDetail'
                for key in metas[detail].keys():
                    tmp[key] = []
                    count[key] = [[],[],[],[],[]]
                    preState[key] = -1

            with open(fileName) as file:
                infos = json.load(file)
            if endTime == -1:  # 如果结束时间没有设置
                endTime = infos[-1]['time']
            for info in infos:
                if info['time']>endTime:
                    break
                tmp[info[viewobject]].append(info['time'])
                code = info['status']['code']  # 得到此次访问的状态码
                # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
                if code == 0:
                    state = 0
                elif code == 1 or code == 3:
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


    else:              # 使用的是时间窗口
        if viewTarget != 'all':  # 观察特定目标
            tmp = []
            count = [[], [], [], [], []]  # 记录每次状态转变时的特征
            flag = False
            preState = -1  # 前一次访问的状态
            with open(fileName) as file:
                infos = json.load(file)
            if endTime == -1:  # 如果结束时间没有设置
                endTime = infos[-1]['time']
            for info in infos:
                if info['time'] > endTime:
                    break
                if  info[viewobject] == viewTarget:
                    tmp.append(info['time'])
                    if info['time']-tmp[0] >=windowsSize:
                        flag = True
                        while info['time']-tmp[0] >windowsSize:     # 清除时间窗口之外的记录
                            del tmp[0]
                    code = info['status']['code']  # 得到此次访问的状态码
                    # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
                    if code == 0:
                        state = 0
                    elif code == 1 or code == 3:
                        state = 1
                    else:
                        state = 2
                    if flag:    # 满足记录条件
                        if state != preState and info['time'] > beginTime and preState != -1:  # 发生状态变化且时间符合条件
                            if state == 0:
                                if preState == 1:  # 怀疑->安全
                                    count[2].append(tmp[-1] - tmp[0])
                                else:  # 封禁->安全
                                    count[3].append(tmp[-1] - tmp[0])
                            elif state == 1:
                                if preState == 0:  # 安全->怀疑
                                    count[0].append(tmp[-1] - tmp[0])
                            elif state == 2:
                                if preState == 0:  # 安全->封禁
                                    count[1].append(tmp[-1] - tmp[0])
                                else:  # 怀疑->封禁
                                    count[4].append(tmp[-1] - tmp[0])
                    preState = state  # 记录前一次状态

            res[viewTarget] = count


        else:       # 观察所有目标
            tmp = {}
            count = {}  # 记录每次状态转变时的特征
            preState = {}  # 前一次访问的状态
            flag = {}
            with open(metainfo) as file:  # 根据元数据进行观察目标初始化
                metas = json.load(file)
                detail = 'ipDetail'
                if viewObject == 1:
                    detail = 'accountDetail'
                for key in metas[detail].keys():
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
                tmp[info[viewobject]].append(info['time'])
                if info['time'] - tmp[info[viewobject]][0]>=windowsSize:
                    flag[info[viewobject]] = True
                    while info['time'] - tmp[info[viewobject]][0] > windowsSize:
                        del tmp[info[viewobject]][0]
                code = info['status']['code']  # 得到此次访问的状态码
                # 获取访问的状态 0表示通过 1表示怀疑 2表示封禁
                if code == 0:
                    state = 0
                elif code == 1 or code == 3:
                    state = 1
                else:
                    state = 2
                if flag[info[viewobject]]:      # 满足记录条件
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

    return res


# print(freAnalyseBox('agents_2.json',0,0,'all',0,-1,200))