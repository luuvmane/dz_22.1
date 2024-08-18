from django.core.cache import cache
from .models import Category


def get_cached_categories():
    cache_key = 'categories'
    categories = cache.get(cache_key)
    if not categories:
        categories = Category.objects.all()
        cache.set(cache_key, categories, timeout=3600)
    return categories
