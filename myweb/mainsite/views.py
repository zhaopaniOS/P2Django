#!/usr/bin/python
# encoding: utf-8

"""
@auth: 273327600@qq.com
@time: 2018/6/26 11:05
"""

from django.template.loader import get_template
from django.http import HttpResponse
from .models import Post, Camera, Polyv
from datetime import datetime

# Create your views here.
def homepage(request):
    template = get_template('index.html')
    posts = Post.objects.all()
    cameras = Camera.objects.all()
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)

def showpost(request, id):
    template = get_template('post.html')
    try:
        post = Post.objects.get(id=id)
        if post != None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return HttpResponse('/')

def showcamera(request, id):
    template = get_template('camera.html')
    try:
        camera = Camera.objects.get(id=id)
        if camera != None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return HttpResponse('/')

def showpolyv(request, id):
    template = get_template('polyv.html')
    try:
        polyv = Polyv.objects.get(id=id)
        if polyv != None:
            # 获取videoId对应的ts和sign
            ts = ''
            sign = ''
            import requests
            url = 'http://wechat.hanzisiwei.com/haozizai/svideo/getSign?videoId=' + polyv.videoId
            headers = {
                'Host': 'wechat.hanzisiwei.com',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-cn',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E216 MicroMessenger/6.7.0 NetType/WIFI Language/zh_CN',
                'X-Requested-With': 'XMLHttpRequest',
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                t = data.get('t', None)
                if t:
                    ts = t.get('ts', '')
                    sign = t.get('sign', '')
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return HttpResponse('/')