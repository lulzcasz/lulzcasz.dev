from django.urls import path, re_path
from blog.views import index, posts, post_detail, posts_by_type, posts_by_tag

urlpatterns = [
    path('', index, name="home"),
    re_path(r'^(?P<post_type>articles|artigos|tutorials|tutoriais)/$',
        posts_by_type, 
        name='posts-by-type',
    ),
    path('posts/', posts, name="posts"),
    path('<slug:post_slug>/', post_detail, name='post-detail'),
    path('tags/<slug:tag_slug>/', posts_by_tag, name='posts-by-tag')
]
