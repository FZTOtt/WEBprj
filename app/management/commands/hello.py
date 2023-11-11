from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Display hello.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Hello")