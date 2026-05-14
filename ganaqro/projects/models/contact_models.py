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

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqələr"

    def __str__(self):
        return self.address_az or 'Əlaqə'
