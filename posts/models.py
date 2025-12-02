from django.db.models import (
    TextChoices,
    CharField,
    URLField,
    SlugField,
    DateTimeField,
    UUIDField,
    ManyToManyField,
    BooleanField,
    ImageField,
    ForeignKey,
    SET_NULL,
)
from django.utils.text import slugify
from tinymce.models import HTMLField
from uuid import uuid4
from django.urls import reverse
from treebeard.mp_tree import MP_Node
from django.db import transaction
from posts.utils.upload_to import post_image_path
from polymorphic.models import PolymorphicModel

from django.utils import timezone


class Category(MP_Node):
    name = CharField('nome', max_length=32)
    slug = SlugField(max_length=32, blank=True)
    created_at = DateTimeField('criada em', auto_now_add=True)
    updated_at = DateTimeField('atualizada em', auto_now=True)
    full_path = CharField('caminho completo', max_length=128, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        ancestor_slugs = list(self.get_ancestors().values_list('slug', flat=True))
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
    
    class Meta:
        verbose_name = 'categoria'

    def get_absolute_url(self):
        return reverse(
            'posts-by-category', kwargs={'category_full_path': self.full_path}
        )


class Post(PolymorphicModel):
    class Status(TextChoices):
        DRAFT = 'draft', 'Rascunho'
        PUBLISHED = 'published', 'Publicado'
        
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    author = ForeignKey(
        'auth.User', SET_NULL, verbose_name='autor', null=True, blank=True
    )
    title = CharField('título', max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField('descrição', max_length=160, blank=True)
    cover = ImageField('capa', upload_to=post_image_path, blank=True)
    video = URLField('vídeo', blank=True)
    content = HTMLField('conteúdo', blank=True)
    created_at = DateTimeField('criado em', auto_now_add=True)
    updated_at = DateTimeField('atualizado em', auto_now=True)
    published_at = DateTimeField('publicado em', null=True, editable=False)
    status = CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    categories = ManyToManyField(
        Category, verbose_name='categorias', related_name='posts', blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        self._cover_changed = False

        if self.cover:
            if self.pk:
                if Post.objects.get(pk=self.pk).cover != self.cover:
                    self._cover_changed = True
            else:
                self._cover_changed = True

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'post-detail', kwargs={'post_slug': self.slug}
        )


class Tutorial(Post):
    prerequisites = ManyToManyField(
        'self', verbose_name='pré-requisitos', blank=True, symmetrical=False
    )

    class Meta:
        verbose_name_plural = 'tutoriais'


class Article(Post):
    is_review = BooleanField('é review', default=False)
    is_opinion = BooleanField('é opinião', default=False)

    class Meta:
        verbose_name = 'artigo'


class News(Post):
    is_breaking = BooleanField('é urgente', default=False)

    class Meta:
        verbose_name = 'notícia'
