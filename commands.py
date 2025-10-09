from catalog.models import Category, Product
from django.utils import timezone

# 1. Создание категорий
electronics = Category.objects.create(
    name='Электроника',
    description='Техника и электронные устройства'
)

books = Category.objects.create(
    name='Книги',
    description='Художественная и учебная литература'
)

clothing = Category.objects.create(
    name='Одежда',
    description='Одежда и аксессуары'
)

# 2. Создание продуктов
product1 = Product.objects.create(
    name='Смартфон Samsung',
    description='Современный смартфон с большим экраном',
    category=electronics,
    price=25000.00
)

product2 = Product.objects.create(
    name='Ноутбук HP',
    description='Мощный ноутбук для работы и игр',
    category=electronics,
    price=55000.00
)

product3 = Product.objects.create(
    name='Роман "Война и мир"',
    description='Классика русской литературы',
    category=books,
    price=1500.00
)

product4 = Product.objects.create(
    name='Футболка хлопковая',
    description='Комфортная футболка из натурального хлопка',
    category=clothing,
    price=1200.00
)

# 3. Получение всех категорий
all_categories = Category.objects.all()
print("Все категории:")
for category in all_categories:
    print(f"- {category.name}")

# 4. Получение всех продуктов
all_products = Product.objects.all()
print("\nВсе продукты:")
for product in all_products:
    print(f"- {product.name} - {product.price} руб.")

# 5. Поиск продуктов в определенной категории
electronics_products = Product.objects.filter(category=electronics)
print(f"\nПродукты в категории 'Электроника':")
for product in electronics_products:
    print(f"- {product.name}")

# 6. Обновление цены продукта
product_to_update = Product.objects.get(name='Смартфон Samsung')
product_to_update.price = 23000.00
product_to_update.save()
print(f"\nОбновленная цена смартфона: {product_to_update.price}")

# 7. Удаление продукта
product_to_delete = Product.objects.get(name='Футболка хлопковая')
product_to_delete.delete()
print("Продукт 'Футболка хлопковая' удален")

# 8. Проверка оставшихся продуктов
remaining_products = Product.objects.all()
print(f"\nОставшиеся продукты: {remaining_products.count()}")