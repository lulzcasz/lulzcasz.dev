from django.urls import path
from blog.views import index, post_list, post_detail

urlpatterns = [
    path('', index, name="index"),
    path('todos-os-posts/', post_list, name="post-list"),
    path('<slug:post_slug>', post_detail, name="post-detail"),
]
