from django.db import models


class Contact(models.Model):
    address_az = models.CharField(
        max_length=255,
        verbose_name='Ünvan (AZ)'
    )
    address_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (EN)'
    )
    address_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (RU)'
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Telefon'
    )
    whatsapp_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Whatsapp əlaqə nömrəsi'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email'
    )
    email_two = models.EmailField(
        null=True,
        blank=True,
        verbose_name='İkinci email'
    )
    instagram = models.URLField(
        null=True,
        blank=True,
        verbose_name=('Instagram')
    )
    facebook = models.URLField(
        null=True,
        blank=True,
        verbose_name=('Facebook')
    )
    youtube = models.URLField(
        null=True,
        blank=True
    )
    linkedn = models.URLField(
        null=True,
        blank=True,
        verbose_name=('Linkedn')
    )
    tiktok = models.URLField(
        null=True,
        blank=True
    )
    map_embed_url = models.TextField(
        null=True,
        blank=True,
        verbose_name='Google Xəritə linki (embed)',
        help_text='Google Maps-dən «Paylaş → Xəritəni daxil et» bölməsindən iframe src linkini yapışdırın.',
    )

    class Meta:
        verbose_name = 'Əlaqə məlumatları'
        verbose_name_plural = 'Əlaqə məlumatları'

    def __str__(self):
        return self.address_az or 'Əlaqə'
