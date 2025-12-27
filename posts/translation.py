from modeltranslation.translator import register, TranslationOptions
from posts.models import Post, Tutorial, Article


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description', 'content')


@register(Tutorial)
class TutorialTranslationOptions(TranslationOptions):
    fields = ()


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ()
