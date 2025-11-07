from django.shortcuts import render, get_object_or_404
from posts.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        {"post": get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)},
    )
