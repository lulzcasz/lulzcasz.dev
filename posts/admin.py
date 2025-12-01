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
    base_model = Post
    show_in_index = False
    
    def has_module_permission(self, request):
        return False

    search_fields = ['title', 'description']
    list_display = ['title', 'status', 'created_at']
    
    prepopulated_fields = {"slug": ("title",)}
    
    readonly_fields = ['uuid', 'created_at', 'updated_at']

    filter_horizontal = ('categories',)

@admin.register(Tutorial)
class TutorialAdmin(PostChildAdmin):
    base_model = Tutorial

    filter_horizontal = PostChildAdmin.filter_horizontal + ('prerequisites',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'cover', 'description')
        }),
        ('Conteúdo', {
            'fields': ('content', 'video', 'categories', 'prerequisites')
        }),
        ('Meta', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Article)
class ArticleAdmin(PostChildAdmin):
    base_model = Article
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'cover', 'description')
        }),
        ('Atributos do Artigo', {
            'fields': ('is_review', 'is_opinion')
        }),
        ('Conteúdo', {
            'fields': ('content', 'video', 'categories')
        }),
        ('Meta', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(News)
class NewsAdmin(PostChildAdmin):
    base_model = News
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'cover', 'description')
        }),
        ('Atributos de Notícia', {
            'fields': ('is_breaking',)
        }),
        ('Conteúdo', {
            'fields': ('content', 'video', 'categories')
        }),
        ('Meta', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Post)
class PostParentAdmin(PolymorphicParentModelAdmin):
    base_model = Post
    child_models = (Tutorial, Article, News)
    
    list_display = ['title', 'status', 'polymorphic_ctype', 'created_at']
    
    list_filter = (PolymorphicChildModelFilter, 'status', 'created_at')
    
    search_fields = ['title', 'description']
