from django.contrib import admin
from posts.models import Post, Tutorial, Article, News
from posts.models import Category
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


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
        'status',
        'kind',
        'category_list',
    ]

    list_filter = ('status', 'kind', 'categories')

    def category_list(self, obj):
        return ", ".join(obj.categories.all().values_list('name', flat=True))


admin.site.register(Tutorial, admin.ModelAdmin)
admin.site.register(Article, admin.ModelAdmin)
admin.site.register(News, admin.ModelAdmin)
