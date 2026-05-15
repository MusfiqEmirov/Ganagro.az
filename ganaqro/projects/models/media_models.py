from django.db import models
from django.db.models import Q
from django.core.files.storage import default_storage
import logging

from .project_models import Product
from .partner_models import Partner
from .about_models import About

logger = logging.getLogger(__name__)


def media_not_marked_as_background_q():
    """Filter for content media only (exclude rows flagged as page background images)."""
    return (
        Q(is_home_page_background_image=False)
        & Q(is_about_page_background_image=False)
        & Q(is_contact_page_background_image=False)
        & Q(is_product_page_background_image=False)
    )


class Media(models.Model):
    about = models.ForeignKey(
        About,
        related_name='medias',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Haqqımızda'
    )
    product = models.ForeignKey(
        Product,
        related_name='medias',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Məhsul'
    )
    partner = models.ForeignKey(
        Partner,
        related_name='medias',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Tərəfdaş'
    )
    name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Ad',
    )
    short_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Qısa məlumat',
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Şəkil'
    )
    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True,
        verbose_name='Video'
    )
    is_home_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Ana səhifə fon şəkli'
    )
    is_about_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Haqqımızda səhifəsi fon şəkli'
    )
    is_contact_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Əlaqə səhifəsi fon şəkli'
    )
    is_product_page_background_image = models.BooleanField(
        default=False,
        verbose_name='Məhsullar səhifəsi fon şəkli'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'

    @property
    def webp_url(self):
        return self.image.url

    def delete_files(self):
        if not self.image:
            return

        image_name = self.image.name
        image_id = self.pk

        logger.info(f"[MEDIA DELETE] Deleting files (ID: {image_id}, File: {image_name})")

        try:
            storage = default_storage

            if image_name.lower().endswith('.webp'):
                base_name = image_name.rsplit('.', 1)[0]
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    original_name = base_name + ext
                    if storage.exists(original_name):
                        try:
                            storage.delete(original_name)
                        except Exception as e:
                            logger.error(f"[MEDIA DELETE] Error deleting original ({original_name}): {e}")

                if storage.exists(image_name):
                    storage.delete(image_name)
            else:
                webp_name = image_name.rsplit('.', 1)[0] + '.webp'
                if storage.exists(webp_name):
                    try:
                        storage.delete(webp_name)
                    except Exception as e:
                        logger.error(f"[MEDIA DELETE] Error deleting webp ({webp_name}): {e}")

                if storage.exists(image_name):
                    storage.delete(image_name)

        except Exception as e:
            logger.error(f"[MEDIA DELETE] Error occurred (ID: {image_id}): {e}")

    def delete(self, *args, **kwargs):
        self.delete_files()
        super().delete(*args, **kwargs)
