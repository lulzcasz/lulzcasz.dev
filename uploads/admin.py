from django.contrib import admin
from uploads.models import Image, Video
from django.utils.html import format_html


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'kind', 'source', 'processed']
    list_filter = ('post', 'kind', 'processed')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['post', 'source', 'processed']
    list_filter = ('post', 'processed')
