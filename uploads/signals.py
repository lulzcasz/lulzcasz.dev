from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from uploads.models import Image, Video
from uploads.tasks.image import process_image, delete_image
from uploads.tasks.video import process_video, delete_video


@receiver(post_save, sender=Image)
def image_post_save(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: process_image.delay(instance.id))


@receiver(post_delete, sender=Image)
def image_post_delete(sender, instance, **kwargs):
    transaction.on_commit(
        lambda: delete_image.delay(instance.source.name, instance.processed.name)
    )


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: process_video.delay(instance.id))


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):   
    transaction.on_commit(
        lambda: delete_video.delay(instance.source.name, instance.processed.name)
    )
