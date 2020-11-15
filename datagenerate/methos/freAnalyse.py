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
                        if len(tmp)>1 and info['time'] - windowsSize > tmp[0]:
                            flag = True
                            while info['time'] - windowsSize > tmp[0]:
                                del tmp[0]

                        tmp.append(info['time'])
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
                    if len(tmp[info[viewobject]])>1 and info['time'] - windowsSize > tmp[info[viewobject]][0]:
                        flag[info[viewobject]] = True
                        while info['time'] - windowsSize > tmp[info[viewobject]][0]:
                            del tmp[info[viewobject]][0]

                    tmp[info[viewobject]].append(info['time'])
                    if info['time'] >= beginTime:
                        if flag[info[viewobject]]:
                            time[info[viewobject]].append(info['time'])
                            count[info[viewobject]].append(len(tmp))
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
                            count[info[viewobject]].append(len(tmp))
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
    return res

print(freAnalyseLine('agents_1.json',0,0,'192.168.1.5',10000,20000,1000))