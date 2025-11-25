from django.shortcuts import render, get_object_or_404
from posts.models import Category, Post
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)[:3]

    ctx = {
        'posts': posts,
    }

    return render(request, 'blog/index.html', ctx)


def post_list(request):
    all_posts = Post.objects.filter(status=Post.Status.PUBLISHED)

    paginator = Paginator(all_posts, 4)

    page_number = request.GET.get('pagina')

    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail(request, post_slug):
    return render(
        request,
        'blog/post_detail.html',
        {'post': get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)}
    )


def posts_by_section(request, section_slug):
    return render(request, 'blog/posts_by_section.html', {'posts': 'Post.objects.all(section_slug = section_slug)'})


def posts_by_category(request, category_full_path):
    posts = Category.objects.get(full_path=category_full_path).posts

    return render(request, 'blog/posts_by_category.html', {'posts': posts})
