from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title

class Camera(models.Model):
    title = models.CharField(max_length=200)
    rtmp = models.CharField(max_length=1024)
    m3u8 = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title

class Polyv(models.Model):
    title = models.CharField(max_length=200)
    videoId = models.CharField(max_length=1024)
    m3u8 = models.CharField(max_length=4096)

    def __unicode__(self):
        return self.title