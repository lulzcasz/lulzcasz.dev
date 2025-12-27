from uuid import uuid4
from django.db.models import (
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    SlugField,
    TextChoices,
    URLField,
    UUIDField,
    Count,
    Q,
)
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel
from posts.utils.upload_to import post_image_path
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _


class Post(PolymorphicModel):
    class Status(TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    author = ForeignKey(
        "auth.User",
        SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    title = CharField(max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField(max_length=145, blank=True)
    cover = ImageField(upload_to=post_image_path, blank=True)
    content = HTMLField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    published_at = DateTimeField(null=True, editable=False)
    status = CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager(blank=True)

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

    def get_related_posts(self):
        if not self.tags.exists():
            return Post.objects.none()

        return (
            Post.objects.filter(
                status=self.Status.PUBLISHED,
                tags__in=self.tags.all(),
            )
            .exclude(
                pk=self.pk,
            )
            .annotate(
                shared_tag_count=Count(
                    "tags",
                    filter=Q(tags__in=self.tags.all()),
                )
            )
            .order_by("-shared_tag_count")
            [:3]
        )

    def __str__(self):
        return self.title

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    @property
    def verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"post_slug": self.slug})


class Tutorial(Post):
    class Difficulty(TextChoices):
        BEGINNER = "beginner", _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        ADVANCED = "advanced", _("Advanced")

    difficulty = CharField(max_length=15, choices=Difficulty.choices)
    source_code = URLField(blank=True)

    class Meta:
        verbose_name = _('tutorial')
        verbose_name_plural = _('tutorials')


class Article(Post):
    class Genre(TextChoices):
        REVIEW = "review", "Review"
        OPINION = "opinion", _("Opinion")

    genres = ArrayField(
        CharField(max_length=10, choices=Genre.choices), blank=True, default=list,
    )

    def get_genres_labels(self):
        return [self.Genre(genre).label for genre in self.genres]
    
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
