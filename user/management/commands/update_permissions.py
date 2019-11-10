from django.core.management.base import BaseCommand
from user.models import Role
from user.constants import NORMAL_USER_PERMISSIONS


class Command(BaseCommand):
    help = "Update Permissions"

    def handle(self, *args, **kwargs):
        normal_role = Role.objects.filter(name='normal').first()
        if not normal_role:
            normal_role = Role(
                name='normal'
            )
            normal_role.save()
        normal_role.permissions = NORMAL_USER_PERMISSIONS
        normal_role.save()
