from django.contrib import admin
from posts.models import Post
from django.contrib import admin
from posts.models import Section, Category, Post
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


admin.site.register(Section, admin.ModelAdmin)


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = ['name', 'full_path']

    form = movenodeform_factory(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created_at',
        'updated_at',
        'published_at',
        'status',
        'section',
        'category_list',
    ]

    list_filter = ('status', 'section', 'categories')

    def category_list(self, obj):
        return ", ".join(obj.categories.all().values_list('name', flat=True))
    
    category_list.short_description = "lista de categorias"
