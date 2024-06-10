# FILE GENERATED WITH CHATGPT

from django.core.management.base import BaseCommand
from init_db import init_db

class Command(BaseCommand):
    help = 'Initialize the database with dummy data'

    def handle(self, *args, **kwargs):
        init_db()
        self.stdout.write(self.style.SUCCESS('Database initialized successfully'))
