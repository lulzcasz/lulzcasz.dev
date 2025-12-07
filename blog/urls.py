from django.urls import path, re_path
from blog.views import index, posts, post_detail, posts_by_category, posts_by_type

urlpatterns = [
    path('', index, name="blog-index"),
    re_path(r'^(?P<post_type>artigos|noticias|tutoriais)/$',
        posts_by_type, 
        name='posts-by-type',
    ),
    path('posts/', posts, name="posts"),
    path('<slug:post_slug>/', post_detail, name='post-detail'),
    path(
        'categorias/<path:category_full_path>/',
        posts_by_category,
        name="posts-by-category",
    ),
]
