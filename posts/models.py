from uuid import uuid4
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    SlugField,
    TextChoices,
    URLField,
    UUIDField,
    Count,
    Q,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel
from posts.utils.upload_to import post_image_path
from tinymce.models import HTMLField
from taggit.managers import TaggableManager


class Post(PolymorphicModel):
    class Status(TextChoices):
        DRAFT = "draft", "Rascunho"
        PUBLISHED = "published", "Publicado"

    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    author = ForeignKey(
        "auth.User",
        SET_NULL,
        verbose_name="autor",
        null=True,
        blank=True,
        related_name="posts",
    )
    title = CharField("título", max_length=60, unique=True)
    slug = SlugField(max_length=60, unique=True, blank=True)
    description = CharField("descrição", max_length=160, blank=True)
    cover = ImageField("capa", upload_to=post_image_path, blank=True)
    video = URLField("vídeo", blank=True)
    content = HTMLField("conteúdo", blank=True)
    created_at = DateTimeField("criado em", auto_now_add=True)
    updated_at = DateTimeField("atualizado em", auto_now=True)
    published_at = DateTimeField("publicado em", null=True, editable=False)
    status = CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()
    products = ManyToManyField(
        'products.Product',
        verbose_name="produtos",
        related_name="posts",
        blank=True,
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
        BEGINNER = "beginner", "Iniciante"
        INTERMEDIATE = "intermediate", "Intermediário"
        ADVANCED = "advanced", "Avançado"

    difficulty = CharField("dificuldade", max_length=15, choices=Difficulty.choices)

    class Meta:
        verbose_name_plural = "tutoriais"


class Article(Post):
    is_review = BooleanField("é review", default=False)
    is_opinion = BooleanField("é opinião", default=False)

    class Meta:
        verbose_name = "artigo"


class News(Post):
    is_breaking = BooleanField("é urgente", default=False)

    class Meta:
        verbose_name = "notícia"
