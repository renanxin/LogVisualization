import json
import os
import re
import numpy as np
from functools import cmp_to_key


#   处理源信息(1.0)
# def metaInfoCreate(fileName):
#     baseDir = os.path.dirname(os.path.abspath(__name__))
#     ips = set()
#     accounts = set()
#     metaInfo = {}
#     with open(os.path.join(baseDir, 'tmp', fileName)) as f:
#         logs = json.load(f)
#         metaInfo['beginTime'] = logs[0]['time']
#         metaInfo['endTime'] = logs[-1]['time']
#         metaInfo['ipDetail'] = {}
#         metaInfo['accountDetail'] = {}
#         for log in logs:
#             # 遇到新的IP
#             if log['ip'] not in ips:
#                 ips.add(log['ip'])
#                 metaInfo['ipDetail'][log['ip']] = [0, 0, 0]
#             # 遇到新的account
#             if log['account'] not in accounts:
#                 accounts.add(log['account'])
#                 metaInfo['accountDetail'][log['account']] = [0, 0, 0]
#             # 判断此次访问的结果
#             if log['status']['code'] == 0:
#                 metaInfo['ipDetail'][log['ip']][0] += 1
#                 metaInfo['accountDetail'][log['account']][0] += 1
#             elif log['status']['code'] == 1:
#                 metaInfo['ipDetail'][log['ip']][0] += 1
#                 metaInfo['accountDetail'][log['account']][1] += 1
#             elif log['status']['code'] == 2:
#                 metaInfo['ipDetail'][log['ip']][0] += 1
#                 metaInfo['accountDetail'][log['account']][2] += 1
#             elif log['status']['code'] == 3:
#                 metaInfo['ipDetail'][log['ip']][1] += 1
#             else:
#                 metaInfo['ipDetail'][log['ip']][2] += 1
#
#         metaInfo['ipNum'] = len(ips)
#         metaInfo['accountNum'] = len(accounts)
#         metaInfo['filename'] = fileName
#
#     print(ips)
#     with open(os.path.join(baseDir, 'tmp', 'meta', fileName), 'w') as f:
#         json.dump(metaInfo, f)



beginTime = np.zeros((4,),dtype=int)        # 起始时间，表示为年、时、分、秒
beginTime[0] = 2020
beginTime[1] = 14
beginTime[2] = 6
beginTime[3] = 54
dayOfMonth = [[31,28,31,30,31,30,31,31,30,31,30,31],       # 每个月对应的天数
              [31,29,31,30,31,30,31,31,30,31,30,31]]
pastDays = 0            # 起始时间距当年1月1日的天数
scale = np.array([3600*24,3600,60,1])       # 两个时间点的差距，分别为天、时、分、秒

def getDays(year):
    if year%4==0 and year%100!=0:
        return 366
    if year%400==0:
        return 366
    return 365


# 将字符型日期转化为距起始时间的秒数
def strToTime(strDate,setBeginTime=False):
    '''
    :param strDate: 时间
    :param setBeginTime: 是否设定初始时间
    :return:
    '''
    global pastDays
    passTime = np.zeros((4,),dtype=int)
    strDate = strDate[:-4]
    now = re.split('-|:|[ ]', strDate)
    now = np.array(now,dtype=int)
    if not setBeginTime:
        beginYear = beginTime[0]
    else:
        beginYear = now[0]
    while now[0]>beginYear:
        passTime[0] += getDays(beginYear)
        beginYear += 1
    yearType = getDays(now[0]) - 365
    for i in range(now[1]-1):
        passTime[0] += dayOfMonth[yearType][i]
    passTime[0] += (now[2]-1)
    # 仅仅初始化开始时间
    if setBeginTime:
        pastDays = passTime[0]
        beginTime[0] = now[0]
        beginTime[1:] = now[3:]
        return
    passTime[0] -= pastDays
    passTime[1:] = now[3:]-beginTime[1:]
    time = np.sum(passTime * scale)
    return time



def compare(json1,json2):
    if json1['time']<json2['time']:
        return -1
    elif json1['time']>json2['time']:
        return 1
    return 0



# 处理源信息(2.0)
def metaInfoCreate(fileName):
    baseDir = os.path.dirname(os.path.abspath(__name__))
    ips = set()
    # accounts = set()
    metaInfo = {}
    rtnCodeType = set()     # 结果码种类
    rtnCodeType.add('000000')
    rtnCodeType.add('900006')
    with open(os.path.join(baseDir, 'tmp', fileName)) as f:
        logs = json.load(f)
        begin = -1
        beginStr = None
        end = -1
        endStr = None
        metaInfo['ipDetail'] = {}
        metaInfo['accountDetail'] = {}

        # 添加time项表示距特定时间所过去的秒
        strToTime('2020-1-1 00:00:00.000',True)
        minTime = float(strToTime(logs[0]['_source']['operationTime']))
        for log in logs:
            log['time'] = float(strToTime(log['_source']['operationTime']))
            minTime = min(minTime,log['time'])

        # 将原始json转化为目标格式
        for log in logs:
            log['time'] -= minTime
            log['ip'] = log['_source']['clientIP']
            del log['_source']['clientIP']
            log['timeStr'] = log['_source']['operationTime']
            del log['_source']['operationTime']
            result = json.loads(log['_source']['operationResult'])
            log['status'] = {}
            if result['rtnCode'] == '000000':
                log['status']['code'] = 0
            elif result['rtnCode'] == '900006':
                log['status']['code'] = 2
            else:
                log['status']['code'] = -1
            del log['_source']['operationResult']
        logs = sorted(logs,key=cmp_to_key(compare))     # 按照时间排序

        for log in logs:
            if log['status']['code'] >-1:
                endStr = log['timeStr']
                end = log['time']
                if begin==-1:
                    beginStr = log['timeStr']
                    begin = log['time']
            # 遇到新的IP
            if log['ip'] not in ips:
                ips.add(log['ip'])
                metaInfo['ipDetail'][log['ip']] = [0, 0, 0]
            # 遇到新的account
            # if log['account'] not in accounts:
            #     accounts.add(log['account'])
            #     metaInfo['accountDetail'][log['account']] = [0, 0, 0]
            # 判断此次访问的结果
            if log['status']['code'] == 0:       # 成功状态
                metaInfo['ipDetail'][log['ip']][0] += 1
                # metaInfo['accountDetail'][log['account']][0] += 1
            elif log['status']['code'] == 1:     # 封禁状态
                metaInfo['ipDetail'][log['ip']][2] += 1
                # metaInfo['accountDetail'][log['account']][1] += 1

        metaInfo['beginTime'] = begin
        metaInfo['beginTimeStr'] = beginStr
        metaInfo['endTime'] = end
        metaInfo['endTimeStr'] = endStr
        metaInfo['ipNum'] = len(ips)
        # metaInfo['accountNum'] = len(accounts)
        metaInfo['filename'] = fileName


    with open(os.path.join(baseDir, 'tmp', 'meta', fileName), 'w') as f:
        json.dump(metaInfo, f)
    with open(os.path.join(baseDir, 'tmp', fileName), 'w') as f:
        json.dump(logs, f)