from os.path import splitext
from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.filter
def variant(image_field, size):
    return default_storage.url(f"{splitext(image_field.name)[0]}-{size}.avif")
