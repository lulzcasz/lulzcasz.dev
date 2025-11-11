from django.contrib import admin
from posts.models import Post
from django.contrib import admin
from posts.models import Category, Tag, Post
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


admin.site.register(Category, admin.ModelAdmin)


@admin.register(Tag)
class TopicAdmin(TreeAdmin):
    list_display = ['name', 'full_path']

    form = movenodeform_factory(Tag)


admin.site.register(Post, admin.ModelAdmin)
