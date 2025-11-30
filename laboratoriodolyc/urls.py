from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import CategorySitemap, PostSitemap


sitemaps_dict = {
    'categories': CategorySitemap, 'posts': PostSitemap,
}


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    )),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps_dict},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
