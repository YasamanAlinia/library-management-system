from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create Librarian and Member groups and assign permissions'

    def handle(self, *args, **kwargs):
        librarian_group, _ = Group.objects.get_or_create(name='Librarian')
        member_group, _ = Group.objects.get_or_create(name='Member')

        perms = Permission.objects.filter(
            codename__in= [
                'add_book',
                'change_book',
                'delete_book',
                'view_borrow',
                'add_borrow',
                'change_borrow',
            ]
        )
        member_perm = perms.filter(codename__in=['add_borrow',])

        librarian_group.permissions.set(perms)
        member_group.permissions.set(member_perm)

        
        self.stdout.write(self.style.SUCCESS('Librarian and Member groups have been set up'))