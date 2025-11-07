from django.contrib import admin
from uploads.models import Image, Video


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'processed']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'processed']
