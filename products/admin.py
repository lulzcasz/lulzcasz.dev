from django.contrib import admin
from products.models import Platform, Product, Link

admin.site.register(Platform, admin.ModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Link, admin.ModelAdmin)
