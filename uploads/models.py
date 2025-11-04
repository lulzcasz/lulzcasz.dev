from django.db.models import Model, FileField, UUIDField
from uuid import uuid4
from os.path import join


def get_video_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()

    return join(f'videos/{instance.uuid}', f'raw.{ext}')


class Video(Model):
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    video = FileField(upload_to=get_video_upload_path)

    def __str__(self):
        return str(self.uuid)
    
    def get_processed_video_url(self):
        return self.video.url.replace("raw.mp4", "processed.webm")
