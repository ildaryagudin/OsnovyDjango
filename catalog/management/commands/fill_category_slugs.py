from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Заполняет slug поля для существующих категорий'

    def handle(self, *args, **options):
        categories = Category.objects.filter(slug='')

        for category in categories:
            category.save()  # Автоматически создаст slug при сохранении

        self.stdout.write(
            self.style.SUCCESS(f'✅ Slug поля заполнены для {categories.count()} категорий')
        )