from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_slug):
    """
    Сервисная функция для получения продуктов по категории
    с использованием кеширования
    """
    cache_key = f'products_category_{category_slug}'
    products = cache.get(cache_key)

    if products is None:
        # Если нет в кеше, получаем из базы
        products = Product.objects.filter(
            category__slug=category_slug
        ).select_related('category')

        # Сохраняем в кеш
        if settings.CACHE_ENABLED:
            cache.set(cache_key, products, settings.CACHE_TIMEOUT)

    return products


def get_all_categories():
    """
    Сервисная функция для получения всех категорий с кешированием
    """
    cache_key = 'all_categories'
    categories = cache.get(cache_key)

    if categories is None:
        categories = Category.objects.all()
        if settings.CACHE_ENABLED:
            cache.set(cache_key, categories, settings.CACHE_TIMEOUT)

    return categories


def get_category_by_slug(category_slug):
    """
    Сервисная функция для получения категории по slug
    """
    cache_key = f'category_{category_slug}'
    category = cache.get(cache_key)

    if category is None:
        try:
            category = Category.objects.get(slug=category_slug)
            if settings.CACHE_ENABLED:
                cache.set(cache_key, category, settings.CACHE_TIMEOUT)
        except Category.DoesNotExist:
            category = None

    return category