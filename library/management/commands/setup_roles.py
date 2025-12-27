from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create Librarian group and assign permissions'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Librarian')

        perms = Permission.objects.filter(
            codename__in=['add_book', 'change_book', 'delete_book']
        )

        group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS('Librarian group has been set up'))