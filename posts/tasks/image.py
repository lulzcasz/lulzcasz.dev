from celery import shared_task
from django.core.files.storage import default_storage
import tempfile
import subprocess
import os
from django.core.files.base import ContentFile
from PIL import Image

@shared_task(bind=True)
def process_image(self, image_name, kind):
    image_url = default_storage.url(image_name)
    
    name_base, _ = os.path.splitext(image_name)

    if kind == 'cover':
        versions = {
            'small': (400, 210, 4),
            'medium': (600, 315, 6),
            'large': (1200, 630, 12),
        }

        for suffix, (width, height, crf) in versions.items():
            new_filename = f"{name_base}-{suffix}.avif"

            with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:
                subprocess.run([
                    'ffmpeg',
                    '-y',
                    '-i',
                    image_url,
                    '-vf',
                    f"scale='if(lt(iw/ih,{width}/{height}),{width},-2)':'if(lt(iw/ih,{width}/{height}),-2,{height})',crop={width}:{height}",
                    '-pix_fmt',
                    'yuva420p',
                    '-c:v', 
                    'libaom-av1',
                    '-still-picture',
                    '1',
                    '-crf',
                    str(crf),
                    temp_output.name,
                ], check=True)

                with open(temp_output.name, 'rb') as f:
                    processed_content = ContentFile(f.read())
                    if default_storage.exists(new_filename):
                        default_storage.delete(new_filename)
                    default_storage.save(new_filename, processed_content)

    elif kind == 'content_image':
        with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:
            with default_storage.open(image_name, 'rb') as old:
                with Image.open(old) as img:
                    if getattr(img, 'is_animated', False):
                        subprocess.run([
                            'ffmpeg',
                            '-y',
                            '-i',
                            image_url,
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
                        ], check=True)
                        
                    else:
                        subprocess.run([
                            'ffmpeg',
                            '-y',
                            '-i',
                            image_url,
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
                        ], check=True)

            with open(temp_output.name, 'rb') as f:
                processed_content = ContentFile(f.read())
                default_storage.delete(image_name)
                default_storage.save(image_name, processed_content)
