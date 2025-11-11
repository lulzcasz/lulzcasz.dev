from django.shortcuts import render, get_object_or_404
from posts.models import Post, Tag
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


from logging import getLogger
logger = getLogger(__name__)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)

    tags = [] 
    created_nodes = {} 

    for tag in post.tags.all(): 
        tag_hierarchy = list(tag.get_ancestors()) + [tag] 

        current_parent_list = tags

        for t in tag_hierarchy:
            unique_key = t.full_path 

            if unique_key in created_nodes:
                node = created_nodes[unique_key]
                
            else:
                node = {
                    'name': t.name,
                    'full_path': t.full_path,
                    'children': []
                }

                created_nodes[unique_key] = node
                
                current_parent_list.append(node)

            current_parent_list = node['children']

    ctx = {
        'post': post,
        'tags': tags,
    }

    return render(request, 'blog/post_detail.html', ctx)


def posts_by_category(request, category_slug):
    return render(request, 'blog/posts_by_category.html', {'posts': 'Post.objects.all(category_slug = category_slug)'})


def posts_by_tag(request, tag_full_path):
    from logging import getLogger
    logger = getLogger(__name__)

    logger.warning(tag_full_path)

    posts = Tag.objects.get(full_path=tag_full_path).posts

    return render(request, 'blog/posts_by_tag.html', {'posts': posts})
