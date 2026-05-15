from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from projects.utils.cache_utils import invalidate_model_cache, invalidate_query_cache
from projects.models import (
    AppealContact,
    Product,
    ProductCategory,
    Partner,
    About,
    Contact,
    Media,
    Motto,
    Statistic,
    Blog,
)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    invalidate_model_cache('Product')


@receiver(post_save, sender=ProductCategory)
@receiver(post_delete, sender=ProductCategory)
def invalidate_product_category_cache(sender, instance, **kwargs):
    invalidate_model_cache('ProductCategory')


@receiver(post_save, sender=Partner)
@receiver(post_delete, sender=Partner)
def invalidate_partner_cache(sender, instance, **kwargs):
    invalidate_model_cache('Partner')


@receiver(post_save, sender=About)
@receiver(post_delete, sender=About)
def invalidate_about_cache(sender, instance, **kwargs):
    invalidate_model_cache('About')


@receiver(post_save, sender=Contact)
@receiver(post_delete, sender=Contact)
def invalidate_contact_cache(sender, instance, **kwargs):
    invalidate_model_cache('Contact')


@receiver(post_save, sender=Media)
@receiver(post_delete, sender=Media)
def invalidate_media_cache(sender, instance, **kwargs):
    invalidate_model_cache('Media')

    if getattr(instance, 'product_id', None):
        invalidate_model_cache('Product')
    if getattr(instance, 'partner_id', None):
        invalidate_model_cache('Partner')
    if getattr(instance, 'about_id', None):
        invalidate_model_cache('About')


@receiver(post_save, sender=Motto)
@receiver(post_delete, sender=Motto)
def invalidate_motto_cache(sender, instance, **kwargs):
    invalidate_model_cache('Motto')


@receiver(post_save, sender=Statistic)
@receiver(post_delete, sender=Statistic)
def invalidate_statistic_cache(sender, instance, **kwargs):
    invalidate_query_cache(['get_statistics'])
    invalidate_model_cache('Statistic')


@receiver(post_save, sender=AppealContact)
@receiver(post_delete, sender=AppealContact)
def invalidate_appeal_contact_cache(sender, instance, **kwargs):
    invalidate_model_cache('AppealContact')


@receiver(post_save, sender=Blog)
@receiver(post_delete, sender=Blog)
def invalidate_blog_cache(sender, instance, **kwargs):
    invalidate_model_cache('Blog')
