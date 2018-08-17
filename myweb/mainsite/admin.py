from django.contrib import admin
from .models import Post, Camera, Polyv, Movie, MovieSeries

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'pub_date')

class CameraAdmin(admin.ModelAdmin):
    list_display = ('title', 'rtmp', 'm3u8')

class PolyvAdmin(admin.ModelAdmin):
    list_display = ('title', 'videoId', 'm3u8')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'image', 'm3u8', 'success')

class MovieSeriesAdmin(admin.ModelAdmin):
    list_display = ('movie', 'id', 'summary')
    raw_id_fields = ('movie',)

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Polyv, PolyvAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieSeries, MovieSeriesAdmin)