from celery import shared_task
from django.core.files.storage import default_storage
import tempfile
import subprocess
from django.core.files.base import ContentFile
from PIL import Image


@shared_task(bind=True)
def process_image(self, image_name, kind):
    image_url = default_storage.url(image_name)

    with tempfile.NamedTemporaryFile(suffix='.avif', delete=True) as temp_output:

        if kind == 'cover':
            subprocess.run([
                'ffmpeg',
                '-y',
                '-i',
                image_url,
                '-vf',
                "scale='if(lt(iw/ih,1200/630),1200,-2)':'if(lt(iw/ih,1200/628),-2,630)',crop=1200:630",
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

        elif kind == 'content_image':
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
                        ])
                        
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
                        ])

        with open(temp_output.name, 'rb') as f:
            processed_content = ContentFile(f.read())

            default_storage.save(image_name, processed_content)
