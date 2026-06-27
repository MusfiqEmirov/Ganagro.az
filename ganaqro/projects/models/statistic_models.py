from django.db import models

from projects.constants.icon_choices import STATISTIC_ICON_CHOICES


class Statistic(models.Model):
    value_one = models.CharField(
        max_length=32,
        verbose_name='1-ci kart — böyük rəqəm',
        help_text='Məsələn: 25 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
    )
    value_two = models.CharField(
        max_length=32,
        verbose_name='2-ci kart — böyük rəqəm',
        help_text='Məsələn: 150 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
    )
    value_three = models.CharField(
        max_length=32,
        verbose_name='3-cü kart — böyük rəqəm',
        help_text='Məsələn: 500 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
    )
    value_four = models.CharField(
        max_length=32,
        verbose_name='4-cü kart — böyük rəqəm',
        help_text='Məsələn: 1000 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
    )
    caption_one_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='1-ci kart — alt yazı (AZ)',
        help_text='Rəqəmin altında görünən qısa mətn. Məs: İllik təcrübə',
    )
    caption_one_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='1-ci kart — alt yazı (EN)',
        help_text='English version of the caption below the first number.',
    )
    caption_one_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='1-ci kart — alt yazı (RU)',
        help_text='Русская версия подписи под первым числом.',
    )
    caption_two_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='2-ci kart — alt yazı (AZ)',
        help_text='Məs: Məhsul növü',
    )
    caption_two_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='2-ci kart — alt yazı (EN)',
    )
    caption_two_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='2-ci kart — alt yazı (RU)',
    )
    caption_three_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='3-cü kart — alt yazı (AZ)',
        help_text='Məs: Müştəri sayı',
    )
    caption_three_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='3-cü kart — alt yazı (EN)',
    )
    caption_three_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='3-cü kart — alt yazı (RU)',
    )
    caption_four_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='4-cü kart — alt yazı (AZ)',
        help_text='Məs: Layihə sayı',
    )
    caption_four_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='4-cü kart — alt yazı (EN)',
    )
    caption_four_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='4-cü kart — alt yazı (RU)',
    )
    icon_one = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        choices=STATISTIC_ICON_CHOICES,
        verbose_name='1-ci kart — ikon',
        help_text='İstəsəniz boş buraxa bilərsiniz.',
    )
    icon_two = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        choices=STATISTIC_ICON_CHOICES,
        verbose_name='2-ci kart — ikon',
        help_text='İstəsəniz boş buraxa bilərsiniz.',
    )
    icon_three = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        choices=STATISTIC_ICON_CHOICES,
        verbose_name='3-cü kart — ikon',
        help_text='İstəsəniz boş buraxa bilərsiniz.',
    )
    icon_four = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        choices=STATISTIC_ICON_CHOICES,
        verbose_name='4-cü kart — ikon',
        help_text='İstəsəniz boş buraxa bilərsiniz.',
    )

    class Meta:
        verbose_name = 'Statistika (saylar bloku)'
        verbose_name_plural = 'Statistika (saylar bloku)'

    def __str__(self):
        return 'Sayt statistikası'
