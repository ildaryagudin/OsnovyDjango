from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает права доступа'

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем группу "Модератор продуктов"
        moderators_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем необходимые права
        permissions = [
            'can_unpublish_product',
            'can_change_product_status',
            'delete_product',  # Удаление любого продукта
            'view_product',  # Просмотр продуктов
        ]

        for perm_codename in permissions:
            try:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=perm_codename
                )
                moderators_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Право {perm_codename} не найдено')
                )

        moderators_group.save()

        self.stdout.write(
            self.style.SUCCESS('✅ Группа "Модератор продуктов" создана с правами:')
        )
        for perm in moderators_group.permissions.all():
            self.stdout.write(f'   - {perm.name}')