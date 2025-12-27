from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from posts.models import Article, Post, Tutorial
from taggit.models import Tag


def index(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-published_at")[
        :3
    ]

    ctx = {
        "posts": posts,
    }

    return render(request, "blog/index.html", ctx)


def posts(request):
    all_posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-published_at"
    )

    paginator = Paginator(all_posts, 4)

    page_number = request.GET.get("pagina")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj, "title": "Todos os Posts"},
    )


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)

    return render(
        request, "blog/post_detail.html", {"post": post},
    )


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__name=tag.name).order_by("-published_at")

    paginator = Paginator(posts, 4)
    page_number = request.GET.get("pagina")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "blog/post_list.html", {"page_obj": page_obj, "title": tag.name}
    )


def posts_by_type(request, post_type):
    model_mapping = {
        "tutorials": Tutorial,
        "tutoriais": Tutorial,
        "articles": Article,
        "artigos": Article,
    }

    model_class = model_mapping.get(post_type)

    all_posts = model_class.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-published_at"
    )

    paginator = Paginator(all_posts, 4)

    page_number = request.GET.get("pagina")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {"page_obj": page_obj, "title": model_class._meta.verbose_name_plural.title()},
    )
