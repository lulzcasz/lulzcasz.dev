from django.db.models import (
    Model,
    TextChoices,
    CharField,
    ForeignKey,
    SET_NULL,
    URLField,
    SlugField,
    DateTimeField,
    UUIDField,
    ManyToManyField,
)
from django.utils.text import slugify
from tinymce.models import HTMLField
from uuid import uuid4
from django.urls import reverse
from treebeard.mp_tree import MP_Node
from django.db import transaction


class Category(Model):
    name = CharField('nome', unique=True, max_length=32)
    slug = SlugField(unique=True, max_length=32, blank=True)
    created_at = DateTimeField("criado em", auto_now_add=True)
    updated_at = DateTimeField("atualizado em", auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Categoria"


class Tag(MP_Node):
    name = CharField('nome', max_length=32)
    slug = SlugField(max_length=32, blank=True)
    created_at = DateTimeField("criado em", auto_now_add=True)
    updated_at = DateTimeField("atualizado em", auto_now=True)
    full_path = CharField("caminho completo", max_length=128, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        ancestor_slugs = list(
            self.get_ancestors().values_list('slug', flat=True)
        )
  
        ancestor_slugs.append(self.slug)

        new_full_path = "/".join(ancestor_slugs)

        self.full_path = new_full_path

        with transaction.atomic():
            super().save(*args, **kwargs)

            descendants = self.get_descendants()
                
            for descendant in descendants:
                descendant.save()

    def __str__(self):
        return self.name


class Post(Model):
    class Status(TextChoices):
        DRAFT = 'rascunho', 'Rascunho'
        PUBLISHED = 'publicado', 'Publicado'
        
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    title = CharField("título", max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField("descrição", max_length=160, blank=True)
    cover = URLField("capa", blank=True)
    content = HTMLField("conteúdo", blank=True)
    created_at = DateTimeField("criado em", auto_now_add=True)
    updated_at = DateTimeField("atualizado em", auto_now=True)
    status = CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    category = ForeignKey(
        Category,
        SET_NULL,
        verbose_name="categoria",
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = ManyToManyField(
        Tag, verbose_name="tags", related_name='posts', blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_slug': self.slug})
