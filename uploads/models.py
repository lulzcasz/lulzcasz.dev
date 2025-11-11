from django.db.models import (
    Model,
    FileField,
    UUIDField,
    ForeignKey,
    CASCADE,
    DateTimeField,
    SET_NULL,
    BooleanField,
    TextChoices,
    CharField,
    ImageField,
)
from uuid import uuid4
from django.contrib.auth.models import User
from os.path import join


class AbstractMedia(Model):
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    post = ForeignKey('posts.Post', CASCADE)
    uploaded_at = DateTimeField(auto_now_add=True)
    processed = BooleanField("processado")

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.uuid)


def upload_post_image_to_path(instance, filename):
    return join(f'posts/{instance.post.uuid}/images', f'{instance.uuid}.avif')


class Image(AbstractMedia):
    class Kind(TextChoices):
        POST_COVER = 'post_cover', 'Capa do Post'
        POST_CONTENT_IMAGE = 'post_content_image', 'Imagem do Conteúdo do Post'

    image = ImageField("imagem", upload_to=upload_post_image_to_path)
    post = ForeignKey('posts.Post', CASCADE, related_name='cover_images')
    kind = CharField("tipo", max_length=20, choices=Kind.choices)
    

    class Meta:
        verbose_name = "imagem"
        verbose_name_plural = "imagens"


def upload_post_video_to_path(instance, filename):
    return join(f'posts/{instance.post.uuid}/videos', f'{instance.uuid}.webm')


class Video(AbstractMedia):
    video = FileField(upload_to=upload_post_video_to_path)
    post = ForeignKey('posts.Post', CASCADE, related_name='content_videos')

    class Meta:
        verbose_name = "Vídeo"
