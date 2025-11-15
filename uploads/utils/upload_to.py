from os.path import splitext


def post_image_source_path(instance, filename):
    return f'posts/{instance.post.uuid}/images/{instance.uuid}/source{splitext(filename)[1]}'


def post_image_processed_path(instance, filename):
    return f'posts/{instance.post.uuid}/images/{instance.uuid}/processed{splitext(filename)[1]}'


def post_video_source_path(instance, filename):
    return f'posts/{instance.post.uuid}/videos/{instance.uuid}/source{splitext(filename)[1]}'


def post_video_processed_path(instance, filename):
    return f'posts/{instance.post.uuid}/videos/{instance.uuid}/processed{splitext(filename)[1]}'
