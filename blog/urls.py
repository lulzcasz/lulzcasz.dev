from django.urls import path
from blog.views import index, post_list, post_detail, posts_by_category, posts_by_tag

urlpatterns = [
    path('', index, name="index"),
    path('posts/', post_list, name="post-list"),
    path('posts/<slug:post_slug>', post_detail, name="post-detail"),
    path('categorias/<slug:category_slug>', posts_by_category, name="posts-by-category"),
    path('tags/<path:tag_full_path>', posts_by_tag, name="posts-by-tag"),
]
