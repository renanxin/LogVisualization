import os
import json

def freAnalyseLine(fileName,windowsType,viewObject,viewTarget,beginTime,endTime,windowsSize):
    res = {}
    baseDir = os.path.dirname(os.path.abspath(__name__))
    fileName = os.path.join(baseDir, 'tmp', fileName)
    metainfo = os.path.join(baseDir, 'tmp','meta', fileName)
    if windowsType == 1:        # 使用的是时间窗口
        viewobject = 'ip'           # 默认统计ip
        if viewObject == 1:         # 统计账户
            viewobject = 'account'

        if viewTarget != 'all':         # 统计特定的目标
            tmp = []
            time = []       # 每次访问的时间节点
            count = []      # 每次访问的时间窗口内频数
            states = []      # 每次访问的状态
            flag = False
            with open(fileName) as file:
                infos = json.load(file)
                if endTime == -1:
                    endTime = infos[-1]['time']
                for info in infos:
                    if info['time'] < beginTime:
                        continue
                    elif info['time'] > endTime:
                        break
                    if info[viewobject] == viewTarget:
                        if info['time'] - windowsSize > tmp[0][0]:
                            flag = True
                            while info['time'] - windowsSize > tmp[0][0]:
                                del tmp[0]

                        tmp.append([info['time']])
                        if flag:
                            time.append(info['time'])
                            count.append(len(tmp))
            res[viewTarget] = {'time':time,'count':count}

        else:
            ips = {}

    else:
        pass
    return res

print(freAnalyseLine('agents_1.json',1,0,'192.168.1.5',0,-1,200))