from django.db import models

class Statistic(models.Model):
    value_one = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 1'
    )
    value_two = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 2'
    )
    value_three = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 3'
    )
    value_four = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 4'
    )
    caption_one_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 1 — alt yazı (AZ)',
    )
    caption_one_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 1 — alt yazı (EN)',
    )
    caption_one_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 1 — alt yazı (RU)',
    )
    caption_two_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 2 — alt yazı (AZ)',
    )
    caption_two_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 2 — alt yazı (EN)',
    )
    caption_two_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 2 — alt yazı (RU)',
    )
    caption_three_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 3 — alt yazı (AZ)',
    )
    caption_three_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 3 — alt yazı (EN)',
    )
    caption_three_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 3 — alt yazı (RU)',
    )
    caption_four_az = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 4 — alt yazı (AZ)',
    )
    caption_four_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 4 — alt yazı (EN)',
    )
    caption_four_ru = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Say 4 — alt yazı (RU)',
    )

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'

    def __str__(self):
        return 'Statistika'

   
    
   
