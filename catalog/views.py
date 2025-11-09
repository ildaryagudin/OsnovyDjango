from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


class ProductOwnerMixin:
    """Миксин для проверки владельца продукта"""

    def test_func(self):
        """Проверяем, что пользователь - владелец или модератор"""
        product = self.get_object()
        user = self.request.user

        # Владелец может все
        if product.owner == user:
            return True

        # Модератор может удалять и менять статус
        if user.has_perm('catalog.delete_product') or user.has_perm('catalog.can_change_product_status'):
            return True

        return False


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Привязываем продукт к текущему пользователю"""
        form.instance.owner = self.request.user
        form.instance.status = 'moderation'  # Новые продукты на модерации
        messages.success(self.request, 'Продукт успешно создан и отправлен на модерацию!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerMixin, UpdateView):
    """CBV для редактирования продукта (только для владельца)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """При редактировании снова отправляем на модерацию"""
        if form.instance.status == 'published':
            form.instance.status = 'moderation'
            messages.info(self.request, 'Продукт отправлен на повторную модерацию.')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, ProductOwnerMixin, DeleteView):
    """CBV для удаления продукта (владелец или модератор)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        """Расширенная проверка для удаления"""
        product = self.get_object()
        user = self.request.user

        # Владелец может удалять свои продукты
        if product.owner == user:
            return True

        # Модератор может удалять любые продукты
        if user.has_perm('catalog.delete_product'):
            return True

        return False


class ProductDetailView(DetailView):
    """CBV для отображения страницы с подробной информацией о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    """CBV для отображения списка всех продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        """Показываем только опубликованные продукты или продукты пользователя"""
        queryset = Product.objects.filter(status='published')

        # Если пользователь авторизован, показываем также его продукты
        if self.request.user.is_authenticated:
            user_products = Product.objects.filter(owner=self.request.user)
            queryset = queryset | user_products

        return queryset.distinct().order_by('-created_at')


class ModeratorProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Список продуктов для модерации"""
    model = Product
    template_name = 'catalog/moderator_product_list.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.has_perm('catalog.can_change_product_status')

    def get_queryset(self):
        return Product.objects.filter(status__in=['moderation', 'published']).order_by('-created_at')


class ChangeProductStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Изменение статуса продукта модератором"""
    model = Product
    fields = ['status']
    template_name = 'catalog/change_product_status.html'

    def test_func(self):
        return self.request.user.has_perm('catalog.can_change_product_status')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Статус продукта изменен на: {form.instance.get_status_display()}')
        return response

    def get_success_url(self):
        return reverse_lazy('catalog:moderator_product_list')