from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Product


class Command(BaseCommand):
    help = 'Create Moderator group with specific permissions'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модераторы')
        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'change_product',
            'delete_product',
            'view_product',
            'can_publish',
            'can_moderate',
        ])

        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created "Модераторы" group with permissions.'))
