from celery import shared_task
from django.core.files.storage import default_storage
import tempfile
import os
import subprocess
from uploads.models import Video
from django.core.files.base import ContentFile


@shared_task(bind=True)
def process_video(self, video_id):
    video = Video.objects.get(id=video_id)

    input_url = video.video.url
    temp_output_path = None

    base_name, _ = os.path.splitext(video.video.name)
    new_s3_key = f"{base_name}.webm"

    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_output:
        temp_output_path = temp_output.name

        cmd = [
            'ffmpeg',
            '-i', input_url,
            '-vf', 'scale=1024:576:force_original_aspect_ratio=decrease',
            '-c:v', 'libvpx-vp9',
            '-crf', '30',
            '-b:v', '0',
            '-c:a', 'libopus',
            '-b:a', '128k',
            '-r', '30',
            '-y',
            temp_output_path
        ]

        subprocess.run(cmd)

        with open(temp_output_path, 'rb') as f:
            processed_content = ContentFile(f.read())

            video.video.save(new_s3_key, processed_content, save=False)
        
        video.processed = True
        video.save(update_fields=['video', 'processed'])

        os.remove(temp_output_path)

@shared_task(bind=True)
def delete_video(self, video_name):
    default_storage.delete(video_name)
