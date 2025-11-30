from django.contrib.sitemaps import Sitemap
from posts.models import Category, Post


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
