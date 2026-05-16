from django.db import models
from django.core.validators import MaxLengthValidator

from projects.utils import SluggedModel


class ProductCategory(SluggedModel):
    name_az = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (AZ)'
    )
    name_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (EN)'
    )
    name_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (RU)'
    )

    class Meta:
        verbose_name = 'Kateqoriya adı'
        verbose_name_plural = 'Kateqoriya adları'
    
    def get_slug_source(self) -> str:
        return self.name_az

    def __str__(self):
        return self.name_az or 'Kateqoriya'


class Product(SluggedModel):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Kateqoriya'
    )
    name_az = models.CharField(
        max_length=250,
        verbose_name='Məhsul adı (AZ)'
    )
    name_en = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Məhsul adı (EN)'
    )
    name_ru = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Məhsul adı (RU)'
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(500)],
        verbose_name='Məhsul haqqında (AZ)'
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(500)],
        null=True,
        blank=True,
        verbose_name='Məhsul haqqında (EN)'
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(500)],
        null=True,
        blank=True,
        verbose_name='Məhsul haqqında (RU)'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Məhsul aktivliyi'
    )
    on_main_page = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Ana səhifədə olsun'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def get_slug_source(self) -> str:
        return self.name_az

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'
        ordering  = ['-created_at']

    def __str__(self):
        return self.name_az
