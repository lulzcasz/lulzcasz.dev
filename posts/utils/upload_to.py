from uuid import uuid4

def post_image_path(instance, filename):
    return f'posts/{instance.uuid}/images/{uuid4()}.avif'
