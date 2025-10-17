from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category


class HomeView(ListView):
    """CBV для отображения домашней страницы"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Возвращаем только первые 6 товаров для главной страницы"""
        return Product.objects.all()[:6]


class ProductDetailView(DetailView):
    """CBV для отображения страницы с подробной информацией о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    """CBV для отображения страницы контактов"""
    template_name = 'catalog/contacts.html'