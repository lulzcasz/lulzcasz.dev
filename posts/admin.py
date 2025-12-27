from django import forms
from django.contrib import admin
from posts.models import Post, Tutorial, Article
from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
)
from modeltranslation.admin import TranslationAdmin

class ArticleAdminForm(forms.ModelForm):
    genres = forms.MultipleChoiceField(
        choices=Article.Genre.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Gêneros"
    )

    class Meta:
        model = Article
        fields = '__all__'


class PostChildAdmin(TranslationAdmin, PolymorphicChildModelAdmin):
    change_form_template = 'admin/posts/post/change_form.html'
    base_model = Post
    show_in_index = False
    
    def has_module_permission(self, request):
        return False

    search_fields = ['title', 'description']
    list_display = ['title', 'status', 'created_at', 'updated_at', 'published_at',]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'published_at']
    

@admin.register(Tutorial)
class TutorialAdmin(PostChildAdmin):
    base_model = Tutorial
    filter_horizontal = PostChildAdmin.filter_horizontal 


@admin.register(Article)
class ArticleAdmin(PostChildAdmin):
    base_model = Article
    form = ArticleAdminForm

    filter_horizontal = PostChildAdmin.filter_horizontal

    def get_list_display(self, request):
        return super().get_list_display(request) + ['get_genres_display']

    def get_genres_display(self, obj):
        return ", ".join([dict(Article.Genre.choices).get(g, g) for g in obj.genres])
    get_genres_display.short_description = "Gêneros"


@admin.register(Post)
class PostParentAdmin(PolymorphicParentModelAdmin):
    base_model = Post
    child_models = (Tutorial, Article)
    
    list_display = ['title', 'status', 'polymorphic_ctype', 'created_at']
    list_filter = (PolymorphicChildModelFilter, 'status', 'created_at')
    search_fields = ['title', 'description']
