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
import requests
from myweb.settings import BASE_DIR

# Create your views here.
def homepage(request):
    template = get_template('index.html')
    posts = Post.objects.all()
    cameras = Camera.objects.all()
    polyvs = Polyv.objects.all()
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

def showvideo(request, id):
    template = get_template('video.html')
    try:
        polyv = Polyv.objects.get(id=id)
        if polyv != None:
            url = 'https://video-dev.github.io/streams/x36xhzz/x36xhzz.m3u8'
            url = 'http://47.96.88.244/static/streams/' + polyv.videoId + '.m3u8'
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return HttpResponse('/')

def generateVideo(request):
    response = HttpResponse()
    response.write("<html>")
    response.write("<body>")
    # generate videos
    polyvs = Polyv.objects.all()
    try:
        for polyv in polyvs:
            response.write("<p>")
            response.write(polyv.title + ' ' + polyv.videoId)
            response.write("</p>")
            # 获取videoId对应的ts和sign
            ts = ''
            sign = ''
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

            response.write("<p>")
            response.write("ts = " + ts + ", sign = " + sign)
            response.write("</p>")

            # m3u8 url
            svideoId = polyv.videoId
            videoName = svideoId.replace('_8', '_2')

            import time
            import random
            t = time.time()
            pid = '%dX%d' % ((int(round(t * 1000))), (int)(random.random() * 1000000 + 1000000))
            m3u8Url = 'http://hls.videocc.net/8b0a2fa267/0/' + videoName + '.m3u8?' + 'pid=' + pid + '&ts='+ ts + '&sign=' + sign

            response.write("<p>")
            response.write("m3u8Url = " + m3u8Url)
            response.write("</p>")

            m3u8XXX = requests.get(m3u8Url)
            if m3u8XXX.status_code == 200:
                m3u8Content = m3u8XXX.text
                response.write("<p>")
                response.write(m3u8Content)
                response.write("</p>")
                # parse m3u8 content
                try:
                    import m3u8
                except ImportError:
                    response.write("<p>")
                    response.write("ImportError")
                    response.write("</p>")
                    break
                response.write("<p>")
                response.write("import m3u8Obj")
                response.write("</p>")

                m3u8Obj = m3u8.loads(m3u8Content)

                response.write("<p>")
                response.write("m3u8.loads")
                response.write("</p>")

                # key url
                keyUrl = m3u8Obj.keys[0].uri

                response.write("<p>")
                response.write("keyUrl")
                response.write("</p>")

                keyName = videoName + '.key'

                response.write("<p>")
                response.write(keyUrl)
                response.write("</p>")

                # key save
                keyRes = requests.get(keyUrl)
                if keyRes.status_code == 200:
                    import os
                    f = open(os.path.join(BASE_DIR, 'static', 'output', keyName), 'wb')
                    f.write(keyRes.content)
                    f.close()
                else:
                    response.write("<p>")
                    response.write("keyRes.status_code = " + keyRes.status_code)
                    response.write("</p>")
                    break
                saveM3U8 = m3u8Content.replace(keyUrl, 'http://47.96.88.244/static/output/' + keyName)

                response.write("<p>")
                response.write("saveM3U8 = " + saveM3U8)
                response.write("</p>")

                # ts urls
                n = 0
                for segm in m3u8Obj.segments:
                    tsUrl = segm.uri
                    tsName = '%s_%d.ts' % (videoName, n)
                    n+=1
                    saveM3U8 = saveM3U8.replace(tsUrl, 'http://47.96.88.244/static/output/' + tsName)
                    # ts save
                    tsRes = requests.get(tsUrl)
                    if tsRes.status_code == 200:
                        response.write("<p>")
                        response.write(tsUrl)
                        response.write("</p>")
                        import os
                        f = open(os.path.join(BASE_DIR, 'static', 'output', tsName), 'wb')
                        f.write(tsRes.content)
                        f.close()
                    else:
                        response.write("<p>")
                        response.write("tsRes.status_code = " + tsRes.status_code)
                        response.write("</p>")
                        break
                # m3u8 save
                m3u8Name = svideoId+'.m3u8'
                import os
                f = open(os.path.join(BASE_DIR, 'static', 'output', m3u8Name), 'w')
                f.write(saveM3U8)
                f.close()
                response.write("<p>")
                response.write("Success!")
                response.write("</p>")
    except:
        response.write("<p>")
        response.write("Failed!")
        response.write("</p>")
    response.write("</body>")
    response.write("</html>")
    return response