#!/usr/bin/python
# encoding: utf-8

"""
@auth: 273327600@qq.com
@time: 2018/6/26 11:05
"""

from django.template.loader import get_template
from django.http import HttpResponse
from .models import Post, Camera, Polyv, Movie, MovieSeries
from datetime import datetime
import requests
from myweb.settings import STATIC_ROOT

URL_OUTPUT_PATH = 'http://hanzisiwei.qdota.com/static/output/'
URL_MOVIE_PATH = 'http://hanzisiwei.qdota.com/static/movies/'

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
            url = URL_OUTPUT_PATH + polyv.videoId + '.m3u8'
            nextid = polyv.id+1
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
                'Referer': 'http://wechat.hanzisiwei.com/haozizai/index.html'
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                t = data.get('t', None)
                if t:
                    ts = t.get('ts', '')
                    sign = t.get('sign', '')
            else:
                response.write("<p>")
                response.write("res.status_code = " + res.status_code)
                response.write("</p>")
                break

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
                    f = open(os.path.join(STATIC_ROOT, 'output', keyName), 'wb')
                    f.write(keyRes.content)
                    f.close()
                else:
                    response.write("<p>")
                    response.write("keyRes.status_code = " + keyRes.status_code)
                    response.write("</p>")
                    break
                saveM3U8 = m3u8Content.replace(keyUrl, URL_OUTPUT_PATH + keyName)

                response.write("<p>")
                response.write("saveM3U8 = " + saveM3U8)
                response.write("</p>")

                # ts urls
                n = 0
                for segm in m3u8Obj.segments:
                    tsUrl = segm.uri
                    tsName = '%s_%d.ts' % (videoName, n)
                    n+=1
                    saveM3U8 = saveM3U8.replace(tsUrl, URL_OUTPUT_PATH + tsName)
                    # ts save
                    tsRes = requests.get(tsUrl)
                    if tsRes.status_code == 200:
                        response.write("<p>")
                        response.write(tsUrl)
                        response.write("</p>")
                        import os
                        f = open(os.path.join(STATIC_ROOT, 'output', tsName), 'wb')
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
                f = open(os.path.join(STATIC_ROOT, 'output', m3u8Name), 'w')
                f.write(saveM3U8)
                f.close()
                response.write("<p>")
                response.write("Success!")
                response.write("</p>")
    except Exception as exp:
        response.write("<p>")
        response.write("Failed! exp = " + str(exp))
        response.write("</p>")
    response.write("</body>")
    response.write("</html>")
    return response

def movies(request):
    template = get_template('movies.html')
    movies = Movie.objects.all()
    html = template.render(locals())
    return HttpResponse(html)

def movie(request, id):
    template = get_template('video.html')
    try:
        movie = Movie.objects.get(id=id)
        if movie and movie.success:
            url = URL_MOVIE_PATH + str(movie.id) + '.m3u8'
            html = template.render(locals())
            return HttpResponse(html)
    except:
        pass
    return HttpResponse('抱歉，该影片暂时未获得！敬请期待')

def fixM3U8UriWithSegments(str,host):
    changed = False
    import requests
    import m3u8
    m3u8Obj = m3u8.loads(str)
    if m3u8Obj and not m3u8Obj.is_variant:
        for segm in m3u8Obj.segments:
            result = requests.utils.urlparse(segm.uri)
            if len(result.scheme) == 0:
                # 需要补上host
                segm.uri = host + segm.uri
                changed = True

    if changed:
        return m3u8Obj.__unicode__()
    return str

def transMovie(request, id):
    try:
        movie = Movie.objects.get(id=id)
        if movie and not movie.success:
            # 清空已有的Movie片段
            MovieSeries.objects.filter(movie=movie).delete()
            # 将movie关联的子播放列表放到id目录下
            import os
            movie_id_path = os.path.join(STATIC_ROOT, 'movies', str(movie.id))
            if not os.path.exists(movie_id_path):
                os.mkdir(movie_id_path)
            # 源m3u8的host
            movie_uri = requests.utils.urlparse(movie.m3u8)
            movie_host = movie_uri.scheme + "://" + movie_uri.netloc
            # 尝试转换源m3u8
            res = requests.get(movie.m3u8)
            if res.status_code == 200:
                import m3u8
                m3u8Obj = m3u8.loads(res.text)
                if m3u8Obj.is_variant:
                    # 跳转到另外的play lists
                    for playlist in m3u8Obj.playlists:
                        # 跳转的url
                        uri = playlist.uri
                        # 解析url
                        uri_ppp = requests.utils.urlparse(uri)
                        host = ''
                        if len(uri_ppp.scheme) == 0:
                            uri = movie_host + uri
                            host = movie_host
                        else:
                            host = uri_ppp.scheme + "://" + uri_ppp.netloc
                        # 需要加Referer
                        uri_res = requests.get(uri, headers={
                            'Referer': movie.m3u8
                        })
                        if uri_res.status_code == 200:
                            # 得到真实的播放序列，修复相对路径的问题、保存本地
                            uri_body = fixM3U8UriWithSegments(uri_res.text, host)
                            # 将Movie片段写数据库
                            obj = MovieSeries.objects.create(movie=movie,summary='')
                            # 子文件路径
                            m3u8Name = str(obj.id) + ".m3u8"
                            f = open(os.path.join(movie_id_path, m3u8Name), 'w')
                            f.write(uri_body)
                            f.close()

                            # 二级播放列表，保存在movies/movie.id/series.id.m3u8
                            playlist.uri =  URL_MOVIE_PATH + str(movie.id) + '/' + m3u8Name
                    # 一级播放列表，保存在movies下边，以movie id命名
                    f = open(os.path.join(STATIC_ROOT, 'movies', str(movie.id) + '.m3u8'), 'w')
                    f.write(m3u8Obj.__unicode__())
                    f.close()
                    # 更新Movie
                    movie.success = True
                    movie.save()
                    return HttpResponse('二级子播放列表转码成功')

                else:
                    # 一级播放列表，保存在movies下边，以movie id命名
                    body = fixM3U8UriWithSegments(res.text, movie_host)
                    # 保存
                    f = open(os.path.join(STATIC_ROOT, 'movies', str(movie.id) + '.m3u8'), 'w')
                    f.write(body)
                    f.close()
                    # 更新Movie
                    movie.success = True
                    movie.save()
                    return HttpResponse('一级子播放列表转码成功')
    except Exception as e:
        return HttpResponse(str(e))
    return HttpResponse('源路径转码失败')