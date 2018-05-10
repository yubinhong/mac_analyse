from django.shortcuts import render,HttpResponse

# Create your views here.
import json
import requests
from backend import analyse


def index(request):
    if request.method=='GET':
        API="http://192.168.100.3:9200/_cat/indices?pretty"
        req=requests.get(API)
        index_list=req.text.strip('\n').split('\n')
        tongji_list=[x.split()[2] for x in index_list]
        return render(request,'index.html',{'tongji_list':tongji_list})
    else:
        start_time=request.POST.get('analyse_at_from')
        stop_time=request.POST.get('analyse_at_to')
        index=request.POST.get('index')
        result=analyse.analyse(start_time,stop_time,index)
        result=result.strip('\n').split('\n')
        return HttpResponse(json.dumps(result))
