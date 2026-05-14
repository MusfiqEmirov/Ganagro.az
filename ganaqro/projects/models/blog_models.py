from django.db import models
from django.core.validators import MaxLengthValidator


class Blog(models.Model):
    name_az = models.CharField(
        max_length=255,
        verbose_name='Başlıq (AZ)'
    )
    name_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Başlıq (EN)'
    )
    name_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Başlıq (RU)'
    )
    image = models.ImageField(
        upload_to='blog/',
        verbose_name='Şəkil'
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(5000)],
        verbose_name='Məzmun (AZ)'
    )
    description_en = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(5000)],
        verbose_name='Məzmun (EN)'
    )
    description_ru = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(5000)],
        verbose_name='Məzmun (RU)'
    )
    date = models.DateField(
        verbose_name='Tarix'
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Baxış sayı'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloqlar'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.name_az
