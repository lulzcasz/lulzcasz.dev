from django.urls import path
from blog.views import index, post_list, post_detail, posts_by_section, posts_by_category

urlpatterns = [
    path('', index, name="index"),
    path('posts/', post_list, name="post-list"),
    path('posts/<slug:post_slug>/', post_detail, name="post-detail"),
    path('secoes/<slug:section_slug>/', posts_by_section, name="posts-by-section"),
    path('categorias/<path:category_full_path>/', posts_by_category, name="posts-by-category"),
]
