from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    """Контроллер для отображения домашней страницы"""
    products = Product.objects.all()[:6]  # Берем первые 6 товаров для главной
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    """Контроллер для отображения страницы с контактной информацией"""
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    """Контроллер для отображения страницы с подробной информацией о товаре"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})