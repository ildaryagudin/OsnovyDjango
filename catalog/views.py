from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Product, Category
from .forms import ProductForm


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

    @method_decorator(cache_page(60 * 15))  # Кешируем на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ContactsView(TemplateView):
    """CBV для отображения страницы контактов"""
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    """CBV для отображения списка всех продуктов с низкоуровневым кешированием"""
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        """Получаем продукты с низкоуровневым кешированием"""
        cache_key = 'all_products'
        products = cache.get(cache_key)

        if products is None:
            # Если нет в кеше, получаем из базы
            products = Product.objects.select_related('category', 'owner').all()

            # Сохраняем в кеш
            if settings.CACHE_ENABLED:
                cache.set(cache_key, products, settings.CACHE_TIMEOUT)

        return products


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Привязываем продукт к текущему пользователю"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """Перенаправляем на страницу отредактированного продукта"""
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления продукта (только для авторизованных)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class CategoryProductsView(ListView):
    """CBV для отображения продуктов по категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Получаем продукты для указанной категории с кешированием"""
        category_slug = self.kwargs['category_slug']
        return get_products_by_category(category_slug)

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст"""
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        context['category'] = get_category_by_slug(category_slug)
        return context


class CategoryListView(ListView):
    """CBV для отображения списка всех категорий"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Получаем категории с кешированием"""
        from .services import get_all_categories
        return get_all_categories()