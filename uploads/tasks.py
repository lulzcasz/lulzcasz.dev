from celery import shared_task
import logging
from django.core.files.storage import default_storage
from django.core.files.base import File
import tempfile
import os
import subprocess

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_video(self, video_name):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            input_path = os.path.join(temp_dir, os.path.basename(video_name))
            
            output_video_name_s3 = video_name.replace("raw.mp4", "processed.webm")
            
            output_path_local = os.path.join(temp_dir, os.path.basename(output_video_name_s3))

            logger.info(f"Downloading {video_name} from S3 to {input_path}")
            with default_storage.open(video_name, 'rb') as s3_file:
                with open(input_path, 'wb') as local_file:
                    local_file.write(s3_file.read())

            logger.info(f"Successfully downloaded file.")

            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libvpx-vp9',
                '-crf', '30',
                '-b:v', '0',
                '-c:a', 'libopus',
                '-b:a', '128k',
                output_path_local
            ]

            logger.info(f"Starting ffmpeg processing for: {input_path}")
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            logger.info(f"ffmpeg STDOUT: {result.stdout}")

            logger.info(f"Uploading processed file to S3: {output_video_name_s3}")
            with open(output_path_local, 'rb') as processed_file:
                default_storage.save(output_video_name_s3, File(processed_file))

            logger.info(f"Successfully processed and uploaded: {output_video_name_s3}")

            return output_video_name_s3

        except subprocess.CalledProcessError as e:
            logger.error(f"ffmpeg processing failed for {video_name}.")
            logger.error(f"ffmpeg STDERR: {e.stderr}")
            raise self.retry(exc=e, countdown=300)
            
        except Exception as e:
            logger.error(f"An error occurred processing {video_name}: {e}")
            raise self.retry(exc=e, countdown=300)
