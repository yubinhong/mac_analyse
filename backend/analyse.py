#!/usr/bin/env python
# coding:utf-8
# __author__="ybh"
import time
import json
import requests
import sys

# 起始时间
start_datetime = '2018-03-01'
# 结束时间
stop_datetime = '2018-03-31'
#elasticsearch 服务器
host='192.168.100.3'
#ela 端口
port=9200
#elasticsearch  索引名称
index='u12'
data={}
data['new']={}
data['act']={}
result="/root/analyse.txt"
ela_api="http://%s:%s/%s/_doc/_search?pretty" % (host,port,index)
############################
def datetimetotimestamp(datetime):
    timestamp = int(time.mktime(time.strptime(datetime, '%Y-%m-%d')))
    return timestamp


def timestamptodatetime(timestamp):
    datetime = time.strftime('%Y-%m-%d', time.localtime(timestamp))
    return datetime


def get_timelen():
    start_time = datetimetotimestamp(start_datetime)
    stop_time = datetimetotimestamp(stop_datetime)
    days = int((stop_time - start_time) / 60 / 60 / 24) + 1
    return days


def get_data_by_ela(is_new,start_time,stop_time):
    headers={'Content-Type':'application/json'}
    pay_load={
        "_source": {
            "include": [
                "mac"
            ]
        },
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "is_new": is_new
                    }
                },
                "filter": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": start_time,
                                "lt": stop_time
                            }
                        }
                    }
                ]
            }
        },
        "size": 1000000
    }
    req=requests.get(ela_api, headers=headers, data=json.dumps(pay_load))
    result_list = [x['_source']['mac'] for x in req.json()['hits']['hits']]
    return result_list


def get_data():
    start_time = datetimetotimestamp(start_datetime)
    days = get_timelen()
    for i in range(days):
        start_t = start_time + i * 60 * 60 * 24
        stop_t = start_time + (i + 1) * 60 * 60 * 24
        datetime = timestamptodatetime(start_t)
        new_list = list(set(get_data_by_ela(1, start_t, stop_t)))
        data['new'][datetime] = new_list
        act_list = list(set(get_data_by_ela(0, start_t, stop_t)))
        data['act'][datetime] = act_list


def ana_file():
    message=''
    start_time = datetimetotimestamp(start_datetime)
    days = get_timelen()
    for i in range(days):
        try:
            datetime = start_time + i * 60 * 60 * 24
            date = time.strftime("%Y-%m-%d", time.localtime(datetime))
            new_dic = {}
            for new_mac in data['new'][date]:
                new_dic[new_mac] = 1
            data['new'][date] = new_dic
            message +="%s 新增：%s  " % (date, len(data['new'][date]))
            #print("%s 新增：%s" % (date, len(data['new'][date])), end="  ")
            for x in range(i + 1, days):
                count = 0
                act_datetime = start_time + x * 60 * 60 * 24
                act_date = time.strftime("%Y-%m-%d", time.localtime(act_datetime))
                for mac in data['act'][act_date]:
                    if mac in new_dic:
                        count += 1
                message += "%s 留存: %s  " % (act_date, count)
                #print("%s 留存: %s" % (act_date, count), end="  ")
            message += '\n'
        except Exception as e:
            print(e)
            break
    return message


def ana_file_by_week():
    message=''
    start_time = datetimetotimestamp(start_datetime)
    stop_time = datetimetotimestamp(stop_datetime) + 60*60*24 - 1
    days = get_timelen()
    for i in range(days):
        sta_time = start_time+i*60*60*24
        end_time = sta_time+7*60*60*24-1
        if end_time > stop_time:
            break
        sta_datetime = timestamptodatetime(sta_time)
        message +="%s 新增：%s  " % (sta_datetime, len(data['new'][sta_datetime]))
        #print("%s 新增：%s" % (sta_datetime, len(data['new'][sta_datetime])), end="  ")
        act_list = []
        for i in range(1,7):
            step_time = sta_time + i*60*60*24
            step_datetime = timestamptodatetime(step_time)
            act_list += data['act'][step_datetime]
        act_list = list(set(act_list))
        count = 0
        for act_mac in act_list:
            if act_mac in data['new'][sta_datetime]:
                count += 1
        message += "周留存: %s \n" % count
        #print("周留存: %s" % count)
    return message

def ana_file_by_month():
    message=''
    start_time = datetimetotimestamp(start_datetime)
    stop_time=datetimetotimestamp(stop_datetime) + 60*60*24 - 1
    days = get_timelen()
    for i in range(days):
        sta_time=start_time+i*60*60*24
        end_time=sta_time+30*60*60*24-1
        if end_time > stop_time:
            break
        sta_datetime=timestamptodatetime(sta_time)
        message += "%s 新增：%s  " % (sta_datetime, len(data['new'][sta_datetime]))
        print("%s 新增：%s" % (sta_datetime, len(data['new'][sta_datetime])), end="  ")
        act_list=[]
        for i in range(1,30):
            step_time=sta_time+i*60*60*24
            step_datetime=timestamptodatetime(step_time)
            act_list+=data['act'][step_datetime]
        act_list=list(set(act_list))
        count = 0
        for act_mac in act_list:
            if act_mac in data['new'][sta_datetime]:
                count+=1
        message += "月留存: %s \n" % count
        #print("月留存: %s" % count)
    return message


def analyse(start_time, stop_time, idx):
    result = ''
    global start_datetime, stop_datetime, index
    start_datetime = start_time
    stop_datetime = stop_time
    index = idx
    get_data()
    result += ana_file()
    result += ana_file_by_week()
    result += ana_file_by_month()
    return result


if __name__ == '__main__':
    get_data()
    ana_file()
    ana_file_by_week()
    ana_file_by_month()
