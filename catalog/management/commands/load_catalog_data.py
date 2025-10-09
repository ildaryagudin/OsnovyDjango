import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загрузка тестовых данных для каталога'

    def handle(self, *args, **options):
        # Удаляем существующие данные
        self.stdout.write('Удаление существующих данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        self.stdout.write('Создание категорий...')
        electronics = Category.objects.create(
            name='Электроника',
            description='Техника и электронные устройства'
        )

        books = Category.objects.create(
            name='Книги',
            description='Художественная и учебная литература'
        )

        home = Category.objects.create(
            name='Товары для дома',
            description='Товары для обустройства дома'
        )

        # Создаем продукты
        self.stdout.write('Создание продуктов...')

        # Электроника
        Product.objects.create(
            name='Смартфон Xiaomi',
            description='Современный смартфон с AMOLED экраном',
            category=electronics,
            price=19999.99
        )

        Product.objects.create(
            name='Наушники Sony',
            description='Беспроводные наушники с шумоподавлением',
            category=electronics,
            price=8999.99
        )

        # Книги
        Product.objects.create(
            name='Python для начинающих',
            description='Учебник по программированию на Python',
            category=books,
            price=1500.00
        )

        Product.objects.create(
            name='Война и мир',
            description='Роман Льва Толстого',
            category=books,
            price=1200.00
        )

        # Товары для дома
        Product.objects.create(
            name='Кофемашина',
            description='Автоматическая кофемашина для дома',
            category=home,
            price=25000.00
        )

        Product.objects.create(
            name='Пылесос',
            description='Мощный пылесос с HEPA фильтром',
            category=home,
            price=8999.99
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Тестовые данные успешно загружены!')
        )
        self.stdout.write(f'Создано категорий: {Category.objects.count()}')
        self.stdout.write(f'Создано продуктов: {Product.objects.count()}')