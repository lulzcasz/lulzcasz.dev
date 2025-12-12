from os.path import splitext
from uuid import uuid4

def platform_logo_path(instance, filename):
    return f'platforms/{instance.uuid}{splitext(filename)[1]}'

def product_image_path(instance, filename):
    return f'products/{instance.uuid}/{uuid4()}{splitext(filename)[1]}'
