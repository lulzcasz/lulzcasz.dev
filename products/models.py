from django.db.models import (
    Model,
    CharField,
    FileField,
    ImageField,
    CASCADE,
    URLField,
    ForeignKey,
    UUIDField,
)
from uuid import uuid4
from products.utils.upload_to import platform_logo_path, product_image_path


class Platform(Model):
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    name = CharField('nome', max_length=50)
    logo = FileField(upload_to=platform_logo_path)
    
    class Meta:
        verbose_name = 'plataforma'

    def __str__(self):
        return self.name


class Product(Model):
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    name = CharField('nome', max_length=64)
    image = ImageField('imagem', upload_to=product_image_path)

    def save(self, *args, **kwargs):
        self._image_changed = False

        if self.image:
            if self.pk:
                if Product.objects.get(pk=self.pk).image != self.image:
                    self._image_changed = True
            else:
                self._image_changed = True

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'produto'

    def __str__(self):
        return self.name


class Link(Model): 
    product = ForeignKey(Product, CASCADE, related_name='links', verbose_name='produto')
    platform = ForeignKey(Platform, CASCADE, verbose_name='plataforma')
    url = URLField(max_length=500)

    def __str__(self):
        return f"{self.product.name} on {self.platform.name}"
