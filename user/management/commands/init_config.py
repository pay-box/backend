from django.core.management.base import BaseCommand
from user.models import Config


class Command(BaseCommand):
    help = "INIT CONFIG"

    def handle(self, *args, **kwargs):
        if Config.objects.count() == 0:
            Config().save()
