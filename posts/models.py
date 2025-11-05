from django.db.models import (
    Model,
    TextChoices,
    CharField,
    ForeignKey,
    CASCADE,
    URLField,
    SlugField,
    DateTimeField,
)
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Post(Model):
    class Status(TextChoices):
        DRAFT = 'rascunho', 'Rascunho'
        PUBLISHED = 'publicado', 'Publicado'

    title = CharField("título", max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField("descrição", max_length=160)
    author = ForeignKey(User, CASCADE, related_name='posts', verbose_name="autor")
    cover = URLField("capa")
    content = HTMLField("conteúdo")
    created_at = DateTimeField("criado em", auto_now_add=True)
    updated_at = DateTimeField("atualizado em", auto_now=True)
    status = CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
