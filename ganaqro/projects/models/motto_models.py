from django.db import models
from django.core.validators import MaxLengthValidator


class Motto(models.Model):
    text_az = models.TextField(
        validators=[MaxLengthValidator(220)],
        verbose_name='Deviz cümləsi(AZ)'
    )
    text_en = models.TextField(
        validators=[MaxLengthValidator(220)],
        null=True,
        blank=True,
        verbose_name='Deviz cümləsi(EN)'
    )
    text_ru = models.TextField(
        validators=[MaxLengthValidator(220)],
        null=True,
        blank=True,
        verbose_name='Deviz cümləsi(RU)'
    )
    show_on_home_hero = models.BooleanField(
        default=True,
        verbose_name='Ana səhifə karuselində göstər'
    )
    is_about_page = models.BooleanField(
        default=False,
        verbose_name='Haqqımızda səhifəsi'
    )
    is_contact_page = models.BooleanField(
        default=False,
        verbose_name='Əlaqə səhifəsi'
    )
    is_product_page = models.BooleanField(
        default=False,
        verbose_name='Məhsullar (kateqoriya) səhifəsi'
    )
    is_blog_page = models.BooleanField(
        default=False,
        verbose_name='Bloq səhifəsi'
    )

    class Meta:
        verbose_name = 'Deviz'
        verbose_name_plural = 'Deviz'

    def __str__(self):
        return self.text_az[:60] if self.text_az else 'Deviz'

    @property
    def is_page_motto(self):
        return any([
            self.is_about_page,
            self.is_contact_page,
            self.is_product_page,
            self.is_blog_page,
        ])
