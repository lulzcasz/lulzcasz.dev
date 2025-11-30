from posts.models import Category


def categories(request):
    return {
        'categories': Category.dump_bulk(),
    }
