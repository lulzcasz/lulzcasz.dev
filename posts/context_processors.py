from posts.models import Section, Category


def sections(request):
    return {
        'sections': Section.objects.all(),
    }


def categories(request):
    return {
        'categories': Category.dump_bulk(),
    }
