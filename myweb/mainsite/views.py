from django.template.loader import get_template
from django.http import HttpResponse
from .models import Post, Camera
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