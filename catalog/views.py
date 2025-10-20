from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.forms import inlineformset_factory
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


class ContactsView(TemplateView):
    """CBV для отображения страницы контактов"""
    template_name = 'catalog/contacts.html'


class ProductCreateView(CreateView):
    """CBV для создания нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    """CBV для редактирования продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """Перенаправляем на страницу отредактированного продукта"""
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """CBV для удаления продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductListView(ListView):
    """CBV для отображения списка всех продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9  # Пагинация по 9 товаров на странице