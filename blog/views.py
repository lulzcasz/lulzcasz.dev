from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from posts.models import Article, Category, News, Post, Tutorial


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

    selected_cats = post.categories.all()
    paths = set()
    step = Category.steplen

    for cat in selected_cats:
        current_path = cat.path
        for i in range(step, len(current_path) + 1, step):
            paths.add(current_path[:i])

    all_cats_queryset = Category.objects.filter(path__in=paths)

    meta_keywords = ", ".join(all_cats_queryset.values_list("name", flat=True))

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "all_cats": all_cats_queryset, "meta_keywords": meta_keywords},
    )


def posts_by_category(request, category_full_path):
    category = get_object_or_404(Category, full_path=category_full_path)

    all_posts = category.posts.all().order_by("-published_at")

    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get("pagina")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "blog/post_list.html", {"page_obj": page_obj, "title": category.name}
    )


def posts_by_type(request, post_type):
    model_mapping = {
        "tutoriais": Tutorial,
        "artigos": Article,
        "noticias": News,
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
