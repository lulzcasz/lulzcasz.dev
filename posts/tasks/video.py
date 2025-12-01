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

    input_url = video.source.url
    temp_output_path = None

    base_name, _ = os.path.splitext(video.source.name)
    new_s3_key = f"{base_name}.webm"

    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_output:
        temp_output_path = temp_output.name

        cmd = [
            'ffmpeg',
            '-i', input_url,
            '-vf', 'scale=1024:576:force_original_aspect_ratio=decrease',
            '-c:v', 'libvpx-vp9',
            '-crf', '32',
            '-b:v', '0',
            '-c:a', 'libopus',
            '-b:a', '64k',
            '-y',
            temp_output_path
        ]

        subprocess.run(cmd)

        with open(temp_output_path, 'rb') as f:
            processed_content = ContentFile(f.read())

            video.processed.save(new_s3_key, processed_content, save=False)
        
        Video.objects.filter(id=video_id).update(processed=video.processed.name)

        os.remove(temp_output_path)

    return {
        'status': 'success',
        'video_id': video_id,
        'new_path': video.processed.name,
        'message': f'Video {video_id} processed successfully to VP9 format.'
    }

@shared_task(bind=True)
def delete_video(self, source, processed):
    default_storage.delete(source)
    default_storage.delete(processed)
