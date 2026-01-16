from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate product list caches when a product is created, updated or deleted
    """
    print("Clearing product cahce")
    # cache.delete_pattern("foo_*", itersize=100_000)
    # clear product list caches
    cache.delete_pattern("*cached_product_list*")
