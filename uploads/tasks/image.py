from celery import shared_task
from uploads.models import Image
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image as PILImage


@shared_task(bind=True)
def process_image(self, image_id):
    post_content_image = Image.objects.get(id=image_id)
    print(post_content_image.image.name)

    with post_content_image.image.open('rb') as old:
        new = BytesIO()

        with PILImage.open(old) as img:
            img_rgba = img.convert('RGBA')
            img_rgba.thumbnail((1024, 576), PILImage.Resampling.LANCZOS)
            img_rgba.save(new, "WEBP", quality=85, method=6)

            new.seek(0)

        post_content_image.image.save(post_content_image.image.name, new)

    post_content_image.processed = True
    post_content_image.save()


@shared_task(bind=True)
def delete_image(self, image_name):
    default_storage.delete(image_name)
