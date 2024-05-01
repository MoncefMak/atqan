from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


# To run python manage.py add_default_permissions
class Command(BaseCommand):
    help = 'Assign users to Admin or Client group'

    def handle(self, *args, **options):
        # Get or create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        client_group, created = Group.objects.get_or_create(name='Client')

        admin_permissions = [
            "accounts.view_user",
            "accounts.add_user",
            "accounts.change_user",
            "accounts.delete_user"
        ]

        for permission_string in admin_permissions:
            app_label, codename = permission_string.split('.')
            permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
            admin_group.permissions.add(permission)

        client_permission = [
            "product.view_product",
            "product.add_product",
        ]

        # Add default permissions to Workshop Visitor group
        for permission_string in client_permission:
            app_label, codename = permission_string.split('.')
            permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
            client_group.permissions.add(permission)

        admin_group.save()
        client_group.save()

        self.stdout.write(self.style.SUCCESS('Default permissions added to groups successfully.'))
