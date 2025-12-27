from .models import Tutorial, Article

def navbar_post_types(request):
    return {
        'tutorial_name_plural': Tutorial._meta.verbose_name_plural,
        'article_name_plural': Article._meta.verbose_name_plural,
    }
