from django.contrib import admin
from posts.models import Post, Tutorial, Article, News
from posts.models import Category
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
)


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = ['name', 'full_path']

    form = movenodeform_factory(Category)


class PostChildAdmin(PolymorphicChildModelAdmin):
    change_form_template = 'admin/posts/post/change_form.html'
    base_model = Post
    show_in_index = False
    
    def has_module_permission(self, request):
        return False

    search_fields = ['title', 'description']
    list_display = ['title', 'status', 'created_at', 'updated_at', 'published_at',]
    
    prepopulated_fields = {"slug": ("title",)}
    
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'published_at']

    filter_horizontal = ('categories',)
    

@admin.register(Tutorial)
class TutorialAdmin(PostChildAdmin):
    base_model = Tutorial

    filter_horizontal = PostChildAdmin.filter_horizontal


@admin.register(Article)
class ArticleAdmin(PostChildAdmin):
    base_model = Article


@admin.register(News)
class NewsAdmin(PostChildAdmin):
    base_model = News


@admin.register(Post)
class PostParentAdmin(PolymorphicParentModelAdmin):
    base_model = Post
    child_models = (Tutorial, Article, News)
    
    list_display = ['title', 'status', 'polymorphic_ctype', 'created_at']
    
    list_filter = (PolymorphicChildModelFilter, 'status', 'created_at')
    
    search_fields = ['title', 'description']
