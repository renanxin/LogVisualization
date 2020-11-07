import json
import os


#   处理源信息
def metaInfoCreate(fileName):
    baseDir = os.path.dirname(os.path.abspath(__name__))
    ips = set()
    accounts = set()
    metaInfo = {}
    with open(os.path.join(baseDir, 'tmp', fileName)) as f:
        logs = json.load(f)
        metaInfo['beginTime'] = logs[0]['time']
        metaInfo['endTime'] = logs[-1]['time']
        metaInfo['ipDetail'] = {}
        metaInfo['accountDetail'] = {}
        for log in logs:
            # 遇到新的IP
            if log['ip'] not in ips:
                ips.add(log['ip'])
                metaInfo['ipDetail'][log['ip']] = [0, 0, 0]
            # 遇到新的account
            if log['account'] not in accounts:
                accounts.add(log['account'])
                metaInfo['accountDetail'][log['account']] = [0, 0, 0]
            # 判断此次访问的结果
            if log['status']['code'] == 0:
                metaInfo['ipDetail'][log['ip']][0] += 1
                metaInfo['accountDetail'][log['account']][0] += 1
            elif log['status']['code'] == 1:
                metaInfo['ipDetail'][log['ip']][0] += 1
                metaInfo['accountDetail'][log['account']][1] += 1
            elif log['status']['code'] == 2:
                metaInfo['ipDetail'][log['ip']][0] += 1
                metaInfo['accountDetail'][log['account']][2] += 1
            elif log['status']['code'] == 3:
                metaInfo['ipDetail'][log['ip']][1] += 1
            else:
                metaInfo['ipDetail'][log['ip']][2] += 1

        metaInfo['ipNum'] = len(ips)
        metaInfo['accountNum'] = len(accounts)
        metaInfo['filename'] = fileName

    print(ips)
    with open(os.path.join(baseDir, 'tmp', 'meta', fileName.split(".")[0] + "_detail.json"), 'w') as f:
        json.dump(metaInfo, f)
