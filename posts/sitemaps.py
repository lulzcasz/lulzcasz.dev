from django.contrib.sitemaps import Sitemap
from posts.models import Category, Post
from django.urls import reverse


class StaticSitemap(Sitemap):
    def items(self):
        return ['blog-index']

    def location(self, item):
        if isinstance(item, tuple):
            url_name, kwargs = item
            return reverse(url_name, kwargs=kwargs)
        else:
            return reverse(item)

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class PostTypeSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['artigos', 'noticias', 'tutoriais']

    def location(self, item):
        return reverse('posts-by-type', args=[item])
