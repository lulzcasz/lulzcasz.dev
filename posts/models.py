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
from django.utils import timezone


class Section(Model):
    name = CharField(unique=True, max_length=32)
    slug = SlugField(unique=True, max_length=32, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts-by-section', kwargs={'section_slug': self.slug})


class Category(MP_Node):
    name = CharField(max_length=32)
    slug = SlugField(max_length=32, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    full_path = CharField(max_length=128, unique=True, blank=True)

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
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse(
            'posts-by-category', kwargs={'category_full_path': self.full_path}
        )


class Post(MP_Node):
    class Status(TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'
        
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    title = CharField(max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField(max_length=160, blank=True)
    cover = URLField(blank=True)
    content = HTMLField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    published_at = DateTimeField(null=True, editable=False)
    status = CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    section = ForeignKey(Section, SET_NULL, null=True, blank=True, related_name='posts')
    categories = ManyToManyField(Category, related_name='posts', blank=True)
    related = ManyToManyField('self', blank=True, symmetrical=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_slug': self.slug})
