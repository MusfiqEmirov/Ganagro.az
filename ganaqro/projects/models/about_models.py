from django.db import models
from django.core.validators import MaxLengthValidator


class About(models.Model):
    main_title_az = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Əsas başlıq (AZ)'
    )
    main_title_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Əsas başlıq (EN)'
    )
    main_title_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Əsas başlıq (RU)'
    )
    second_title_az = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name='Alt başlıq (AZ)'
    )
    second_title_en = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name='Alt başlıq (EN)'
    )
    second_title_ru = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name='Alt başlıq (RU)'
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(4000)],
        verbose_name='Text (AZ)'
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(4000)],
        verbose_name='Text (EN)'
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(4000)],
        verbose_name='Text (RU)'
    )

    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'

    def __str__(self):
        return self.main_title_az or 'Haqqımızda'
