from celery import shared_task
from uploads.models import Image
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image as PILImage
import tempfile
import subprocess
from django.core.files.base import ContentFile
import os


@shared_task(bind=True)
def process_image(self, image_id):
    image = Image.objects.get(id=image_id)

    with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:
        with image.image.open('rb') as old:
            if image.kind == Image.Kind.POST_COVER:
                subprocess.run(
                    [
                        'ffmpeg',
                        '-y',
                        '-i',
                        old.url,
                        '-vf',
                        "scale=1024:576, scale='trunc(iw/2)*2':'trunc(ih/2)*2'",
                        '-c:v',
                        'libaom-av1',
                        '-still-picture',
                        '1',
                        '-crf',
                        '30',
                        temp_output.name,
                    ]
                )

            else:
                with PILImage.open(old) as img:
                    if img.is_animated:
                        subprocess.run([
                            'ffmpeg',
                            '-y',
                            '-i',
                            old.url,
                            '-c:v',
                            'libsvtav1',
                            '-r',
                            '15',
                            '-vf',
                            "scale='min(1024,iw)':576:force_original_aspect_ratio=decrease",
                            temp_output.name,
                        ])
                    else:
                        subprocess.run([
                            'ffmpeg',
                            '-y',
                            '-i',
                            old.url,
                            '-vf',
                            "scale='min(1024,iw)':'min(576,ih)':force_original_aspect_ratio=increase, scale='min(1024,iw)':'min(576,ih)', scale='trunc(iw/2)*2':'trunc(ih/2)*2'",
                            '-c:v',
                            'libaom-av1',
                            '-still-picture',
                            '1',
                            '-crf',
                            '30',
                            temp_output.name,
                        ])

            with open(temp_output.name, 'rb') as f:
                processed_content = ContentFile(f.read())

                image.image.save(image.image.name, processed_content, save=False)

    image.processed = True
    image.save()


@shared_task(bind=True)
def delete_image(self, image_name):
    default_storage.delete(image_name)
