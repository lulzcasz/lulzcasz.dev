from celery import shared_task
from uploads.models import Image
from django.core.files.storage import default_storage
from PIL import Image as PILImage
import tempfile
import subprocess
from django.core.files.base import ContentFile


@shared_task(bind=True)
def process_image(self, image_id):
    image = Image.objects.get(id=image_id)

    with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:
        with image.source.open('rb') as old:
            if image.kind == Image.Kind.POST_COVER:
                subprocess.run([
                    'ffmpeg',
                    '-y',
                    '-i',
                    old.url,
                    '-vf',
                    "scale=1024:576",
                    '-pix_fmt',
                    'yuva420p',
                    '-c:v',
                    'libaom-av1',
                    '-still-picture',
                    '1',
                    '-crf',
                    '15',
                    temp_output.name,
                ])

            else:
                with PILImage.open(old) as img:
                    if getattr(img, 'is_animated', False):
                        subprocess.run([
                            'ffmpeg',
                            '-y',
                            '-i',
                            old.url,
                            '-c:v',
                            'libsvtav1',
                            '-crf',
                            '38',
                            '-r',
                            '15',
                            '-preset',
                            '2',
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
                            "scale='min(1024,iw)':'min(576,ih)':force_original_aspect_ratio=decrease, scale='min(1024,iw)':'min(576,ih)', scale='trunc(iw/2)*2':'trunc(ih/2)*2'",
                            '-pix_fmt',
                            'yuva420p',
                            '-c:v',
                            'libaom-av1',
                            '-still-picture',
                            '1',
                            '-crf',
                            '15',
                            temp_output.name,
                        ])

            with open(temp_output.name, 'rb') as f:
                processed_content = ContentFile(f.read())

                image.processed.save(temp_output.name, processed_content, save=False)
    
    Image.objects.filter(id=image_id).update(processed=image.processed.name)


@shared_task(bind=True)
def delete_image(self, source, processed):
    default_storage.delete(source)
    default_storage.delete(processed)
