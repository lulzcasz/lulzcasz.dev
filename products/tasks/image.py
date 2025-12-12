from celery import shared_task
from django.core.files.storage import default_storage
import tempfile
import subprocess
import os
from django.core.files.base import ContentFile

@shared_task(bind=True)
def process_image(self, image_name):
    image_url = default_storage.url(image_name)

    root, _ = os.path.splitext(image_name)
    new_image_name = f"{root}-small.avif"

    with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:
        subprocess.run([
            'ffmpeg',
            '-y',
            '-i',
            image_url,
            '-vf',
            'scale=300:300',
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

            default_storage.save(new_image_name, processed_content)
            
    return new_image_name
